"""
A basic webserver to test the site layout and pages.
"""

import logging
import os


def find_file(host: str, content_dir: str) -> tuple[bytes, str]:
    fragments = host.split(".")[:-1]
    fragments.reverse()
    logging.debug(f"Finding file for host {host} with fragments {fragments}")

    path = os.path.join(content_dir, "index.html")  # default
    if fragments:
        new_path = os.path.join(content_dir, *fragments[:-1])
        matching_files_at_path = [
            filename
            for filename in os.listdir(new_path)
            if filename.split(".")[0].lower() == fragments[-1].lower()
        ]
        if len(matching_files_at_path) == 0:
            new_path = os.path.join(new_path, "index.html")
        elif len(matching_files_at_path) == 1:
            new_path = os.path.join(new_path, matching_files_at_path[0])
            if os.path.isdir(new_path):
                new_path = os.path.join(new_path, "index.html")
        elif len(matching_files_at_path) == 2:
            first_is_file = os.path.isfile(
                os.path.join(new_path, matching_files_at_path[0])
            )
            second_is_file = os.path.isfile(
                os.path.join(new_path, matching_files_at_path[1])
            )
            if first_is_file and second_is_file:
                msg = (
                    "Two files with the same name in the same directory: "
                    f"{matching_files_at_path}"
                )
                raise ValueError(msg)
            if not first_is_file and not second_is_file:
                msg = (
                    "Two directories with the same name in the same "
                    "directory: "
                    f"{matching_files_at_path}"
                )
                raise ValueError(msg)
            if first_is_file:
                new_path = os.path.join(new_path, matching_files_at_path[0])
            else:
                new_path = os.path.join(
                    new_path, matching_files_at_path[1]
                )
        else:
            msg = (
                "More than two files with the same name in the same "
                "directory: "
                f"{matching_files_at_path}"
            )
            raise ValueError(msg)

        path = new_path

    with open(path, "rb") as f:
        _, ext = os.path.splitext(path)
        # Strip leading dot and lowercase for mime lookup
        ext = ext[1:].lower() if ext.startswith(".") else ext.lower()
        return f.read(), ext or "html"
