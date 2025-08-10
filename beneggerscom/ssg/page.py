from __future__ import annotations
import os
import re
from datetime import date
from typing import Optional

from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.input_files.layout import LayoutFile

import logging


IF_START_REGEX = re.compile(r"{% if (?P<cond>.+?) %}")
IF_END_REGEX = re.compile(r"{% end if %}")
FOR_START_REGEX = re.compile(r"{% for (?P<var>.+?) in (?P<iter>.+?) %}")
FOR_END_REGEX = re.compile(r"{% end for %}")
LAYOUT_INCLUDE_REGEX = re.compile(r"{% include (?P<layout>.+?) %}")
VARIABLE_REGEX = re.compile(r"{% (?P<var>.+?) %}")


class EvalContext:
    # This class exists purely to provide documentation for the eval() calls.
    # It's plumbed into the code even though it doesn't really need to be. This
    # ensures that I keep it up to date.
    base_url: str
    protocol: str
    pages: list[Page]
    eng_posts: list[Page]
    thoughts_posts: list[Page]
    page: Page
    site: dict
    # HTML to hydrate
    slot: str

    def as_dict(self) -> dict[str, str | list[Page] | Page | dict]:
        return {
            "base_url": self.base_url,
            "protocol": self.protocol,
            "pages": self.pages,
            "eng_posts": self.eng_posts,
            "thoughts_posts": self.thoughts_posts,
            "page": self.page,
            "slot": self.slot,
            "site": getattr(self, "site", {}),
        }


class Page:
    nav: int = -1
    title: str
    subtitle: str
    date: str
    display_date: str
    meta_title: str
    description: str
    url: str
    style: str

    _rendered_content: Optional[str]
    _md: MarkdownFile
    _layout: LayoutFile
    _path: str

    def __init__(
        self,
        md: MarkdownFile,
        layout: LayoutFile,
        url: str,
        style: str,
        path: str,
    ):
        self._md = md
        self._layout = layout
        self._rendered_content = layout.content
        self._path = path

        self.nav = md.nav
        self.title = md.title
        self.subtitle = getattr(md, "subtitle", "")
        self.date = md.date
        # Just month year
        if md.date:
            self.display_date = date.fromisoformat(md.date).strftime("%B %Y")
        else:
            self.display_date = ""
        self.meta_title = md.meta_title
        self.description = md.description
        self.url = url
        self.style = style

    def render(
        self,
        base_url: str,
        protocol: str,
        partials: dict[str, LayoutFile],
        pages: list[Page],
        eng_posts: list[Page] = [],
        thoughts_posts: list[Page] = [],
    ) -> None:
        eval_context = EvalContext()
        eval_context.base_url = base_url
        eval_context.protocol = protocol
        eval_context.pages = pages
        eval_context.eng_posts = eng_posts
        eval_context.thoughts_posts = thoughts_posts
        eval_context.page = self
        eval_context.slot = self._md.content_as_html()
        eval_context.site = {
            "url": base_url,
            "protocol": protocol,
        }

        # TODO nested loops
        # TODO if statements
        # TODO parametrized partials
        self._render_partials(partials)
        self._render_ifs(eval_context)
        self._render_loops(eval_context)
        self._render_variables(eval_context)

    def _render_partials(self, partials) -> None:
        if not self._rendered_content:
            raise ValueError("No content to render partials on.")

        rendered = self._rendered_content

        include = LAYOUT_INCLUDE_REGEX.search(rendered)
        while include:
            logging.debug("Rendering include %s", include.group("layout"))
            partial_name = include.group("layout")
            if partial_name not in partials:
                raise ValueError(f"Partial '{partial_name}' not found.")
            rendered = rendered.replace(
                include.group(0), partials[partial_name].content
            )
            include = LAYOUT_INCLUDE_REGEX.search(rendered)

        self._rendered_content = rendered

    def _render_ifs(self, eval_context: EvalContext) -> None:
        if not self._rendered_content:
            raise ValueError("No content to render loops on.")
        eval_variables = eval_context.as_dict()
        rendered = self._rendered_content

        if_match = IF_START_REGEX.search(rendered)
        if not if_match:
            return

        if_end = IF_END_REGEX.search(rendered, if_match.end())
        while if_match:
            if not if_end:
                raise ValueError(
                    "No end for if statement starting at ", if_match.group(0)
                )
            logging.debug("Rendering if-statement %s", if_match.group(0))
            cond = if_match.group("cond")
            if_content = rendered[if_match.end() : if_end.start()]
            logging.debug("If content: %s", if_content)

            rendered_body = ""
            if eval(cond, eval_variables):
                rendered_body = if_content
            rendered = (
                rendered[: if_match.start()]
                + rendered_body
                + rendered[if_end.end() :]
            )

            if_match = IF_START_REGEX.search(rendered)
            if if_match:
                if_end = IF_END_REGEX.search(rendered, if_match.end())

        self._rendered_content = rendered

    def _render_loops(self, eval_context: EvalContext) -> None:
        if not self._rendered_content:
            raise ValueError("No content to render loops on.")

        eval_variables = eval_context.as_dict()
        rendered = self._rendered_content

        for_match = FOR_START_REGEX.search(rendered)
        if not for_match:
            return

        loop_end = FOR_END_REGEX.search(rendered, for_match.end())
        while for_match:
            if not loop_end:
                raise ValueError(
                    "No end found for for loop starting at", for_match.group(0)
                )
            logging.debug("Rendering for loop %s", for_match.group(0))
            var = for_match.group("var")
            iterable = for_match.group("iter")
            loop_content = rendered[for_match.end() : loop_end.start()]
            logging.debug("Loop content: %s", loop_content)

            rendered_loop = ""
            logging.debug("Looping over %s", eval(iterable, eval_variables))
            for item in eval(iterable, eval_variables):
                current_loop_render = loop_content
                m = VARIABLE_REGEX.search(current_loop_render)
                while m:
                    logging.debug(
                        "Rendering possibly loop variable %s", m.group(0)
                    )

                    e = eval(m.group("var"), eval_variables, {var: item})
                    logging.debug("Replacing %s with %s", m.group(0), e)

                    current_loop_render = current_loop_render.replace(
                        m.group(0), str(e)
                    )
                    m = VARIABLE_REGEX.search(current_loop_render)
                rendered_loop += current_loop_render
            logging.debug("Rendered loop: %s", rendered_loop)
            rendered = (
                rendered[: for_match.start()]
                + rendered_loop
                + rendered[loop_end.end() :]
            )

            for_match = FOR_START_REGEX.search(rendered, loop_end.end())
            if for_match:
                loop_end = FOR_END_REGEX.search(rendered, for_match.end())

        self._rendered_content = rendered

    def _render_variables(self, eval_context: EvalContext) -> None:
        if not self._rendered_content:
            raise ValueError("No content to render variables on.")

        eval_variables = eval_context.as_dict()
        rendered = self._rendered_content

        var = VARIABLE_REGEX.search(rendered)
        while var:
            logging.debug("Rendering non-loop variable %s", var.group(0))
            e = eval(var.group("var"), eval_variables)
            logging.debug("Replacing %s with %s", var.group(0), e)
            rendered = rendered.replace(var.group(0), str(e))
            var = VARIABLE_REGEX.search(rendered)

        self._rendered_content = rendered

    def flush(self) -> None:
        if not self._rendered_content:
            raise ValueError("No content to write to file.")
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w") as f:
            f.write(self._rendered_content)
