"""Check and join the two readers' filing of the Times attributions under a fixed list of claims.
Run: python3 -I scripts/claims_merge.py
Reads  lanes clm1a, clm1b (out/claims.jsonl) under lanes/, and research/sourcing_times_a.tsv
       (the 345 attribution lines of the eleven news reports, already matched to the article text).
Writes research/claims_lines.tsv: one row per attribution line with both readers' claim, stance and basis side by side, and
       the statement each reader copied from the article (kept only if it is in the article, whitespace collapsed).
The drawing rule was fixed before either lane reported (see the README): a line counts under a claim, a
basis or a stance only where both readers give the same value; otherwise it is "the two readers differ"."""
import csv, hashlib, json, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import rows_sourcing as S
from textmatch import find, ws
# the reader lanes' folders: beside the scripts in the published copy, else where they ran
B = str(ROOT / 'lanes')
# script rules used by the figure's place-by-place list (not reader judgments):
# a sentence end is a full stop not after a title or an initial, followed by a capital or an opening quotation mark
SENT_END = re.compile(r'(?<!Mr)(?<!Ms)(?<!Mrs)(?<!Dr)(?<![A-Z])[.!?][”"]?\s+(?=[A-Z“"])')
CITES_TIMES = re.compile(r'\b(?:The New York Times|The Times)\b[^.]{0,40}?\b(?:reported|revealing)\b|reports by The New York Times')
US_AGENCY = re.compile(r'C\.I\.A\.|F\.B\.I\.|N\.S\.A\.|National Security Agency|Central Intelligence|Federal Bureau|Defense Intelligence|Director of National Intelligence|Department|Treasury|Pentagon|Homeland')
NO_TEXT = ('The article texts are not here (the published copy leaves them out; see the README). research/claims_lines.tsv is the result of the last run.\n'
           'To run the merge yourself, save your own copy of each article\'s text as research/primary/<article id>/text.txt.')


def sentence_of(text, passage):
    """The sentence of the article text that holds the passage (None if the passage is not found as one run)."""
    i = text.find(passage)
    if i < 0:
        return None
    starts = [m.end() for m in SENT_END.finditer(text, 0, i)]
    m = SENT_END.search(text, i + len(passage) - 1)
    return text[(starts[-1] if starts else 0):(m.start() + 1 if m else len(text))]


def article_texts(news):
    """(texts the lanes read, saved originals): the lanes' input shard where it is present, and research/primary/<id>/text.txt."""
    saved = {p: re.sub(r'\s+', ' ', (R / 'primary' / p / 'text.txt').read_text()) for p in news if (R / 'primary' / p / 'text.txt').exists()}
    sp = Path(B + '/clm1a/shards/articles.jsonl'); given = {}
    if sp.exists():
        for l in open(sp):
            r = json.loads(l); given[r['id']] = ws(r['text'])
    return (given or {p: ws(t) for p, t in saved.items()}), saved
CLAIMS = ['spy', 'relationship', 'huang_knowledge', 'collection', 'who_was_told', 'trump_stance', 'export_enforcement', 'megaspeed', 'other_buyers', 'congress',
          'company_response', 'second_relationship', 'huang_china_policy', 'her_background', 'markets_industry', 'whole_account', 'other_background']
STANCES = ['asserts', 'disputes', 'declines']
PROP = ['spy', 'relationship', 'huang_knowledge', 'who_was_told']      # claims that can be stated or denied
MODES = ['states', 'comments']
BASES = ['named_on_record', 'institution_on_record', 'institution_conclusion', 'unnamed_people', 'record_available', 'material_described', 'paper_observation', 'earlier_report']


def load(lane, texts, want):
    """The last record per (article, n), the articles closed, and what was dropped."""
    p = Path(f'{B}/{lane}/out/claims.jsonl'); got, done, drop = {}, set(), Counter()
    if not p.exists():
        return got, done, Counter({'lane has no output': 1})
    for l in open(p):
        try:
            r = json.loads(l)
        except Exception:
            drop['unparsable'] += 1; continue
        if r.get('role') == 'page_done':
            done.add(r.get('id')); continue
        k = (r.get('id'), int(r['n']) if str(r.get('n', '')).isdigit() else None)
        if k not in want:
            drop['not a listed line'] += 1; continue
        if r.get('claim') not in CLAIMS or r.get('stance') not in STANCES or r.get('basis') not in BASES:
            drop['value outside the lists'] += 1; continue
        run = find(texts[k[0]], r.get('statement', ''))
        if not run:
            drop['statement not in the article (classification kept, statement left empty)'] += 1
        r['statement'] = run
        got[k] = r                                   # a later line with the same key (a correction) stands in for the earlier one
    return got, done, drop


def load_modes(lane, texts, want):
    """Round 3: for the says-so lines under the four statable claims, whether the source itself states the claim or comments on it."""
    p = Path(f'{B}/{lane}/out/modes.jsonl'); got, drop = {}, Counter()
    if not p.exists():
        return got, Counter({'lane has no output': 1})
    for l in open(p):
        try:
            r = json.loads(l)
        except Exception:
            drop['unparsable'] += 1; continue
        if r.get('role') == 'page_done':
            continue
        k = (r.get('id'), int(r['n']) if str(r.get('n', '')).isdigit() else None)
        if k not in want:
            drop['not a listed line'] += 1; continue
        if r.get('mode') not in MODES:
            drop['value outside the list'] += 1; continue
        run = find(texts[k[0]], r.get('statement', ''))
        if not run:
            drop['statement not in the article (mode kept, statement left empty)'] += 1
        r['statement'] = run
        got[k] = r
    return got, drop


