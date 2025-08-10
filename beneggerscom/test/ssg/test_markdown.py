from beneggerscom.ssg.markdown import (
    _process_bolds,
    _process_headings,
    _process_italics,
    _process_links,
    _process_paragraphs_and_lists,
    str_to_html,
)


def _assert_equals_ignore_whitespace(a: str, b: str) -> None:
    assert "".join(a.split()) == "".join(b.split())


# Re-enable the full historical tests; keep everything active unless superseded
def test_process_headings_no_headings():
    assert _process_headings("No headings here") == "No headings here"


def test_process_headings_one_heading_one():
    assert _process_headings("# Heading 1") == "<h1>Heading 1</h1>"


def test_process_headings_one_heading_two():
    assert _process_headings("## Heading 2") == "<h2>Heading 2</h2>"


def test_process_headings_one_heading_three():
    assert _process_headings("### Heading 3") == "<h3>Heading 3</h3>"


def test_process_headings_one_heading_four():
    assert _process_headings("#### Heading 4") == "<h4>Heading 4</h4>"


def test_process_headings_one_heading_five():
    assert _process_headings("##### Heading 5") == "<h5>Heading 5</h5>"


def test_process_one_heading_plus_text():
    text = """
# Heading 1
Some text
"""
    expected = """
<h1>Heading 1</h1>
Some text
"""
    assert _process_headings(text) == expected


def test_process_one_heading_after_text():
    text = """
Some text
# Heading 1
"""
    expected = """
Some text
<h1>Heading 1</h1>
"""
    assert _process_headings(text) == expected


def test_process_headings_multiple_headings():
    text = """
# Heading 1

Text

## Heading 2

More text

### Heading 3
"""
    expected = """
<h1>Heading 1</h1>

Text

<h2>Heading 2</h2>

More text

<h3>Heading 3</h3>
"""
    assert _process_headings(text) == expected


def test_bold_no_bold():
    assert _process_bolds("No bold here") == "No bold here"


def test_bold_asterisks_one_bold():
    assert _process_bolds("**Bold text**") == "<strong>Bold text</strong>"


def test_bold_asterisks_one_bold_plus_text():
    text = """
**Bold text**
Non-bold text
"""
    expected = """
<strong>Bold text</strong>
Non-bold text
"""
    assert _process_bolds(text) == expected


def test_bold_asterisks_one_bold_after_text():
    text = """
Non-bold text
**Bold text**
"""
    expected = """
Non-bold text
<strong>Bold text</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_asterisks_multiple_bold():
    text = """
**Bold 1**
Non-bold text
**Bold 2**
"""
    expected = """
<strong>Bold 1</strong>
Non-bold text
<strong>Bold 2</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_one_bold():
    assert _process_bolds("__Bold text__") == "<strong>Bold text</strong>"


def test_bold_underscores_one_bold_plus_text():
    text = """
__Bold text__
Non-bold text
"""
    expected = """
<strong>Bold text</strong>
Non-bold text
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_one_bold_after_text():
    text = """
Non-bold text
__Bold text__
"""
    expected = """
Non-bold text
<strong>Bold text</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_multiple_bold():
    text = """
__Bold 1__
Non-bold text
__Bold 2__
"""
    expected = """
<strong>Bold 1</strong>
Non-bold text
<strong>Bold 2</strong>
"""
    assert _process_bolds(text) == expected


def test_italics_no_italics():
    assert _process_italics("No italics here") == "No italics here"


def test_italics_asterisks_one_italics():
    assert _process_italics("*Italic text*") == "<em>Italic text</em>"


def test_italics_asterisks_one_italics_plus_text():
    text = """
*Italic text*
Non-italic text
"""
    expected = """
<em>Italic text</em>
Non-italic text
"""
    assert _process_italics(text) == expected


def test_italics_asterisks_one_italics_after_text():
    text = """
Non-italic text
*Italic text*
"""
    expected = """
Non-italic text
<em>Italic text</em>
"""
    assert _process_italics(text) == expected


