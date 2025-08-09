import markdown

from beneggerscom.utils.config import CONFIG
from beneggerscom.ssg.input_files import InputFile

import logging


class MarkdownFile(InputFile):
    # TODO
    title: str = ""
    date: str = ""
    meta_title: str = ""
    layout: str = CONFIG["default_layout"]
    nav: int = -1
    description: str = ""
    content: str = ""
    draft: bool = False

    @classmethod
    def from_lines(
        _cls, lines: list[str], base_site_title: str = "Ben Eggers dot com"
    ):
        markdown_file = MarkdownFile()
        logging.debug("Read lines %s", lines)
        if lines[0].strip() != "---":
            raise ValueError("Lines do not begin with metadata marker (---).")

        metadata_end = 0
        for i, line in enumerate(lines[1:]):
            if line.strip().startswith("---"):
                # We start at 1 so we need to add 1
                metadata_end = i + 1
                break
            key, value = line.split(":")
            markdown_file._set_metadata_item(
                key.strip().lower(), value.strip()
            )
        logging.debug("Metadata ends at line %d", metadata_end + 1)
        logging.debug("markdown_file after metadata ingest: %s", markdown_file)

        # Add one because the start index is inclusive
        markdown_file.content = "\n".join(lines[metadata_end + 1:])

        if not markdown_file.title:
            raise ValueError(f"No title for file. Parsed {markdown_file}")
        if markdown_file.meta_title == "_base":
            markdown_file.meta_title = base_site_title
        if not markdown_file.meta_title:
            markdown_file.meta_title = markdown_file.title
            if base_site_title:
                markdown_file.meta_title = (
                    markdown_file.meta_title + " | " + base_site_title
                )
        return markdown_file

    def content_as_html(self) -> str:
        return markdown.markdown(
            self.content,
            extensions=[
                "footnotes",
                "fenced_code",
                "tables",
            ],
        )

    def _set_metadata_item(self, key: str, value: str):
        if key == "title":
            self.title = value
        elif key == "date":
            self.date = value
        elif key == "layout":
            self.layout = value
        elif key == "nav":
            self.nav = int(value)
        elif key == "description":
            self.description = value
        elif key == "meta_title":
            self.meta_title = value
        elif key == "draft":
            v = value.lower()
            if v not in ("true", "false"):
                raise ValueError(f"Invalid boolean for draft: {value}")
            self.draft = v == "true"
        else:
            raise ValueError(f"Unknown metadata key: {key}")
