"""Finding a quoted passage in a saved page's text. The same three functions as in sourcing_merge.py, kept in a file of their
own so the claims figure can be rebuilt without the rest of that script."""
import re


def ws(s):
    return re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip()


def loose(s):
    """For matching only: quotation marks, apostrophes, dashes and ligatures folded."""
    for a, b in (('’', "'"), ('‘', "'"), ('ʼ', "'"), ('“', '"'), ('”', '"'), ('–', '-'), ('—', '-'),
                 ('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬃ', 'ffi'), ('ﬀ', 'ff'), ('ﬄ', 'ffl')):
        s = s.replace(a, b)
    return s


def find(text, passage):
    """The page's own run that equals the passage (exactly, or after folding marks and ligatures), else ''."""
    p = ws(passage)
    if not p:
        return ''
    if p in text:
        return p
    lt, lp = loose(text), loose(p)
    if len(lt) == len(text):                       # folding kept every position: copy the page's own characters
        i = lt.find(lp)
        return text[i:i + len(lp)] if i >= 0 else ''
    return lp if lp in lt else ''                  # a ligature changed lengths: keep the folded run (it is in the folded text)