def test_italics_asterisks_multiple_italics():
    text = """
*Italic 1*
Non-italic text
*Italic 2*
"""
    expected = """
<em>Italic 1</em>
Non-italic text
<em>Italic 2</em>
"""
    assert _process_italics(text) == expected


def test_italics_underscores_one_italics():
    assert _process_italics("_Italic text_") == "<em>Italic text</em>"


def test_italics_underscores_one_italics_plus_text():
    text = """
_Italic text_
Non-italic text
"""
    expected = """
<em>Italic text</em>
Non-italic text
"""
    assert _process_italics(text) == expected


def test_italics_underscores_one_italics_after_text():
    text = """
Non-italic text
_Italic text_
"""
    expected = """
Non-italic text
<em>Italic text</em>
"""
    assert _process_italics(text) == expected


def test_italics_underscores_multiple_italics():
    text = """
_Italic 1_
Non-italic text
_Italic 2_
"""
    expected = """
<em>Italic 1</em>
Non-italic text
<em>Italic 2</em>
"""
    assert _process_italics(text) == expected


def test_links_no_links():
    assert _process_links("No links here") == "No links here"


def test_links_one_link():
    assert (
        _process_links("[Link](https://example.com)")
        == '<a href="https://example.com">Link</a>'
    )


def test_links_one_link_plus_text():
    text = """
[Link](https://example.com)
Non-link text
"""
    expected = """
<a href="https://example.com">Link</a>
Non-link text
"""
    assert _process_links(text) == expected


def test_links_one_link_after_text():
    text = """
Non-link text
[Link](https://example.com)
"""
    expected = """
Non-link text
<a href="https://example.com">Link</a>
"""
    assert _process_links(text) == expected


def test_links_multiple_links():
    text = """
[Link 1](https://example.com)
Non-link text
[Link 2](https://example.com)
"""
    expected = """
<a href="https://example.com">Link 1</a>
Non-link text
<a href="https://example.com">Link 2</a>
"""
    assert _process_links(text) == expected


def test_links_inline_in_sentence():
    text = "This [Link](https://example.com) is cool"
    expected = 'This <a href="https://example.com">Link</a> is cool'
    assert _process_links(text) == expected


def test_links_multiple_in_one_line():
    text = "Two [A](https://a.example) and [B](https://b.example) here."
    expected = (
        'Two <a href="https://a.example">A</a> and '
        '<a href="https://b.example">B</a> here.'
    )
    assert _process_links(text) == expected


def test_links_parentheses_in_url():
    # Desired behavior: allow parentheses in URLs
    text = "[with (parens)](https://example.com/a(b)c)"
    expected = '<a href="https://example.com/a(b)c">with (parens)</a>'
    assert _process_links(text) == expected


def test_links_mailto_scheme():
    text = "Email [me](mailto:me@example.com) please."
    expected = 'Email <a href="mailto:me@example.com">me</a> please.'
    assert _process_links(text) == expected


def test_links_integration_with_bold():
    md = "Para [link](x) with **bold**"
    expected = '<p>Para <a href="x">link</a> with <strong>bold</strong></p>'
    _assert_equals_ignore_whitespace(str_to_html(md), expected)


def test_paragraphs_single_line():
    text = "Just a single line of text"
    expected = "<p>Just a single line of text</p>"
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_paragraphs_multiple_paragraphs():
    text = """Line one
Line two

Line three

Line four and five
Line five continued"""
    expected = """<p>Line one Line two</p>
<p>Line three</p>
<p>Line four and five Line five continued</p>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_unordered_list_simple():
    text = """- Item one
- Item two
- Item three"""
    expected = """<ul>
<li><p>Item one</p></li>
<li><p>Item two</p></li>
<li><p>Item three</p></li>
</ul>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_nested_unordered_list():
    text = """
- Item one
    - Nested item one
    - Nested item two
- Item two"""
    expected = """
<ul>
    <li>
        <p>Item one</p>
        <ul>
            <li><p>Nested item one</p></li>
            <li><p>Nested item two</p></li>
        </ul>
    </li>
    <li>
        <p>Item two</p>
    </li>
</ul>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_ordered_list_simple():
    text = """1. First item
