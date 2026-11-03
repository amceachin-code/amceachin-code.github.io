"""
Tests for the hand-made Students & Guardians tools page and its menu entry.

The page links to tools that live in their own repos and are served by
GitHub Pages: the grades guide under this domain, the math worksheets and
Times Tables Games at their own hearthandwit.com addresses since November
2026. These tests guard the pieces that connect them: the page must survive
sync_hugo.py, appear in the menu, and link to each tool at its address.

Run with: python -m pytest tests/
"""

from pathlib import Path

import yaml

SITE = Path(__file__).resolve().parent.parent / "site"
TOOLS_DIR = SITE / "content" / "tools"
MENUS = SITE / "config" / "_default" / "menus.yaml"


def test_tools_page_is_hand_made():
    # sync_hugo.py deletes any content folder holding a .generated marker,
    # so this folder must never have one.
    assert (TOOLS_DIR / "_index.md").exists()
    assert not (TOOLS_DIR / ".generated").exists()


def test_menu_links_to_tools_page():
    menu = yaml.safe_load(MENUS.read_text())["main"]
    entry = next(m for m in menu if m["url"] == "/tools/")
    assert entry["name"] == "Students & Guardians"


WORKSHEETS = "https://worksheets.hearthandwit.com/"
GAMES = "https://timestables.hearthandwit.com/"


def test_page_links_each_tool_at_its_address():
    text = (TOOLS_DIR / "_index.md").read_text()
    assert "](/grade-inflation/)" in text
    assert f"]({WORKSHEETS})" in text
    assert f"]({GAMES})" in text
    # The apps moved off this domain; nothing may still point at their old paths.
    assert "/multiplication-worksheet/" not in text.replace("github.com/amceachin-code/multiplication-worksheet", "")
    assert "/times-tables-games/" not in text
    # Only the worksheets show their repo; grade-inflation links to the tool alone.
    assert "https://github.com/amceachin-code/multiplication-worksheet" in text
    assert "https://github.com/amceachin-code/grade-inflation" not in text


def test_page_links_division_worksheet():
    # The division tool lives in a subfolder of the multiplication-worksheet repo.
    text = (TOOLS_DIR / "_index.md").read_text()
    assert f"]({WORKSHEETS}division/)" in text


def test_page_links_color_by_number_under_math_worksheets():
    # Color by Number lives in a subfolder of the multiplication-worksheet repo
    # too, and belongs with the other worksheets.
    text = (TOOLS_DIR / "_index.md").read_text()
    section = text.split("## Math Worksheets", 1)[1].split("\n## ", 1)[0]
    assert f"]({WORKSHEETS}color-by-number/)" in section


def test_games_links_name_its_privacy_and_accessibility_pages():
    text = (TOOLS_DIR / "_index.md").read_text()
    assert f"]({GAMES}privacy/)" in text
    assert f"]({GAMES}accessibility/)" in text
