# I couldn't find a markdown processor that handles sidenotes how I want.
# So here we are.

import re
from typing import Dict, List, Optional, Tuple, Match


BOLD_REGEX = r"\*\*(.*?)\*\*|__([^_]*?)__"
HEADER_REGEX = r"^(#+)\s(.+)"
ITALICS_REGEX = r"\*(.*?)\*|_([^_]*?)_"
LINK_REGEX = r"\[([^\]]+)\]\(([^)]+)\)"
FOOTNOTE_DEF_REGEX = r"^\[\^([^\]]+)\]:\s*(.*)$"
FOOTNOTE_REF_REGEX = r"\[\^([^\]]+)\]"


def str_to_html(raw_md: str) -> str:
    # Extract footnote definitions first so they don't interfere
    # with other parsing
    content_wo_fns, footnotes = _extract_footnotes(raw_md)

    html = _process_headings(content_wo_fns)
    html = _process_paragraphs_and_lists(html, footnotes)
    html = _process_links(html)
    html = _process_bolds(html)
    html = _process_italics(html)
    return html


def _process_headings(raw_md: str) -> str:
    def replace_with_header(match: Match[str]) -> str:
        header_level = len(match.group(1))
        header_text = match.group(2).strip()
        return f"<h{header_level}>{header_text}</h{header_level}>"

    return re.sub(
        HEADER_REGEX, replace_with_header, raw_md, flags=re.MULTILINE
    )


def _process_bolds(raw_md: str) -> str:
    def replace_with_strong(match: Match[str]) -> str:
        return f"<strong>{match.group(1) or match.group(2)}</strong>"

    return re.sub(BOLD_REGEX, replace_with_strong, raw_md)


def _process_italics(raw_md: str) -> str:
    def replace_with_em(match: Match[str]) -> str:
        return f"<em>{match.group(1) or match.group(2)}</em>"

    return re.sub(ITALICS_REGEX, replace_with_em, raw_md)


def _process_links(raw_md: str) -> str:
    def replace_with_a(match: Match[str]) -> str:
        return f'<a href="{match.group(2)}">{match.group(1)}</a>'

    return re.sub(LINK_REGEX, replace_with_a, raw_md)


def _extract_footnotes(raw_md: str) -> Tuple[str, Dict[str, str]]:
    lines = raw_md.split("\n")
    kept_lines: List[str] = []
    footnotes: Dict[str, str] = {}

    current_id: Optional[str] = None
    current_chunks: List[str] = []

    def flush_current() -> None:
        nonlocal current_id, current_chunks
        if current_id is not None:
            # Join with spaces; strip indentation on continuation lines
            value = " ".join(
                [chunk for chunk in current_chunks if chunk is not None]
            ).strip()
            footnotes[current_id] = value
        current_id = None
        current_chunks = []

    for line in lines:
        m = re.match(FOOTNOTE_DEF_REGEX, line)
        if m:
            # Starting a new footnote
            flush_current()
            current_id = m.group(1)
            current_chunks = [m.group(2)] if m.group(2) else []
            continue
        # Continuation lines are indented by at least 4 spaces or a tab
        if current_id is not None and (
            line.startswith("    ")
            or line.startswith("\t")
            or line.strip() == ""
        ):
            # Remove one level of indentation if present
            if line.startswith("    "):
                current_chunks.append(line[4:])
            elif line.startswith("\t"):
                current_chunks.append(line[1:])
            else:
                current_chunks.append("")
            continue
        # Not a footnote def or continuation: keep the line and flush if needed
        flush_current()
        kept_lines.append(line)

    flush_current()
    return "\n".join(kept_lines), footnotes