2. Second item
3. Third item"""
    expected = """<ol>
<li><p>First item</p></li>
<li><p>Second item</p></li>
<li><p>Third item</p></li>
</ol>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_unordered_list_multiple_paragraphs_in_item():
    text = """- First item line one

  First item line two

  First item line three
- Second item"""
    expected = """<ul>
<li><p>First item line one</p>
<p>First item line two</p>
<p>First item line three</p></li>
<li><p>Second item</p></li>
</ul>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_paragraphs_multiple_lines_one_paragraph():
    text = """Line one
Line two
Line three"""
    expected = "<p>Line one Line two Line three</p>"
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


# End of re-enabled historical tests
def test_footnote_single_in_paragraph():
    md = """
This is a sentence with a footnote[^1].

[^1]: This is the footnote.
""".strip()
    html = str_to_html(md)
    expected = (
        '<div class="para-with-footnote">'
        '<p>This is a sentence with a footnote<sup class="fn-ref">1</sup>.</p>'
        '<aside class="footnote">'
        "<ol><li>This is the footnote.</li></ol></aside>"
        "</div>"
    )
    _assert_equals_ignore_whitespace(html, expected)


def test_footnote_multiple_refs_in_one_paragraph():
    md = """
Text with two refs[^a] and again[^a] plus another[^b].

[^a]: First footnote body.
[^b]: Second footnote body.
""".strip()
    html = str_to_html(md)
    # The paragraph should have numbered refs in order of first appearance:
    # a=1, b=2
    assert html.count('<sup class="fn-ref">1</sup>') == 2
    assert html.count('<sup class="fn-ref">2</sup>') == 1
    assert "First footnote body." in html
    assert "Second footnote body." in html


def test_footnote_in_list_item():
    md = """
- List item with footnote[^x]

[^x]: Footnote in list item.
""".strip()
    html = str_to_html(md)
    # Ensure wrapper is inside the list item
    assert "<ul>" in html and "</ul>" in html
    li_start = html.find("<li>")
    wrapper_pos = html.find('<div class="para-with-footnote">')
    assert li_start != -1 and wrapper_pos != -1 and wrapper_pos > li_start


def test_ordered_list_multiple_paragraphs_in_item():
    text = """1. This is the first paragraph of the first item.

   This is the second paragraph of the first item.
2. Second item"""
    expected = """<ol>
<li><p>This is the first paragraph of the first item.</p>
<p>This is the second paragraph of the first item.</p></li>
<li><p>Second item</p></li>
</ol>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_outside_paragraph_and_list():
    text = """
Outside paragraph line one
Outside paragraph line two

- List item one
- List item two

Outside paragraph again"""
    expected = """
<p>Outside paragraph line one Outside paragraph line two</p>
    <ul>
        <li><p>List item one</p></li>
    <li><p>List item two</p></li>
</ul>
<p>Outside paragraph again</p>"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_deep_nested_unordered_list_and_dedent():
    text = """
- A
    - B1
        - C1
    - B2
- D

Outside paragraph
""".strip()
    expected = """
<ul>
    <li>
        <p>A</p>
        <ul>
            <li>
                <p>B1</p>
                <ul>
                    <li><p>C1</p></li>
                </ul>
            </li>
            <li><p>B2</p></li>
        </ul>
    </li>
    <li><p>D</p></li>
</ul>
<p>Outside paragraph</p>
"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_continuation_line_inside_list_item():
    text = """
- First line of item
Second line continues
Third line continues too
""".strip()
    expected = """
<ul>
    <li><p>First line of item Second line continues
Third line continues too</p></li>
</ul>
"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )


def test_mixed_bullets_same_list():
    text = """
- Dash item
* Star item
+ Plus item
""".strip()
    expected = """
<ul>
    <li><p>Dash item</p></li>
    <li><p>Star item</p></li>
    <li><p>Plus item</p></li>
</ul>
"""
    _assert_equals_ignore_whitespace(
        _process_paragraphs_and_lists(text), expected
    )
