# Attribution report

Input: `shards/shard-01.jsonl`. Output: `out/attributions.jsonl`.

Each article was read in full in input order. Replacements supersede the preceding record with the same article id and attribution number. Replacement records are counted once.

| Article id | named_person | institution | document | own_observation | other_outlet | unnamed | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| man-e1161e38dc19 | 4 | 4 | 3 | 1 | 0 | 7 | 19 |
| man-nyt-1029-01 | 7 | 12 | 14 | 6 | 1 | 29 | 69 |
| man-nyt-1105-01 | 12 | 4 | 2 | 2 | 0 | 2 | 22 |
| man-nyt-1106-01 | 13 | 3 | 1 | 2 | 0 | 9 | 28 |
| man-nyt-1107-01 | 5 | 8 | 7 | 5 | 1 | 9 | 35 |
| man-nyt-1108-01 | 22 | 8 | 6 | 2 | 1 | 2 | 41 |
| man-nyt-1108-02 | 11 | 7 | 3 | 1 | 0 | 7 | 29 |
| man-nyt-1109-01 | 18 | 2 | 1 | 3 | 0 | 1 | 25 |
| man-nyt-1110-01 | 11 | 5 | 3 | 0 | 0 | 1 | 20 |
| man-nyt-1110-02 | 19 | 5 | 2 | 2 | 0 | 10 | 38 |
| man-nyt-1111-01 | 16 | 8 | 5 | 6 | 8 | 10 | 53 |
| man-nyt-1111-02 | 4 | 6 | 0 | 1 | 1 | 5 | 17 |
| man-nyt-1112-07 | 10 | 5 | 2 | 2 | 1 | 2 | 22 |
| **Total** | 152 | 77 | 49 | 33 | 13 | 94 | **418** |

Closing records: 13. Replacement records: 9.

Counting and classification:

- Named people in a joint attribution receive separate records when the sentence names them separately. A collective reference is retained as written.
- References to this newspaper’s reporting are `own_observation`; references to another outlet’s reporting are `other_outlet`. A quoted person remains `named_person` when the article identifies an interview or podcast.
- Cited surveillance findings, records, profiles, filings, reports and datasets are `document`. Institutions identified as speaking are `institution`.
- Statements that someone did not respond are excluded. Refusals to comment and the reported lack of a Treasury Department comment are included.
- The newsletter’s news sections, quote of the day and source citations in its news roundup are included. Captions, photo credits, page furniture, subscription prompts, bylines and reporter biographies are excluded.

Excerpt exception:

- `man-nyt-1029-01`, attribution 27: the source `They` ends page 3, and its predicate `described` begins page 4 after the header. The record contains the page-local locator `current and former U.S. officials said. They`. This locator preserves the source and the preceding attribution, but cannot include the predicate of instance 27 without crossing the header. The instance is counted; its excerpt does not meet the source-and-predicate requirement.

No network access was used. No sources were identified from another article. No requested article was skipped.

The validator checks schemas, enums, exact substrings after whitespace collapse, word limits, source containment, page boundaries, reading order, replacement targets, numbering and closing counts. Failure controls and run results are saved in `out/validation.json`. These checks do not resolve the excerpt exception above.

attributions: incomplete page furniture separates one attribution’s source and predicate
