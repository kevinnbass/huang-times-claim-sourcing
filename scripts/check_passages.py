"""Check every quoted passage behind the claims figure against the article it is said to come from.
Run: python3 scripts/check_passages.py

The article texts are not in this repository. To run the check, save your own copy of each article's text as
research/primary/<article id>/text.txt (the ids and addresses are in links.tsv). A passage passes if it is found in the
article after runs of whitespace are collapsed and typographic quotation marks, dashes and PDF ligatures are folded.
Nothing else is changed.

Rows checked: every attribution passage of the first reading (research/sourcing_times_a.tsv), every statement the later
readers copied (research/claims_lines.tsv), and the four passages from the first report (rows_claimlines.FIRST_REPORT).
Exit code: 0 all found; 1 a passage was not found; 2 some article text was not supplied, so those rows were not checked."""
import hashlib, json, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rows_claimlines, rows_sourcing


def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace(' ', ' ').replace('​', '')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬃ', 'ffi'), ('ﬄ', 'ffl'), ('ﬀ', 'ff'), ('ʼ', "'")):
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    news = {t[0] for t in rows_sourcing.TIMES if t[3] == 'news'}
    rows = [r for r in rows_sourcing.rows() + rows_claimlines.rows() if r['src'] in news]
    ids = Counter(r['row_id'] for r in rows); assert max(ids.values()) == 1, [k for k, v in ids.items() if v > 1][:5]
    texts = {}
    for p in sorted(news):
        f = ROOT / 'research' / 'primary' / p / 'text.txt'
        if f.exists():
            raw = f.read_bytes(); texts[p] = norm(raw.decode('utf-8', 'replace'))
            meta = json.loads((f.parent / 'meta.json').read_text())
            same = hashlib.sha256(raw).hexdigest() == meta.get('text_sha256')
            print(f'{p}: text supplied ({len(raw):,} bytes; {"the same bytes as" if same else "not byte-identical to"} the copy the figure was built from)')
    checked = failed = 0; missing = Counter()
    for r in rows:
        if r['src'] not in texts:
            missing[r['src']] += 1; continue
        checked += 1
        if norm(r['q']) not in texts[r['src']]:
            failed += 1; print('NOT FOUND', r['row_id'], r['src'], '|', r['q'][:90])
    # control: the check can fail
    control = bool(texts) and all(norm('this passage is not in the article zqxj') not in t for t in texts.values())
    print(f'rows={len(rows)} checked={checked} failed={failed} not_checked_no_text={sum(missing.values())} articles_supplied={len(texts)}_of_{len(news)} control_caught={"yes" if control else "not run"}')
    sys.exit(1 if failed else (2 if missing else 0))


if __name__ == '__main__':
    main()
