"""
Tests for the journal article numbering in the CV template.

Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from build_cv import render_cv
from utils import filter_pubs_by_type, load_all_data


def test_journal_articles_count_down_from_total():
    """With N articles, item k is labeled (N + 1 - k), so the first item is N."""
    # The template needs the full data set (profile, etc.), so render the real CV.
    data = load_all_data()
    pubs = data["publications"]["publications"]
    n = len(filter_pubs_by_type(pubs, "journal"))
    tex = render_cv(data)

    section = tex.split(r"\section{Peer-Reviewed Journal Articles}", 1)[1]
    assert rf"\renewcommand*{{\revtotal}}{{{n}}}" in section
    begin = next(l for l in section.splitlines() if l.startswith(r"\begin{enumerate}"))
    assert r"label=\revarabic*." in begin


def test_alphabetical_flag_marks_journal_authors():
    """Flagged articles get a leading # and the key appears under the heading."""
    data = load_all_data()
    tex = render_cv(data)
    section = tex.split(r"\section{Peer-Reviewed Journal Articles}", 1)[1].split(r"\end{enumerate}", 1)[0]
    assert r"\# = Alphabetical authorship" in section

    pubs = filter_pubs_by_type(data["publications"]["publications"], "journal")
    items = [l for l in section.splitlines() if l.lstrip().startswith(r"\item")]
    flagged = sum(1 for p in pubs if p.get("alphabetical"))
    assert sum(1 for l in items if l.lstrip().startswith(r"\item \#")) == flagged
