# Attribution report

Input: `shards/shard-01.jsonl`. Articles were read in full, in input order. All work used the saved text; no network was used.

Counts below use the last record for each `(id, n)`. Appended replacement records are corrections, not additional attribution instances.

| Article id | named_person | institution | document | own_observation | other_outlet | unnamed | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| man-e1161e38dc19 | 6 | 5 | 3 | 1 | 0 | 7 | 22 |
| man-nyt-1029-01 | 8 | 14 | 14 | 5 | 1 | 25 | 67 |
| man-nyt-1105-01 | 6 | 3 | 3 | 3 | 0 | 3 | 18 |
| man-nyt-1106-01 | 14 | 3 | 2 | 2 | 0 | 6 | 27 |
| man-nyt-1107-01 | 5 | 12 | 7 | 5 | 1 | 9 | 39 |
| man-nyt-1108-01 | 22 | 8 | 6 | 2 | 1 | 3 | 42 |
| man-nyt-1108-02 | 10 | 7 | 3 | 1 | 0 | 6 | 27 |
| man-nyt-1109-01 | 19 | 2 | 2 | 3 | 0 | 1 | 27 |
| man-nyt-1110-01 | 11 | 5 | 2 | 0 | 0 | 1 | 19 |
| man-nyt-1110-02 | 17 | 5 | 3 | 2 | 0 | 9 | 36 |
| man-nyt-1111-01 | 16 | 7 | 4 | 6 | 9 | 10 | 52 |
| man-nyt-1111-02 | 4 | 5 | 0 | 1 | 1 | 5 | 16 |
| man-nyt-1112-07 | 12 | 5 | 3 | 2 | 1 | 2 | 25 |
| **Totals** | 150 | 81 | 52 | 33 | 14 | 87 | **417** |

Each of the 13 articles has exactly one `page_done` record. The file contains 41 replacement records.

## Checks

The final attribution file passed the local validator three times with the same SHA-256. It checked JSON fields, source types, topics, word limits, exact substrings after whitespace collapse, source containment in quotations, page boundaries, source order, numbering, and closing counts. Every pass rejected ten altered cases used as controls. These checks establish formatting and span consistency; they do not establish a census of attribution instances.

Validator: `validate_attributions.py`. Results: `out/validation-1.json`, `out/validation-2.json`, `out/validation-3.json`.

- Input SHA-256: `0916464b81870f5cfc0f1f5e4be861ea6adaefe797a2bec474bac499e73202e5`
- Attribution SHA-256: `da1879c780c2842e718c633e237e08fa05f3f033d92a8b11291caa89b3fd5eb7`

## Counting and classification

Article summaries were included. Captions, photo credits, bylines, reporter biographies, newsletter subscription prompts, metadata, and running page furniture were excluded. The newsletter’s reporting sections, including subjects outside Nvidia, were included. Explicit failures to respond to requests for comment were counted. Speech recounted inside a quotation was kept within that quotation’s attribution.

References to The Times’s own reporting were classified as `own_observation`. Records, surveillance findings, photographs, social media records, and datasets cited as sources were classified as `document`. A named author speaking through a post or letter remained `named_person`; an institution speaking through a spokesperson the article did not name remained `institution`. Topics follow the content of the statement, including `intelligence_and_relationship` for statements about the relationships and `company` for board inquiries and succession.

## Could not record

In `man-nyt-1029-01`, the sentence following attribution 25 starts with `They` at the end of PDF page 3. Its verb, `described`, and the statement about investigations and proposed trade sanctions appear on page 4. The intervening footer and page header prevent a quotation that both contains the source and attribution words and stays on one side of a header. That continuation has no attribution row. Its preceding attribution to `current and former U.S. officials` is recorded.

No network access or outside-source research was performed. No background process remains running. The file and this report are the handoff; coverage is incomplete for the reason above.

attributions: incomplete one attribution crosses a PDF page header