def kappa(pairs):
    n = len(pairs)
    if not n:
        return 0.0
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    news = [t[0] for t in S.TIMES if t[3] == 'news']
    texts, saved = article_texts(news)
    if set(texts) != set(news) or set(saved) != set(news):
        sys.exit(NO_TEXT)
    base = []
    for i, r in enumerate(S.times('a'), 1):
        if r['page'] in news:
            base.append((r.get('row_id') or f'TA{i:04d}', r))
    want = {(r['page'], int(r['n'])) for _, r in base}
    assert len(base) == len(want) == 345, (len(base), len(want))
    # the lanes were given exactly these lines
    if Path(B + '/clm1a/shards/lines.jsonl').exists():
        given = {(json.loads(l)['id'], json.loads(l)['n']) for l in open(B + '/clm1a/shards/lines.jsonl')}
        assert given == want
    A, done_a, drop_a = load('clm1a', texts, want); Bq, done_b, drop_b = load('clm1b', texts, want)
    out = []
    for key, r in base:
        k = (r['page'], int(r['n'])); a, b = A.get(k, {}), Bq.get(k, {})
        out.append({'key': key, 'page': r['page'], 'n': r['n'], 'source': r['source'], 'quote': r['quote'], 'round1_source_type': r['source_type'],
                    'claim_a': a.get('claim', ''), 'claim_b': b.get('claim', ''), 'stance_a': a.get('stance', ''), 'stance_b': b.get('stance', ''),
                    'basis_a': a.get('basis', ''), 'basis_b': b.get('basis', ''), 'statement_a': a.get('statement', ''), 'statement_b': b.get('statement', '')})
    # round 3: the lines both readers filed as saying so under a statable claim
    sub = {(r['page'], int(r['n'])) for r in out if r['claim_a'] == r['claim_b'] and r['claim_a'] in PROP and r['stance_a'] == r['stance_b'] == 'asserts'}
    lp = Path(B + '/clm2a/shards/lines.jsonl')
    if lp.exists():
        given2 = {(json.loads(l)['id'], json.loads(l)['n']) for l in open(lp)}
        assert given2 == sub, ('the round-3 lanes were given a different set of lines', len(given2), len(sub))
    MA, mdrop_a = load_modes('clm2a', texts, sub); MB, mdrop_b = load_modes('clm2b', texts, sub)
    for r in out:
        k = (r['page'], int(r['n'])); a, b = MA.get(k, {}), MB.get(k, {})
        r['mode_asked'] = 'yes' if k in sub else ''
        r['mode_a'] = a.get('mode', ''); r['mode_b'] = b.get('mode', ''); r['mode_statement'] = a.get('statement', '') or b.get('statement', '')
        # the script rules, from the saved original: which sentence holds the attribution, whether that sentence cites the
        # paper's own earlier report, and whether the place names a U.S. agency
        s_ = sentence_of(saved[r['page']], r['quote'])
        r['sentence_id'] = hashlib.sha256((r['page'] + '\n' + s_).encode()).hexdigest()[:12] if s_ else ''
        r['in_times_sentence'] = 'yes' if s_ and CITES_TIMES.search(s_) else ''
        r['names_us_agency'] = 'yes' if US_AGENCY.search(' '.join((r['source'], r['quote'], r['mode_statement'] or r['statement_a']))) else ''
    with open(R / 'claims_lines.tsv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
    print(f'reading A: lines filed {len(A)} of 345 | articles closed {len(done_a & set(news))} of 11 | dropped {dict(drop_a)}')
    print(f'reading B: lines filed {len(Bq)} of 345 | articles closed {len(done_b & set(news))} of 11 | dropped {dict(drop_b)}')
    both = [r for r in out if r['claim_a'] and r['claim_b']]
    for f_ in ('claim', 'stance', 'basis'):
        pairs = [(r[f_ + '_a'], r[f_ + '_b']) for r in both]
        if pairs:
            print(f'{f_}: the readers agree on {sum(a == b for a, b in pairs)} of {len(pairs)} lines (kappa {kappa(pairs):.2f})')
            mis = Counter((a, b) for a, b in pairs if a != b)
            print('   most frequent differences (A, B):', mis.most_common(8))
    agree_all = sum(r['claim_a'] == r['claim_b'] and r['stance_a'] == r['stance_b'] and r['basis_a'] == r['basis_b'] for r in both)
    print(f'all three fields agree on {agree_all} of {len(both)} lines')
    asked = [r for r in out if r['mode_asked']]; mboth = [r for r in asked if r['mode_a'] and r['mode_b']]
    print(f'states or comments: asked of {len(asked)} lines | reading A {len(MA)} {dict(mdrop_a)} | reading B {len(MB)} {dict(mdrop_b)}')
    if mboth:
        mp = [(r['mode_a'], r['mode_b']) for r in mboth]
        print(f'mode: the readers agree on {sum(a == b for a, b in mp)} of {len(mp)} lines (kappa {kappa(mp):.2f}); both say comments on {sum(a == b == "comments" for a, b in mp)}')
    # controls: the statement check can fail, and the agreement count can see a difference
    assert find(texts[news[0]], 'this sentence is not in the article zqxj') == ''
    assert kappa([('a', 'a'), ('b', 'b'), ('a', 'b'), ('b', 'a')]) == 0.0 and kappa([('a', 'a'), ('b', 'b')]) == 1.0
    assert CITES_TIMES.search('The Times reported last month that it was so.') and not CITES_TIMES.search('Officials said it was so.')
    assert US_AGENCY.search('the C.I.A. concluded') and not US_AGENCY.search('U.S. intelligence determined')
    assert sentence_of('One thing. Mr. Smith said so. Another thing.', 'Smith said') == 'Mr. Smith said so.'
    print(f'sentence found for {sum(1 for r in out if r["sentence_id"])} of {len(out)} lines')
    print('controls: ok')


if __name__ == '__main__':
    main()
