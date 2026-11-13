"""nv12: what each claim in the New York Times's eleven news reports rests on.
Every attribution line of those reports (the 345 of reading A, each already matched to the article) was filed by two reader
lanes under one of seventeen claims, with a stance (says so, disputes, declined to comment) and a basis (who or what the
article has it from at that place). A line counts under a value only where both readers give that value; the rest is drawn
grey as "the two readers differ". Band 1: all eleven reports, one row per claim. Band 2: one panel per report.
The figure counts how claims are attributed. It does not say whether any claim is true."""
import re
from collections import Counter, defaultdict

import rows_claimlines as C, rows_sourcing as S
from fig_common import *

PAGE = 3000
WARM = '#d95a2b'; BLUE_ = '#2a78d6'; GREEN_ = '#178f66'; OCHRE = '#c98a00'; PURPLE = '#7b5cd6'; DIFF = '#cbc7ba'
# basis -> (colour, style, label). Warm = nobody on the record at that place and no record the paper says it holds.
BASIS = [('unnamed_people', WARM, 'solid', 'Unnamed people or officials'),
         ('institution_conclusion', WARM, 'hollow', 'An agency\'s conclusion, with no one quoted for it'),
         ('material_described', WARM, 'dot', 'Intelligence or a memo the article relays'),
         ('named_on_record', BLUE_, 'solid', 'A named person'),
         ('institution_on_record', GREEN_, 'solid', 'A company or agency on the record'),
         ('record_available', OCHRE, 'solid', 'A record the paper holds, or its own check'),
         ('earlier_report', PURPLE, 'solid', 'An earlier news report'),
         ('', DIFF, 'solid', 'The two readers differ')]
STYLE = {b: (c, s) for b, c, s, _ in BASIS}; BLABEL = {b: l for b, _, _, l in BASIS}; BORDER = [b for b, _, _, _ in BASIS]
OFF = ('unnamed_people', 'institution_conclusion', 'material_described')
SHORT = {'spy': 'She worked for Chinese intelligence', 'relationship': 'The relationship with Huang', 'huang_knowledge': 'What Huang knew; whether secrets leaked',
         'collection': 'The surveillance and the memo', 'who_was_told': 'Who in government was told', 'trump_stance': 'Trump on Huang afterwards',
         'export_enforcement': 'Chip exports and enforcement', 'megaspeed': 'Megaspeed and its chips', 'other_buyers': 'Other chip buyers', 'congress': 'Congress',
         'company_response': 'Nvidia and its board', 'second_relationship': 'A relationship with an Nvidia executive', 'huang_china_policy': 'Huang on China sales; the administration',
         'her_background': 'Her biography', 'markets_industry': 'Markets and the industry', 'whole_account': 'Basis of the whole article', 'other_background': 'Other background'}
LINT = re.compile(r'\b(?:EV|OP|CL|BN|TI|AC|RU|ST|AP|MA|MT|TA|TC|TK|TM|TW|TQ|SP)\d{2,5}\b|[\w/-]+\.(?:csv|json|jsonl|py|tsv|html|pdf)\b|research/|scripts/')


def bold_source(passage, source):
    """The passage with the article's words for the source set in bold where they occur in it."""
    i = passage.find(source)
    if i < 0 and source[:1].isupper():
        i = passage.find(source[:1].lower() + source[1:]); source = source[:1].lower() + source[1:] if i >= 0 else source
    if i < 0:
        return f'<b>{esc(source)}</b> <span style="color:{MUTED}">·</span> {esc(passage)}'
    return f'{esc(passage[:i])}<b>{esc(source)}</b>{esc(passage[i + len(source):])}'


def basis_of(r):
    if r.get('_grey'):
        return ''
    b = C.agreed(r, 'basis')
    return 'record_available' if b == 'paper_observation' else b      # the paper's own check is drawn with the records it holds


def mark(x, y, r, size=14):
    c, s = STYLE[basis_of(r)]
    tip = LINT.sub('…', f'{BLABEL[basis_of(r)]}: {r["source"]}: {r["statement_a"] or r["statement_b"] or r["quote"]}')
    t = f'<title>{esc(tip)}</title>'
    if s == 'solid':
        return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{c}">{t}</rect>'
    out = f'<rect x="{x + 1.3}" y="{y + 1.3}" width="{size - 2.6}" height="{size - 2.6}" rx="2.2" fill="{BG}" stroke="{c}" stroke-width="2.6">{t}</rect>'
    if s == 'dot':
        out += f'<rect x="{x + size / 2 - 2.6}" y="{y + size / 2 - 2.6}" width="5.2" height="5.2" fill="{c}"/>'
    return out