def _process_paragraphs_and_lists(
    raw_md: str, footnotes: Optional[Dict[str, str]] = None
) -> str:
    lines = raw_md.split("\n")

    output_lines: List[str] = []
    in_paragraph: bool = False
    # Each element is (indent_level, "ul" or "ol")
    list_stack: list[Tuple[int, str]] = []
    in_list_item: bool = False

    # Accumulate the current paragraph's text so we can post-process footnotes
    current_paragraph_chunks: List[str] = []

    def close_paragraph() -> None:
        nonlocal in_paragraph, current_paragraph_chunks
        if in_paragraph:
            paragraph_text = " ".join(
                [c for c in current_paragraph_chunks if c]
            )

            # Replace footnote refs and optionally render aside when present
            paragraph_html = f"<p>{paragraph_text}</p>"
            aside_html = ""
            if footnotes is not None:
                refs_in_para = re.findall(FOOTNOTE_REF_REGEX, paragraph_text)
                if refs_in_para:
                    # assign numbers in order of first appearance
                    assigned_numbers: Dict[str, int] = {}
                    next_num = 1

                    def replace_ref(m: Match[str]) -> str:
                        nonlocal next_num
                        ref_id = m.group(1)
                        if ref_id not in assigned_numbers:
                            assigned_numbers[ref_id] = next_num
                            next_num += 1
                        num = assigned_numbers[ref_id]
                        return f'<sup class="fn-ref">{num}</sup>'

                    # Render superscripts
                    paragraph_text = re.sub(r"^<p>", "", paragraph_text)
                    replaced_refs = re.sub(
                        FOOTNOTE_REF_REGEX, replace_ref, paragraph_text
                    )
                    paragraph_html = f"<p>{replaced_refs}</p>"

                    # Render aside with ordered list of footnotes for this
                    # paragraph
                    if assigned_numbers:
                        items: List[str] = []
                        for ref_id, num in sorted(
                            assigned_numbers.items(), key=lambda kv: kv[1]
                        ):
                            body = (
                                footnotes.get(ref_id, "")
                                if footnotes is not None
                                else ""
                            )
                            items.append(f"<li>{body}</li>")
                        aside_html = (
                            '<aside class="footnote"><ol>'
                            + "".join(items)
                            + "</ol></aside>"
                        )

            if aside_html:
                # Wrap paragraph and aside together so CSS can place
                # side-by-side
                output_lines.append('<div class="para-with-footnote">')
                output_lines.append(paragraph_html)
                output_lines.append(aside_html)
                output_lines.append("</div>")
            else:
                output_lines.append(paragraph_html)

            in_paragraph = False
            current_paragraph_chunks = []

    def close_list_item() -> None:
        nonlocal in_list_item
        if in_list_item:
            close_paragraph()
            output_lines.append("</li>")
            in_list_item = False

    def close_all_lists() -> None:
        nonlocal list_stack, in_list_item
        close_list_item()
        while list_stack:
            _, ltype = list_stack.pop()
            output_lines.append(f"</{ltype}>")

    def start_paragraph() -> None:
        nonlocal in_paragraph, current_paragraph_chunks
        if not in_paragraph:
            current_paragraph_chunks = []
            in_paragraph = True

    def start_list_item() -> None:
        nonlocal in_list_item
        close_list_item()
        output_lines.append("<li>")
        in_list_item = True

    def close_lists_down_to(indent_level: int) -> None:
        nonlocal list_stack
        while list_stack and list_stack[-1][0] > indent_level:
            close_list_item()
            _, ltype = list_stack.pop()
            output_lines.append(f"</{ltype}>")

    def detect_list_item(line: str) -> Optional[Tuple[int, str, str]]:
        spaces = 0
        for ch in line:
            if ch == " ":
                spaces += 1
            else:
                break
        content_after_spaces = line[spaces:]

        if re.match(r"^[-\*\+]\s", content_after_spaces):
            return spaces, "ul", content_after_spaces[2:]
        elif re.match(r"^\d+\.\s", content_after_spaces):
            m = re.match(r"^\d+\.\s+(.*)", content_after_spaces)
            if m:
                return spaces, "ol", m.group(1)
        return None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("<h"):
            close_paragraph()
            close_all_lists()
            output_lines.append(line)
            continue

        if not stripped:
            if in_list_item:
                close_paragraph()
            else:
                close_paragraph()
            continue

        list_item_info = detect_list_item(line)
        if list_item_info is not None:
            current_indent, list_type, list_content = list_item_info

            if not list_stack:
                close_paragraph()
                output_lines.append(f"<{list_type}>")
                list_stack.append((current_indent, list_type))
                start_list_item()
            else:
                if current_indent > list_stack[-1][0]:
                    close_paragraph()
                    output_lines.append(f"<{list_type}>")
                    list_stack.append((current_indent, list_type))
                    start_list_item()
                else:
                    close_lists_down_to(current_indent)
                    if list_stack and list_stack[-1][1] != list_type:
                        close_list_item()
                        _, old_type = list_stack.pop()
                        output_lines.append(f"</{old_type}>")
                        output_lines.append(f"<{list_type}>")
                        list_stack.append((current_indent, list_type))
                        start_list_item()
                    else:
                        start_list_item()

            if list_content.strip():
                start_paragraph()
                current_paragraph_chunks.append(list_content.strip())
        else:
            if list_stack:
                if not in_list_item:
                    close_all_lists()
                    start_paragraph()
                    current_paragraph_chunks.append(stripped)
                else:
                    if not in_paragraph:
                        start_paragraph()
                    else:
                        current_paragraph_chunks.append(" ")
                    current_paragraph_chunks.append(stripped)
            else:
                if not in_paragraph:
                    start_paragraph()
                else:
                    current_paragraph_chunks.append(" ")
                current_paragraph_chunks.append(stripped)

    close_paragraph()
    close_all_lists()

    return "\n".join(output_lines)
