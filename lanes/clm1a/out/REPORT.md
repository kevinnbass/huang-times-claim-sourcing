Counts use the latest entry for each `(id, n)`: 345 attributions across 11 articles. The file includes 18 appended replacement entries; superseded entries are excluded from both tables. Each article has exactly one `page_done` line with its original attribution count. Articles follow `articles.jsonl` order; attribution numbers retain their original order within each article.

Claim by basis

| claim | named_on_record | institution_on_record | institution_conclusion | unnamed_people | record_available | material_described | paper_observation | earlier_report | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| spy | 4 | 7 | 6 | 13 | 0 | 4 | 0 | 8 | 42 |
| relationship | 17 | 7 | 4 | 5 | 2 | 5 | 0 | 5 | 45 |
| huang_knowledge | 10 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 15 |
| collection | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 6 |
| who_was_told | 12 | 4 | 0 | 8 | 2 | 0 | 0 | 5 | 31 |
| trump_stance | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| export_enforcement | 4 | 5 | 1 | 13 | 0 | 0 | 0 | 3 | 26 |
| megaspeed | 0 | 7 | 2 | 12 | 9 | 0 | 1 | 4 | 35 |
| other_buyers | 0 | 3 | 0 | 7 | 7 | 0 | 3 | 0 | 20 |
| congress | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 9 |
| company_response | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 22 |
| second_relationship | 1 | 3 | 0 | 6 | 2 | 0 | 0 | 1 | 13 |
| huang_china_policy | 14 | 2 | 0 | 7 | 0 | 1 | 0 | 0 | 24 |
| her_background | 2 | 1 | 0 | 3 | 8 | 0 | 1 | 1 | 16 |
| markets_industry | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| whole_account | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 4 |
| other_background | 9 | 2 | 0 | 3 | 1 | 0 | 0 | 0 | 15 |
| total | 113 | 56 | 13 | 89 | 31 | 11 | 5 | 27 | 345 |

Claim by stance

| claim | asserts | disputes | declines | total |
| --- | ---: | ---: | ---: | ---: |
| spy | 33 | 4 | 5 | 42 |
| relationship | 34 | 11 | 0 | 45 |
| huang_knowledge | 2 | 13 | 0 | 15 |
| collection | 6 | 0 | 0 | 6 |
| who_was_told | 16 | 7 | 8 | 31 |
| trump_stance | 20 | 0 | 0 | 20 |
| export_enforcement | 24 | 1 | 1 | 26 |
| megaspeed | 32 | 2 | 1 | 35 |
| other_buyers | 20 | 0 | 0 | 20 |
| congress | 8 | 0 | 1 | 9 |
| company_response | 20 | 2 | 0 | 22 |
| second_relationship | 11 | 0 | 2 | 13 |
| huang_china_policy | 24 | 0 | 0 | 24 |
| her_background | 16 | 0 | 0 | 16 |
| markets_industry | 2 | 0 | 0 | 2 |
| whole_account | 4 | 0 | 0 | 4 |
| other_background | 15 | 0 | 0 | 15 |
| total | 287 | 40 | 18 | 345 |

Unfiled lines

None. Every input `(id, n)` has an effective claim entry.

Definition boundaries requiring judgment

| Definitions | Lines | Filing decision |
| --- | --- | --- |
| `relationship` / `her_background` | `man-nyt-1106-01` n=8; `man-nyt-1108-02` n=26 | General industry connections and language ability are `her_background`; these passages do not describe the closeness or intimacy of the particular relationship. |
| `collection` / `who_was_told` | `man-nyt-1108-02` n=2,13; `man-nyt-1110-02` n=18 | Memo circulation and intended recipients are `collection`. The account of Rubio warning officials is `who_was_told`. A memo's reported substantive findings are filed by their content. |
| `congress` / substantive claims | `man-nyt-1105-01` n=9; `man-nyt-1108-01` n=35,41 | The national-security-risk question is `huang_knowledge`; the request for answers is `congress`. McCaul's statement supports the espionage account and also proposes an export pause; `spy` takes precedence. |
| `export_enforcement` / `other_buyers` | `man-nyt-1107-01` n=8,11–13,28,33–34 | Statements about licensing approvals are `export_enforcement`. Statements about approved buyers' ownership or military ties are `other_buyers`. |
| `company_response` / `megaspeed` / `huang_china_policy` | `man-nyt-1029-01` n=10,28; `man-nyt-1105-01` n=20 | Nvidia's general denial of chip smuggling is `company_response`; its specific answer about Megaspeed is `megaspeed`. The general denial does not state a position on whether chips should be sold to China. |
| `second_relationship` / `company_response` / `other_background` | `man-e1161e38dc19` n=4–5,14–16; `man-nyt-1112-07` n=18–19 | The code and misconduct policy cited about the second relationship are `second_relationship`. Powell's career and technical presentation are `other_background`. |

Stance and basis notes

- `man-nyt-1109-01` n=11–14 and `man-nyt-1110-02` n=4,6,9–10: denials of hearing the information and the statement of no recollection are `disputes`; demurring or saying he would have to check is `declines` because it gives no definite answer about receiving the briefing.
- `man-nyt-1029-01` n=58: the paper's inability to corroborate the biography is `asserts` / `paper_observation`; it does not assert the opposite biography.
- `man-nyt-1107-01` n=22; `man-nyt-1108-01` n=2; `man-nyt-1108-02` n=7; `man-nyt-1109-01` n=17: the board disclosures are conveyed through Nvidia's statement, so the basis is `institution_on_record`. Huang's directly attributed public statements or employee messages use `named_on_record`.
- `man-nyt-1110-02` n=3,20–21; `man-nyt-1111-02` n=1–2,6–7,12: naming the participant in a private conversation does not make its sourcing on record. These accounts use `unnamed_people`.
- `man-nyt-1110-02` n=26–27: the office's background email was sent to the paper, so it is `record_available`; it is not treated as an on-record statement.
- `man-nyt-1108-02` n=16: the article describes a drafted post without saying it was published or viewed by the paper; its content is `material_described`.
- Corporate self-descriptions are `institution_on_record`; corporate records, biographies, directories and records of ownership are `record_available`. The subsidiary's promise in `man-nyt-1029-01` n=67 is relayed within the stock-filing passage and uses `record_available`.
- `man-nyt-1108-01` n=40 uses `record_available` for the media-captured footage. `man-e1161e38dc19` n=6 uses `unnamed_people` for the video described by workers; that article explicitly says the paper has not seen it.

Text and file checks

The final output passed 3 consecutive checks, each including 10 deliberately failing controls. Checks covered exact coverage and numbering, article order, replacement handling, allowed values and keys, closing counts, the word limit, exact substring matching after whitespace normalization, and separation from PDF headers. Every statement is at most 40 words. Validation details and file hashes are saved in `work/validation.json`.

Page headers split the attributed sentences in `man-nyt-1105-01` n=11 and `man-nyt-1107-01` n=6,29. Those entries retain a contiguous fragment on one side of the header.

claims: complete
