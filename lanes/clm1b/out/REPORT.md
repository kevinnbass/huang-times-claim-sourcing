All 345 listed attributions are filed across 11 articles. Each article has exactly one closing line, with its required count. The tables count the latest entry for each `(id, n)`; 5 appended replacement rows clarify excerpts without changing their classifications.

**Claim by basis**

| claim | named_on_record | institution_on_record | institution_conclusion | unnamed_people | record_available | material_described | paper_observation | earlier_report | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| spy | 4 | 7 | 6 | 14 | 0 | 6 | 0 | 8 | 45 |
| relationship | 24 | 3 | 4 | 5 | 2 | 3 | 0 | 4 | 45 |
| huang_knowledge | 10 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 15 |
| collection | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 1 | 8 |
| who_was_told | 12 | 6 | 0 | 6 | 0 | 0 | 0 | 4 | 28 |
| trump_stance | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19 |
| export_enforcement | 4 | 7 | 1 | 14 | 0 | 0 | 0 | 4 | 30 |
| megaspeed | 0 | 7 | 2 | 12 | 9 | 0 | 1 | 3 | 34 |
| other_buyers | 0 | 3 | 0 | 7 | 7 | 0 | 3 | 0 | 20 |
| congress | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| company_response | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| second_relationship | 1 | 5 | 0 | 6 | 0 | 0 | 0 | 1 | 13 |
| huang_china_policy | 15 | 2 | 0 | 6 | 0 | 0 | 0 | 0 | 23 |
| her_background | 2 | 1 | 0 | 3 | 8 | 0 | 1 | 1 | 16 |
| markets_industry | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| whole_account | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 4 |
| other_background | 9 | 2 | 0 | 3 | 1 | 0 | 0 | 0 | 15 |
| total | 119 | 57 | 13 | 88 | 27 | 10 | 5 | 26 | 345 |

**Claim by stance**

| claim | asserts | disputes | declines | total |
| --- | ---: | ---: | ---: | ---: |
| spy | 36 | 4 | 5 | 45 |
| relationship | 34 | 11 | 0 | 45 |
| huang_knowledge | 1 | 14 | 0 | 15 |
| collection | 8 | 0 | 0 | 8 |
| who_was_told | 13 | 7 | 8 | 28 |
| trump_stance | 19 | 0 | 0 | 19 |
| export_enforcement | 26 | 3 | 1 | 30 |
| megaspeed | 31 | 2 | 1 | 34 |
| other_buyers | 20 | 0 | 0 | 20 |
| congress | 9 | 0 | 1 | 10 |
| company_response | 18 | 0 | 0 | 18 |
| second_relationship | 11 | 0 | 2 | 13 |
| huang_china_policy | 23 | 0 | 0 | 23 |
| her_background | 16 | 0 | 0 | 16 |
| markets_industry | 2 | 0 | 0 | 2 |
| whole_account | 4 | 0 | 0 | 4 |
| other_background | 15 | 0 | 0 | 15 |
| total | 286 | 41 | 18 | 345 |

**Unfiled lines**

None. The effective attribution keys exactly match `shards/lines.jsonl`, including every article's running numbers.

**Definition boundaries and dispositions**

- `collection` / `who_was_told`: the definitions overlap for memo recipients. Memo drafting, circulation and intended recipients are `collection`: `man-nyt-1108-02` n=2, 13; `man-nyt-1109-01` n=10; `man-nyt-1110-02` n=18. Actual presidential briefings, warnings and reactions are `who_was_told`, including `man-nyt-1110-02` n=2, 3, 20–22.
- `spy` / `relationship`: combined statements can describe both the relationship and the woman's intelligence role. The earlier category, `spy`, governs the combined memo/intelligence statements at `man-nyt-1108-02` n=1 and `man-nyt-1110-02` n=1. Statements limited to contact or intimacy remain `relationship`.
- `export_enforcement` / `other_buyers`: licensing decisions are `export_enforcement`, including `man-nyt-1107-01` n=11–13, 28. Statements principally about buyers' corporate ties are `other_buyers`, including that article's n=8, 33, 34.
- `company_response` / `second_relationship`: the specific definition covering the second relationship and its cited code of conduct governs `man-e1161e38dc19` n=4, 5, 11, 12, 18 and `man-nyt-1112-07` n=18, 19. These are `second_relationship`.
- `spy` / `megaspeed`: Megaspeed's general responses about the allegations and its own investigation, without a specific admission or denial about Alice Huang's intelligence role, are `megaspeed`: `man-nyt-1029-01` n=17–19.

**Other coding and excerpt notes**

Named private speakers whose words are expressly relayed through unnamed participants retain `unnamed_people` as the article's information route, including `man-nyt-1110-02` n=3, 21 and `man-nyt-1111-02` n=1, 6, 12. Directly attributed public statements, employee messages and acknowledgments use the named or institutional speaker as applicable.

Historical May invitations before the reports are `huang_china_policy`, including `man-nyt-1108-02` n=15, 16 and `man-nyt-1110-02` n=19, 23. Invitations or decisions after the reports are `trump_stance`.

`man-nyt-1029-01` n=12 is a conditional expectation that the government would notify Nvidia, filed as `who_was_told` / `asserts`. It is not converted into an express denial that a warning occurred. Nonanswers about when the president learned the information are `declines`; explicit denials or failures to recall are `disputes`.

Page boundaries require shortened excerpts at `man-nyt-1105-01` n=11 and `man-nyt-1107-01` n=6, 29. No excerpt bridges a header. The replacement at `man-nyt-1029-01` n=27 uses the continuation on the next page as its single passage.

**Checks**

`out/validation.json` records the counts, input/output hashes and checks. All raw and effective statements pass exact substring matching after whitespace collapse, the word limit and the single-page check. The longest effective statement has 37 words. All 7 deliberate fault controls were rejected: altered text, excess words, a page crossing, an invalid label, a missing attribution, a duplicate closing line and an unmarked duplicate.

The article sequence follows `articles.jsonl`; running numbers within each article follow `lines.jsonl`. The latter file groups its undated article first, unlike the article file. The validator checks the required article sequence and per-article numbering separately.

claims: complete
