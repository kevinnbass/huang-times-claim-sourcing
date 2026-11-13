"""Render the claims figure (figures/nv12-claims-and-their-sources.html, .png, .jpg) from the tables in research/.
Run: python3 scripts/build_nv12.py
Needs Python 3.10 or later, playwright with its chromium browser (pip install playwright; playwright install chromium)
and pillow. The article texts are not needed: everything the figure draws is in research/claims_lines.tsv."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig_claimsources

KICKER = 'Huang resignation · dated public records, Nov 2026 · draft'
DRAFT = ('<b>Status:</b> draft of Nov 12, 2026. Each passage behind a drawn item was matched by script to a saved copy '
         'of its source. One independent audit round read the first eight figures and their rows against the saved copies, and its findings are applied; '
         'it did not fetch the originals again, and rows added since then have not been audited.')

if __name__ == '__main__':
    fig_claimsources.draw(KICKER, DRAFT)