def block(lines, per_row, pitch=18, size=14):
    """Squares for one group of lines, ordered by basis so each kind forms one run."""
    ls = sorted(lines, key=lambda r: BORDER.index(basis_of(r)))
    if not ls:
        return ''
    rows_n = -(-len(ls) // per_row)
    w = min(len(ls), per_row) * pitch
    return (f'<svg width="{w}" height="{rows_n * pitch}" viewBox="0 0 {w} {rows_n * pitch}">'
            + ''.join(mark((i % per_row) * pitch, (i // per_row) * pitch + 1, r, size) for i, r in enumerate(ls)) + '</svg>')


def key_swatch(b):
    c, s = STYLE[b]
    inner = f'<rect x="1.5" y="1.5" width="15" height="15" rx="3" fill="{c}"/>' if s == 'solid' else (
        f'<rect x="2.8" y="2.8" width="12.4" height="12.4" rx="2.4" fill="{BG}" stroke="{c}" stroke-width="2.6"/>' + (f'<rect x="6.2" y="6.2" width="5.6" height="5.6" fill="{c}"/>' if s == 'dot' else ''))
    return f'<span><svg width="18" height="18" viewBox="0 0 18 18" style="display:inline-block">{inner}</svg>{esc(BLABEL[b])}</span>'


def fig_claimsources(KICKER, DRAFT, partial=False):
    L = C.lines(); art = {t[0]: t for t in S.TIMES}; news = [t[0] for t in S.TIMES if t[3] == 'news']
    assert len(L) == 345
    filed = [r for r in L if r['claim_a'] and r['claim_b']]
    if not partial:
        assert len(filed) == 345, ('lines not filed by both readers', 345 - len(filed))
    n = len(filed)
    ag = {f: sum(1 for r in filed if C.agreed(r, f)) for f in ('claim', 'stance', 'basis')}
    by_claim = defaultdict(list); differ = []
    for r in filed:
        (by_claim[C.agreed(r, 'claim')] if C.agreed(r, 'claim') else differ).append(r)

    def split(ls):
        """asserts = the source states the claim or gives the information; comments = it says something about a statable claim
        without stating it (both readers); differ = the readers split on the stance or on states-or-comments."""
        g = defaultdict(list)
        for r in ls:
            st_ = C.agreed(r, 'stance') or 'differ'; m = C.mode(r)
            if st_ == 'asserts' and m is not None:
                if m == 'comments':
                    st_ = 'comments'
                elif m != 'states':
                    assert partial or m == 'split', (m, r['key'])
                    st_ = 'differ'; r = dict(r, _grey=True)
            g[st_].append(r)
        return g

    def off(ls):
        return sum(1 for r in ls if basis_of(r) in OFF)

    css = (f'.h2{{font-size:25px;font-weight:bold;margin:0 0 4px}}.note{{font-size:16.5px;color:{MUTED};line-height:1.4;margin-bottom:10px;max-width:1900px}}.mut{{color:{MUTED}}}'
           f'.cr{{display:grid;grid-template-columns:500px 900px 250px 300px 190px 1fr;column-gap:18px;align-items:center;padding:7px 0;border-top:1px solid {GRID};font-size:16.5px}}'
           f'.ch{{font-size:13.5px;font-weight:bold;letter-spacing:1.4px;text-transform:uppercase;color:{MUTED}}}'
           f'.pn{{background:{CARD};border-radius:10px;padding:14px 16px 10px}}.pr{{display:grid;grid-template-columns:262px 296px 96px 110px 74px;column-gap:10px;align-items:center;padding:4px 0;border-top:1px solid {GRID};font-size:14.5px}}'
           f'.key{{display:flex;gap:24px;font-size:17px;flex-wrap:wrap;margin:0 0 12px}}.key span{{display:inline-flex;align-items:center;gap:8px}}')
    key = '<div class="key">' + ''.join(key_swatch(b) for b in BORDER) + '</div>'
    # ---------------------------------------------------------------- band 1: every report together, by claim
    b1 = (f'<div class="h2">All eleven reports: each claim, and where the articles say it comes from</div>'
          f'<div class="note">One square is one place where an article attributes a statement about that claim. Warm marks are places with nobody on the record and no record the paper says it holds: '
          f'unnamed people, a conclusion ascribed to an agency, or intelligence the article relays. Point at a square for the article\'s words.</div>' + key
          + f'<div class="cr" style="border-top:none;padding-bottom:2px"><div class="ch">Claim</div><div class="ch">Sources stating it, or giving the information</div><div class="ch">About it, without stating it</div>'
            f'<div class="ch">Sources disputing it</div><div class="ch">Declined to comment</div><div class="ch">Of those stating it</div></div>')
    stats = {}
    for k, label in C.CLAIMS:
        ls = by_claim.get(k, [])
        if not ls:
            continue
        g = split(ls); a = g['asserts']; o = off(a)
        on = sum(1 for r in a if basis_of(r) in ('named_on_record', 'institution_on_record', 'record_available'))
        stats[k] = {'n': len(ls), 'asserts': len(a), 'off': o, 'on': on, 'disputes': len(g['disputes']), 'declines': len(g['declines']), 'comments': g['comments'], 'split': len(g['differ']),
                    'named': sum(1 for r in a if basis_of(r) == 'named_on_record'), 'inst': sum(1 for r in a if basis_of(r) == 'institution_on_record'),
                    'unnamed': sum(1 for r in a if basis_of(r) == 'unnamed_people'), 'record': sum(1 for r in a if basis_of(r) == 'record_available'),
                    'earlier': [r for r in a if basis_of(r) == 'earlier_report'], 'named_lines': [r for r in a if basis_of(r) == 'named_on_record']}
        extra = f' <span class="mut" style="font-size:13.5px">+{len(g["differ"])} read two ways</span>' if g['differ'] else ''
        summ = (f'<b>{o} of {len(a)}</b> <span class="mut">with nobody on the record</span>' if a else '<span class="mut">none</span>')
        b1 += (f'<div class="cr"><div><b>{esc(label)}</b>{extra}</div><div>{block(a + g["differ"], 49)}</div><div>{block(g["comments"], 13)}</div><div>{block(g["disputes"], 16)}</div><div>{block(g["declines"], 10)}</div><div style="font-size:15.5px">{summ}</div></div>')
    if differ:
        b1 += (f'<div class="cr"><div class="mut"><b>Filed under different claims by the two readers</b></div><div>{block(differ, 49)}</div><div></div><div></div><div></div>'
               f'<div class="mut" style="font-size:15.5px">{len(differ)} of {n} lines; not counted under any claim</div></div>')
    # ---------------------------------------------------------------- band 1b: the spy claim, place by place
    g_spy = split(by_claim.get('spy', []))
    trace = sorted(g_spy['asserts'], key=lambda r: (art[r['page']][1], news.index(r['page']), int(r['n'])))
    # which sentence holds each place, whether it cites the paper's own earlier report, and whether the place names a U.S. agency
    # are script rules worked out from the saved articles when the table is built (claims_merge.py)
    assert partial or all(r['sentence_id'] for r in trace), 'an attribution passage was not found as one run in its article'
    restated = {r['key'] for r in trace if basis_of(r) == 'earlier_report' or r['in_times_sentence'] == 'yes'}
    n_sent = len({r['sentence_id'] for r in trace})
    named_agency = [r['key'] for r in trace if r['names_us_agency'] == 'yes']
    words = Counter(re.sub(r'^(?:the|a|an)\s+', '', r['source'].strip(), flags=re.I) for r in trace if basis_of(r) != 'earlier_report')
    cards = ''.join(f'<div style="background:{CARD};border-left:6px solid {AXIS};border-radius:8px;padding:10px 14px;margin-bottom:10px">'
                    f'<div class="ch" style="margin-bottom:4px">{esc(lab)}</div><div style="font-size:16.5px;line-height:1.38">“{esc(q)}”</div></div>' for lab, q in C.FIRST_REPORT)
    wl = ''.join(f'<div style="display:flex;justify-content:space-between;border-top:1px solid {GRID};padding:4px 0;font-size:15.5px"><span>“{esc(w)}”</span><b>{c}</b></div>' for w, c in words.most_common())
    def trow(r):
        bar = PURPLE if r['key'] in restated else 'transparent'
        mk = f'<svg width="16" height="16" viewBox="0 0 16 16" style="display:block">{mark(1, 1, r)}</svg>'
        return (f'<div style="display:grid;grid-template-columns:62px 20px 1fr;column-gap:8px;align-items:start;padding:5px 0 5px 8px;border-top:1px solid {GRID};border-left:5px solid {bar};break-inside:avoid;font-size:15px;line-height:1.34">'
                f'<div class="mut">{day(art[r["page"]][1])}</div><div style="padding-top:2px">{mk}</div><div>{bold_source(r["mode_statement"] or r["statement_a"] or r["quote"], r["source"])}</div></div>')
    b1 += (f'<div class="h2" style="margin-top:40px">The first claim, place by place: every time a report states that she worked for Chinese intelligence</div>'
           f'<div class="note">All {len(trace)} places, in order, in the articles\' own words, with the words for the source in bold. They sit in {n_sent} sentences: a sentence that cites both the paper\'s earlier report and the officials behind it is two places. '
           f'{"None names" if not named_agency else str(len(named_agency)) + " name"} a U.S. agency. A purple bar marks the {len(restated)} that sit in a sentence citing the paper\'s own earlier report.</div>'
           f'<div style="display:grid;grid-template-columns:820px 1fr;column-gap:50px;align-items:start">'
           f'<div><div style="font-size:19px;font-weight:bold;margin-bottom:8px">What the first report, on Oct 29, says about its own sourcing</div>{cards}'
           f'<div style="font-size:19px;font-weight:bold;margin:18px 0 6px">The words used for the source in the {sum(words.values())} places that are not the paper citing itself</div>{wl}</div>'
           f'<div style="column-count:2;column-gap:36px">{"".join(trow(r) for r in trace)}</div></div>')
    # ---------------------------------------------------------------- band 2: one panel per report
    b2 = (f'<div class="h2" style="margin-top:40px">Report by report</div>'
          f'<div class="note">The same squares, for each article in order. Columns in every panel: sources stating it or giving the information; about it without stating it; disputing it; declined to comment.</div>'
          f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start">')
    per = defaultdict(list)
    for r in filed:
        per[r['page']].append(r)
    for p in news:
        ls = per.get(p, [])
        if not ls and partial:
            continue
        _, date, title, _ = art[p]
        a_all = [r for r in ls if C.agreed(r, 'claim') and C.agreed(r, 'stance') == 'asserts' and C.mode(r) in (None, 'states')]
        b2 += (f'<div class="pn"><div style="font-size:17.5px;font-weight:bold;line-height:1.25">{day(date)} · {esc(title)}</div>'
               f'<div class="mut" style="font-size:14.5px;margin:3px 0 8px">{len(ls)} attributions; of {len(a_all)} stating a claim or giving information, {off(a_all)} with nobody on the record</div>')
        pc = defaultdict(list); pd = []
        for r in ls:
            (pc[C.agreed(r, 'claim')] if C.agreed(r, 'claim') else pd).append(r)
        for k, _ in C.CLAIMS:
            if k in pc:
                g = split(pc[k])
                b2 += (f'<div class="pr"><div>{esc(SHORT[k])}</div><div>{block(g["asserts"] + g["differ"], 16)}</div><div>{block(g["comments"], 5)}</div><div>{block(g["disputes"], 6)}</div><div>{block(g["declines"], 4)}</div></div>')
        if pd:
            b2 += f'<div class="pr"><div class="mut">Filed two ways</div><div>{block(pd, 16)}</div><div></div><div></div><div></div></div>'
        b2 += '</div>'
    b2 += '</div>'
    # ---------------------------------------------------------------- words
    return {'b1': b1, 'b2': b2, 'css': css, 'stats': stats, 'n': n, 'ag': ag, 'differ': len(differ), 'filed': filed,
            'restated': len(restated), 'named_agency': len(named_agency), 'trace': len(trace), 'n_sent': n_sent}


def draw(KICKER, DRAFT, partial=False):
    d = fig_claimsources(KICKER, DRAFT, partial); st = d['stats']; n = d['n']; ag = d['ag']
    spy = st['spy']; rel = st['relationship']; art = {t[0]: t for t in S.TIMES}
    tot_a = sum(v['asserts'] for v in st.values()); tot_off = sum(v['off'] for v in st.values())
    asked = [r for r in d['filed'] if C.mode(r) is not None]; m_ag = sum(1 for r in asked if C.mode(r) in ('states', 'comments'))
    n_comm = sum(len(v['comments']) for v in st.values())
    spy_comm = spy['comments']; spy_comm_named = sorted(r['source'] for r in spy_comm if basis_of(r) == 'named_on_record')
    # the sentences below are written from these counts; the build stops if the table stops supporting them
    assert spy['inst'] == 0 and spy['record'] == 0 and spy['named'] == 0, ('the title says no named person, agency on the record or held record states the spy claim', spy['named'], spy['inst'], spy['record'])
    assert all('Times' in r['source'] and 'Financial' not in r['source'] for r in spy['earlier'])
    assert spy_comm_named == ['Mr. Mattis', 'Representative Michael McCaul'], spy_comm_named
    assert spy['off'] + len(spy['earlier']) == spy['asserts'], (spy['off'], len(spy['earlier']), spy['asserts'])
    assert d['named_agency'] == 0 and d['trace'] == spy['asserts'], (d['named_agency'], d['trace'])
    assert any('could not be determined which intelligence agency or agencies' in q for _, q in C.FIRST_REPORT)
    assert all('Huang' in r['source'] or r['source'] == 'he' for r in rel['named_lines']) and min(art[r['page']][1] for r in rel['named_lines']) == '2026-11-08'
    title = (f'The Times\'s eleven reports state the spy claim {spy["asserts"]} times: {spy["off"]} with nobody on the record, {len(spy["earlier"])} citing the paper\'s own earlier reports, '
             f'none from a named person, an agency on the record or a record the paper holds')
    sub = (f'Every place the New York Times\'s eleven news reports on Huang say where a statement comes from, filed under the claim it is about and drawn by who or what the article has it from. '
           f'None of the {d["trace"]} places that state the woman worked for Chinese intelligence names a U.S. agency; the first report says it "could not be determined which intelligence agency or agencies" were involved, '
           f'and {d["restated"]} of the {d["trace"]} restate the paper\'s own earlier reports. The two named people quoted about it, a former C.I.A. analyst and a congressman, speak about it without stating it. '
           f'That the relationship was romantic is on the record from Nov 8, in Huang\'s own words ({rel["named"]} of the {rel["asserts"]} attributions stating it). A count of attribution. It does not say whether a claim is true.')
    foot = (f'<b>Reading it:</b> a square is one attribution, so a source cited five times for a claim is five squares; the figure shows how much of the text about a claim rests on each kind of source, not how many people there are. '
            f'"With nobody on the record" adds three kinds: people the article does not name; a conclusion the article ascribes to an agency without quoting anyone for it ("U.S. intelligence determined"); and intelligence or a memo whose contents the article relays without saying the paper saw it. '
            f'A denial is drawn under the claim it denies, in the disputing column. For the first four claims, which can be stated or denied, a source counts as stating the claim only if it is itself reported as saying, concluding or showing that the thing is so; '
            f'a general remark, a reaction to the reports, or a weaker statement is drawn in the next column and counted for nobody. For the relationship that column holds the lines reporting closeness or contact '
            f'(a "close relationship", photographs together, being in contact) without saying it was romantic or intimate. '
            f'<b>How it was made:</b> the {n} attributions are those the first reading found in the eleven reports, each matched to the article by script. Two further reader lanes (a different model family from the one that drew this) each filed every line under one of seventeen claims, '
            f'with a stance and a basis. The list of claims was written for this figure before the filing; another list would cut the lines differently. The two readers agree on the claim for {ag["claim"]} of {n} lines, on the stance for {ag["stance"]} and on the basis for {ag["basis"]}. '
            f'A third pass by two more readers put the stating-or-commenting question to all {len(asked)} lines filed as saying so under the first four claims, named and unnamed alike; they agree on {m_ag}, and both find that {n_comm} do not state the claim. '
            f'A line is counted under a value only where both readers agree; the rest is drawn grey. In the place-by-place list, the purple bar is a script rule, not a reader\'s judgment: the sentence holding the attribution contains "The Times reported" or the like, '
            f'or the line is itself such a citation; "names a U.S. agency" is a search of each place for agency names. The four passages from the first report were chosen for this figure. Across all claims, {tot_off} of the {tot_a} attributions stating a claim or giving the information have nobody on the record. '
            f'<b>What the record does not show:</b> who any unnamed source is, what documents the paper holds but does not describe, or whether any claim is true. A claim attributed only to unnamed sources is not thereby false, and one on the record is not thereby true. '
            f'Reporting on classified intelligence commonly rests on unnamed sources. No other paper\'s reports were counted, so nothing here says whether this pattern is unusual. '
            f'<b>Limits:</b> eleven articles saved by hand, one paper; the readers\' filings have not been audited. '
            f'<b>Source:</b> the saved articles; the attribution and claim tables built from them. Fetched Nov 12, 2026. ' + DRAFT)
    ids = [r['row_id'] for r in C.rows()] + ['TA' + r['key'][2:] for r in d['filed']]
    render('nv12-claims-and-their-sources', cite(ids) + shell(title, KICKER, sub, d['b1'] + d['b2'], foot, PAGE, extra_css=d['css']), PAGE)
