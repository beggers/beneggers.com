import pytest

from beneggerscom.ssg.input_files.layout import LayoutFile
from beneggerscom.ssg.page import Page


def test_render_partials_no_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_partials({})
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_partials_one_partial(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split("\n")
    partial = """
{% define partial %}
<html>
{% end partial %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_partials({"partial": partial_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>"


def test_render_partials_multiple_sibling_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
{% include partial2 %}
""".strip().split("\n")
    partial = """
{% define partial %}
<html>
{% end partial %}
""".strip().split("\n")
    partial2 = """
{% define partial2 %}
<body>
{% end partial2 %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    partial2_file = LayoutFile.from_lines("", partial2)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_partials({"partial": partial_file, "partial2": partial2_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>\n<body>"


def test_render_partials_nested_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split("\n")
    partial = """
{% define partial %}
<html>
{% include partial2 %}
{% end partial %}
""".strip().split("\n")
    partial2 = """
{% define partial2 %}
<body>
{% end partial2 %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    partial2_file = LayoutFile.from_lines("", partial2)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_partials({"partial": partial_file, "partial2": partial2_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>\n<body>"


def test_render_partials_missing_partial(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    with pytest.raises(ValueError) as e:
        page._render_partials({})
    assert str(e.value) == "Partial 'partial' not found."


def test_render_ifs_no_if(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.page = page
    page._render_ifs(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_ifs_one_true_if(valid_md_file, base_eval_context):
    layout = """
{% if page.title %}
<!DOCTYPE html>
{% end if %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.page = page
    page._render_ifs(base_eval_context)
    assert "".join(page._rendered_content.split("\n")) == "<!DOCTYPE html>"


def test_render_ifs_one_false_if(valid_md_file, base_eval_context):
    layout = """
{% if page %}
<!DOCTYPE html>
{% end if %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.page = None
    page._render_ifs(base_eval_context)
    assert page._rendered_content == ""


def test_render_ifs_one_true_one_false(valid_md_file, base_eval_context):
    layout = """
{% if page %}
<!DOCTYPE html>
{% end if %}
{% if page.title is None %}
<p>Something</p>
{% end if %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.page = page
    page._render_ifs(base_eval_context)
    assert "".join(page._rendered_content.split("\n")) == "<!DOCTYPE html>"


def test_render_loops_no_loops(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_loops(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_loops_raises_if_no_end(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{{ page.title }}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    with pytest.raises(ValueError):
        page._render_loops(base_eval_context)


def test_render_loops_empty_loop(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{% page.title %}
{% end for %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_loops(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>\n"


def test_render_loops_single_loop(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{% page.title %}
{% end for %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.pages = [page, page, page]
    page._render_loops(base_eval_context)
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>TestTestTest"
    )


def test_render_loop_with_if_statement(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for i in sorted([p for p in pages if p.nav != -1], key=lambda p: p.nav) %}
{% i.nav %}
{% end for %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page1 = Page(valid_md_file, layout_file, "", "", "")
    page2 = Page(valid_md_file, layout_file, "", "", "")
    page3 = Page(valid_md_file, layout_file, "", "", "")
    page1.nav = 1
    page2.nav = 2
    page3.nav = 3
    pages = [page1, page2, page3]
    base_eval_context.pages = pages
    page1._render_loops(base_eval_context)
    assert "".join(page1._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>123"
    )


def test_render_variables_no_variables(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._render_variables(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_variables_single_variable(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% page.title %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.page = page
    page._render_variables(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>\nTest"


def test_render_variables_multiple_variables(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% page.title %}
{% page.date %}
{% base_url %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    valid_md_file.date = "2021-01-01"

    page = Page(valid_md_file, layout_file, "", "", "")
    base_eval_context.base_url = "localhost"
    base_eval_context.page = page

    page._render_variables(base_eval_context)
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>Test2021-01-01localhost"
    )


def test_render_for_loop_in_if(valid_md_file):
    layout = """
<!DOCTYPE html>
{% if page %}
{% for page in pages %}
{% page.title %}
{% end for %}
{% end if %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page.render("localhost", "http", {}, [page, page, page], "")
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>TestTestTest"
    )


def test_render_if_in_for_loop(valid_md_file):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{% if page %}
{% page.title %}
{% end if %}
{% if page is None %}
SHOULD NOT APPEAR
{% end if %}
{% end for %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page.render("localhost", "http", {}, [page, page, page], "")
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>TestTestTest"
    )


def test_render_with_all(valid_md_file):
    layout = """
<!DOCTYPE html>
{% page.title %}
{% for page in pages %}
{% page.title %}
{% end for %}
{% base_url %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    valid_md_file.date = "2021-01-01"
    page = Page(valid_md_file, layout_file, "", "", "")
    page.render("localhost", "http", {}, [page, page, page], "")
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<!DOCTYPE html>TestTestTestTestlocalhost"
    )


def test_render_includes_markdown_as_html(valid_md_file):
    layout = """
{% slot %}
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page.render("localhost", "http", {}, [page], "")
    assert "".join(page._rendered_content.split("\n")) == "".join(
        "<p>Here's a paragraph</p>"
    )


def test_markdown_can_expand_template_variables_in_links(valid_md_file):
    # The markdown content will contain a link that includes template variables
    valid_md_file.content = (
        "Link to "
        + "[Local]({% protocol %}://non-breaking-spaces."
        + "technical-bites.{% base_url %})"
    )
    layout = """
    {% slot %}
    """.strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    # Render with known base_url/protocol
    page.render("localhost:8099", "http", {}, [page], "")
    html = "".join(page._rendered_content.split("\n"))
    # Avoid linter long line by joining parts
    expected_href = (
        'href="http://non-breaking-spaces.' + 'technical-bites.localhost:8099"'
    )
    assert expected_href in html


def test_flush(valid_md_file, tmp_path):
    layout = """
<!DOCTYPE html>
""".strip().split("\n")
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "", "", "")
    page._path = tmp_path / "index.html"
    page.flush()
    with open(tmp_path / "index.html", "r") as f:
        assert f.read() == "<!DOCTYPE html>"
