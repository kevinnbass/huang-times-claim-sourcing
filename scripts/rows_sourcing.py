"""Rows behind nv11: how the saved pages attribute what they report.
Two tables, written by sourcing_merge.py from reader lanes whose every line was matched to the page text by script:
  research/sourcing_times_a.tsv  one row per attribution in the 13 New York Times articles saved by hand (reading A, the one
                                 drawn; reading B is kept beside it as a check)
  research/sourcing_pages.tsv    one row per unnamed-source description or credit to another outlet on the wider set of saved pages (not in this copy)
Each line is a row here: the page and the passage that carries the attribution. What kind of source a passage names is
the reader's judgment and has not been audited; that the passage is in the page has been checked."""
import csv
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'
# the 13 articles in the order drawn: (page id, date, short title, set)
TIMES = [('man-nyt-1029-01', '2026-10-29', 'Nvidia chief is seen as target of Chinese spy plot', 'news'),
         ('man-nyt-1105-01', '2026-11-05', 'House G.O.P. leaders ask Huang to a closed-door briefing', 'news'),
         ('man-nyt-1106-01', '2026-11-06', 'China\'s top spy agency recruited the woman', 'news'),
         ('man-nyt-1107-01', '2026-11-07', 'U.S. cleared Nvidia chips to Chinese firms with empty offices', 'news'),
         ('man-nyt-1108-01', '2026-11-08', 'Nvidia opens investigation into Huang\'s relationship', 'news'),
         ('man-nyt-1108-02', '2026-11-08', 'Rubio warned officials about the entanglement', 'news'),
         ('man-nyt-1109-01', '2026-11-09', 'Huang told Trump he did not know she was a suspected spy', 'news'),
         ('man-nyt-1110-02', '2026-11-10', 'Despite denial, Trump was told on the trip to China', 'news'),
         ('man-e1161e38dc19', '2026-11-11', 'Huang said to have had a relationship with an Nvidia executive', 'news'),
         ('man-nyt-1111-02', '2026-11-11', 'Trump officials clashed over Megaspeed', 'news'),
         ('man-nyt-1112-07', '2026-11-12', 'Huang resigns from Nvidia', 'news'),
         ('man-nyt-1110-01', '2026-11-10', 'With its giant I.P.O., Anthropic ties itself closer to Nvidia', 'offering'),
         ('man-nyt-1111-01', '2026-11-11', 'DealBook: Anthropic\'s I.P.O. and the clubby business of A.I.', 'offering')]


def table(name):
    p = R / name
    return list(csv.DictReader(open(p, newline=''), delimiter='\t')) if p.exists() else []


def times(reading='a'):
    return table(f'sourcing_times_{reading}.tsv')


def pages():
    return table('sourcing_pages.tsv')


def by_page():
    return table('sourcing_by_page.tsv')


def rows():
    out = []
    for i, r in enumerate(times('a'), 1):
        out.append({'row_id': r.get('row_id') or f'TA{i:04d}', 'page': r['page'], 'source_type': r['source_type'], 'topic': r['topic'], 'src': r['page'], 'q': r['quote']})
    for r in pages():
        out.append({'row_id': r['key'], 'page': r['page'], 'role': r['role'], 'src': r['page'], 'q': r['quote']})
    return out
