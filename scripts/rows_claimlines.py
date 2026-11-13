"""Rows behind nv12: the attribution lines of the eleven New York Times news reports, filed under a fixed list of claims
by two reader lanes (research/claims_lines.tsv, written by claims_merge.py). The attribution passage itself is already a
row (TA####, rows_sourcing.py); each row here carries the statement a reader copied from the article for that line,
which the checker matches to the saved article. Which claim a line belongs to, its stance and its basis are the readers'
judgments; a line is counted under a value only where both readers give it."""
import csv
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'
CLAIMS = [('spy', 'She worked for Chinese intelligence'),
          ('relationship', 'Huang and she had a romantic or intimate relationship'),
          ('huang_knowledge', 'Huang knew what she was, or secrets were compromised'),
          ('collection', 'The surveillance and the memo themselves'),
          ('who_was_told', 'Who in government was warned, and when'),
          ('trump_stance', 'What Trump said and did about Huang afterwards'),
          ('export_enforcement', 'How the government handled chip exports and enforcement'),
          ('megaspeed', 'Megaspeed\'s business and whether it moved chips to China'),
          ('other_buyers', 'Other buyers cleared to receive chips'),
          ('congress', 'What members of Congress asked and said'),
          ('company_response', 'What Nvidia and its board said and did'),
          ('second_relationship', 'A relationship with an Nvidia executive'),
          ('huang_china_policy', 'Huang\'s position on China sales and his dealings with the administration'),
          ('her_background', 'Her biography and career'),
          ('markets_industry', 'Markets and the industry'),
          ('whole_account', 'What the article as a whole is based on'),
          ('other_background', 'Other background')]


# What the first report (Oct 29) says about its own sourcing: passages chosen for the figure, each matched to the saved article.
FIRST = 'man-nyt-1029-01'
FIRST_REPORT = [('What the account is based on', 'This account is based on interviews with people briefed on the surveillance, who spoke on the condition of anonymity because the findings are drawn from classified intelligence, as well as other officials and industry executives and analysts.'),
                ('Which agency', 'It could not be determined which intelligence agency or agencies have been involved in monitoring Ms. Huang, or what prompted them to start.'),
                ('What she is said to have passed on', 'It is also not clear under what circumstances Ms. Huang began gathering information for Beijing, what information she passed along or its value to China.'),
                ('The agencies, asked', 'The White House, the C.I.A. and the National Security Agency all declined to comment.')]
PROP = ('spy', 'relationship', 'huang_knowledge', 'who_was_told')     # claims that can be stated or denied


def mode(r):
    """For a says-so line under a statable claim: 'states' or 'comments' where both readers agree, 'split' where they differ,
    'unread' if either has not answered; None for every other line (the question was not asked of it)."""
    if not r.get('mode_asked'):
        return None
    a, b = r.get('mode_a', ''), r.get('mode_b', '')
    if not a or not b:
        return 'unread'
    return a if a == b else 'split'


def lines():
    p = R / 'claims_lines.tsv'
    return list(csv.DictReader(open(p, newline=''), delimiter='\t')) if p.exists() else []


def agreed(r, field):
    """The value both readers give for a field, else ''."""
    a, b = r[field + '_a'], r[field + '_b']
    return a if a and a == b else ''


def rows():
    out = [{'row_id': f'TQ{i:02d}', 'page': FIRST, 'src': FIRST, 'q': q} for i, (_, q) in enumerate(FIRST_REPORT, 1)]
    for r in lines():
        # the table's own copies of the attribution passage and of the words for the source: the figure draws from these cells,
        # so they are checked against the article as well
        out.append({'row_id': 'TK' + r['key'][2:], 'page': r['page'], 'src': r['page'], 'q': r['quote']})
        out.append({'row_id': 'TW' + r['key'][2:], 'page': r['page'], 'src': r['page'], 'q': r['source']})
        q = r['statement_a'] or r['statement_b']
        if q:
            out.append({'row_id': 'TC' + r['key'][2:], 'page': r['page'], 'src': r['page'], 'q': q})
        if r.get('mode_statement'):
            out.append({'row_id': 'TM' + r['key'][2:], 'page': r['page'], 'src': r['page'], 'q': r['mode_statement']})
    return out
