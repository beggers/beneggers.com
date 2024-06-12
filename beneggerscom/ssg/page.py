from __future__ import annotations
import re
from typing import Optional

from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.input_files.layout import LayoutFile

import logging

END_REGEX = re.compile(r"{% end %}")
FOR_REGEX = re.compile(r"{% for (?P<var>.+?) in (?P<iter>.+?) %}")
LAYOUT_INCLUDE_REGEX = re.compile(r"{% include (?P<layout>.+?) %}")
VARIABLE_REGEX = re.compile(r"{% (?P<var>.+?) %}")


class EvalContext:
    # This class exists purely to provide documentation for the eval() calls.
    # It's plumbed into the code even though it doesn't really need to be. This
    # ensures that I keep it up to date.
    base_url: str
    protocol: str
    pages: list[Page]
    page: Page

    def as_dict(self) -> dict[str, str | list[Page] | Page]:
        return {
            "base_url": self.base_url,
            "protocol": self.protocol,
            "pages": self.pages,
            "page": self.page,
        }


class Page:
    nav: int = -1
    title: str
    date: str
    description: str
    url: str
    style: str

    _rendered_content: Optional[str]
    _md: MarkdownFile
    _layout: LayoutFile

    def __init__(self,
                 md: MarkdownFile,
                 layout: LayoutFile,
                 style: str,
                 ):
        self._md = md
        self._layout = layout
        self._rendered_content = None
        self._style = style

        self.title = md.title
        self.date = md.date
        self.description = md.description

    def render(self) -> None:
        pass

    def _render_partials(self, partials) -> None:
        rendered = self._layout.content

        include = LAYOUT_INCLUDE_REGEX.search(rendered)
        while include:
            logging.debug("Rendering include %s", include.group("layout"))
            partial_name = include.group("layout")
            if partial_name not in partials:
                raise ValueError(f"Partial '{partial_name}' not found.")
            rendered = rendered.replace(
                include.group(0),
                partials[partial_name].content
            )
            include = LAYOUT_INCLUDE_REGEX.search(rendered)

        self._rendered_content = rendered

    def _render_loops(self, eval_context: EvalContext) -> None:
        if not self._rendered_content:
            raise ValueError("No content to render loops on.")

        eval_variables = eval_context.as_dict()
        rendered = self._rendered_content

        for_match = FOR_REGEX.search(rendered)
        if not for_match:
            return

        loop_end = END_REGEX.search(rendered, for_match.end())
        while for_match:
            if not loop_end:
                raise ValueError(
                    "No end found for for loop starting at", for_match.group(0)
                )
            logging.debug("Rendering for loop %s", for_match.group(0))
            var = for_match.group("var")
            iterable = for_match.group("iter")
            loop_content = rendered[for_match.end(): loop_end.start()]
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
                        m.group(0), e
                    )
                    m = VARIABLE_REGEX.search(current_loop_render)
                rendered_loop += current_loop_render
            logging.debug("Rendered loop: %s", rendered_loop)
            rendered = (
                rendered[: for_match.start()]
                + rendered_loop
                + rendered[loop_end.end():]
            )

            for_match = FOR_REGEX.search(rendered, loop_end.end())
            if for_match:
                loop_end = END_REGEX.search(rendered, for_match.end())

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
            rendered = rendered.replace(var.group(0), e)
            var = VARIABLE_REGEX.search(rendered)

        self._rendered_content = rendered

    def write_to_file(self, path: str) -> None:
        pass
