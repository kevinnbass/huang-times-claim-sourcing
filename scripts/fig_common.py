"""Shared render and tokens for the figure: warm paper background, spaced-caps kicker, bold title, grey subtitle,
legend chips, footnote under a rule. Row ids ride only in an HTML comment.
The page grows to fit its content; the PNG is cut at the measured height."""
from pathlib import Path
import re
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / 'figures'
BG = '#f7f4ee'; INK = '#191b1a'; MUTED = '#666960'; GRID = '#e3dfd5'; AXIS = '#c3c2b7'; CARD = '#efece4'
BLUE = '#2a78d6'; ORANGE = '#eb6834'; AQUA = '#1baf7a'; YELLOW = '#eda100'; RED = '#e34948'
BLUE250 = '#86b6ef'; GRAY = '#b2b4aa'; LGRAY = '#dcd9cf'; PURPLE = '#7b5cd6'
PARTY_D = '#2f5da8'; PARTY_R = '#b93129'
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def money(v):
    v = float(v)
    if v >= 1e6: return f'${v/1e6:,.1f}M' if v < 100e6 else f'${v/1e6:,.0f}M'
    return f'${v:,.0f}'


def day(d, year=False):
    """'2026-07-07' -> 'Jul 7'; '2026-05' -> 'May 2026'."""
    p = d.split('-')
    if len(p) == 2: return f'{MONTHS[int(p[1]) - 1]} {p[0]}'
    s = f'{MONTHS[int(p[1]) - 1]} {int(p[2])}'
    return f'{s}, {p[0]}' if year else s


def legend(items):
    return '<div class="legend">' + ''.join(f'<span><i class="sw" style="background:{c}"></i>{esc(t)}</span>' for c, t in items) + '</div>'


def cite(ids):
    return '<!-- rows: ' + ' '.join(sorted(set(ids))) + ' -->'


def shell(title, kicker, subtitle, body, footnote, width, extra_css=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(re.sub("<[^>]+>", "", title))}</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;background:{BG}}}
body{{padding:46px 60px 34px;font-family:Arial,Helvetica,sans-serif;color:{INK}}}
.kicker{{font-size:17px;letter-spacing:2.8px;text-transform:uppercase;color:{MUTED};font-weight:bold}}
h1{{font-size:46px;letter-spacing:-1.4px;margin:12px 0 10px;line-height:1.07;max-width:{width - 160}px}}
.subtitle{{font-size:22px;line-height:1.35;color:{MUTED};margin:0 0 16px;max-width:{min(width - 220, 1900)}px}}
.legend{{display:flex;gap:26px;font-size:18px;color:{INK};margin:0 0 14px;flex-wrap:wrap}}
.legend span{{display:inline-flex;align-items:center;gap:9px}}.sw{{width:18px;height:18px;border-radius:4px;display:inline-block}}
.footnote{{margin-top:30px;border-top:1px solid #cdcfc6;padding-top:12px;font-size:15px;line-height:1.45;color:{MUTED}}}
.footnote b{{color:{INK}}}svg{{display:block}}text{{font-family:Arial,Helvetica,sans-serif}}{extra_css}
</style></head><body><div class="kicker">{esc(kicker)}</div><h1>{title}</h1><p class="subtitle">{subtitle}</p>{body}<div class="footnote">{footnote}</div></body></html>'''


def render(stem, document, width):
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / (stem + '.html'); path.write_text(document, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': width, 'height': 900}, device_scale_factor=2)
        pg.goto(path.as_uri(), wait_until='networkidle'); pg.evaluate('document.fonts.ready')
        ov = pg.evaluate('({w:document.documentElement.scrollWidth,h:Math.ceil(document.documentElement.scrollHeight)})')
        assert ov['w'] <= width, (stem, 'content wider than the page', ov)
        clipped = pg.evaluate('''() => [...document.querySelectorAll('[data-fit]')].filter(e => e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1).map(e => e.textContent.slice(0, 60))''')
        assert not clipped, (stem, 'text overflows its box', clipped)
        pg.set_viewport_size({'width': width, 'height': ov['h']})
        pg.screenshot(path=str(FIGURES / (stem + '.png')), full_page=True); b.close()
    im = Image.open(FIGURES / (stem + '.png')).convert('RGB'); im.save(FIGURES / (stem + '.jpg'), quality=92)
    print('rendered', stem, im.size)
