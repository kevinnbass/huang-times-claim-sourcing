# Task: file 345 listed attributions from eleven newspaper articles under a fixed list of claims

Owner: the session that built the figure, 2026-11-13.

You are running headless in the folder lanes/clm1b. Work only inside it, and do not read any other lane's folder. Do not use the network at all: everything you need is in `shards/`.
This is for a private research project on how one news story was reported (the Nvidia chief executive's resignation, Oct 29 to Nov 12, 2026). Nothing here is published. A script will check your output against the article text, character for character, and a person will then read it. A second reader is doing the same task separately; the two will be compared line by line.

## Input
- `shards/articles.jsonl`: eleven articles, one JSON object per line: `id`, `title`, `date`, `text`. The text is a PDF text layer: page headers (a shortened headline, "3 of 12", a shortened address, a timestamp), photo credits and newsletter prompts are mixed in. Ignore them.
- `shards/lines.jsonl`: 345 attributions already found in those articles, one per line: `id` (the article), `n` (its running number within the article, in reading order), `source` (the article's words for the source) and `quote` (the article's words containing the source and the attributing words). The list is fixed: do not add, drop, merge or renumber lines.

## What to do
Read each article in full, in order. Then, for every line of `lines.jsonl` belonging to it, find the place in the article and decide four things. Append one JSON line per attribution to `out/claims.jsonl` with the keys `id`, `n`, `role` (always `claim`), `claim`, `stance`, `basis`, `statement`.

### `statement`
The article's own words for what this source is said to say, show or do at that place: one unbroken run of the article text, copied character for character, at most 40 words. It may overlap `quote`. It must not cross a page header. Example: for the line whose quote is "people briefed on the surveillance said", the statement is the run of words that those people are reported to have said.

### `claim`: what the attributed statement is about. Exactly one of:
1. `spy`: that Alice Huang (Huang Le) worked for, was recruited by, or passed information to Chinese intelligence, or was targeting Mr. Huang; and denials of that.
2. `relationship`: that Jensen Huang and Alice Huang had a close, romantic or intimate relationship: contact shown by surveillance, photographs together, her talk of her connection to him, his acknowledgment, and statements that their dealings were ordinary or "not unusual".
3. `huang_knowledge`: whether Mr. Huang knew what she was, and whether national security or company secrets were compromised.
4. `collection`: the intelligence gathering itself, not what it showed: that U.S. agencies surveilled her, that surveillance continues, that a memo circulated and who received it, requests to identify the American in the intercepts. A line that reports what the surveillance or memo showed is filed under what it showed (`spy` or `relationship`).
5. `who_was_told`: who in the U.S. government was warned or briefed about the matter, when, by whom, and what they then did or did not do about Mr. Huang; including the president's statements about what he was told.
6. `trump_stance`: what Mr. Trump or the White House said or did about Mr. Huang after the reports: defending him, trips and invitations, whether he should stay, speaking with him.
7. `export_enforcement`: how the U.S. government handled Nvidia chip exports and enforcement: investigations or sanctions said to have stalled, licences approved, the dispute over adding Megaspeed to the entity list, agency statements on licensing, officials' or lawmakers' views on loopholes.
8. `megaspeed`: Megaspeed's business and whether it helped China obtain restricted chips: its purchases, records of them, its data centres, suspicions of diversion or smuggling, the site visit, and Megaspeed's or Nvidia's answers about it.
9. `other_buyers`: other buyers cleared to receive chips or linked to China (New Matrix, Maginfra, Wise Road, Inspur and the like): who they are, their offices, their records.
10. `congress`: what members of Congress asked for, wrote, said or did.
11. `company_response`: what Nvidia, its board or its executives said or did in response: statements, the investigation, the resignation, the search for a successor, messages to employees. Mr. Huang's own acknowledgment of the relationship is `relationship`, not this.
12. `second_relationship`: the reported relationship between Mr. Huang and an Nvidia executive, how the company handled it, and the code of conduct cited about it.
13. `huang_china_policy`: Mr. Huang's and Nvidia's positions on selling chips to China and their dealings with the administration: lobbying, donations, investment pledges, closeness to the president, China's own limits on imports.
14. `her_background`: Alice Huang's biography, career, titles and manner, apart from the intelligence claim.
15. `markets_industry`: effects on Nvidia's business, its stock and the industry; analysts' views of them.
16. `whole_account`: a statement of what the article as a whole is based on ("This account is based on interviews with ...").
17. `other_background`: anything else: Chinese intelligence services in general, Mr. Huang's biography and marriage, comparisons with other executives.

File by what the statement is about, not by who is speaking. If two fit, take the one earlier in the list. A line that restates an earlier report ("The Times reported last month that ...") is filed under the claim it restates.

### `stance`: exactly one of
- `asserts`: the source gives the information, or supports or confirms the claim
- `disputes`: the source denies it, contradicts it, or says the opposite
- `declines`: the source declined to comment or gave no answer

For `spy`, `relationship`, `huang_knowledge` and `who_was_told`, read the claim as a proposition: "she worked for Chinese intelligence"; "the two had a romantic or intimate relationship"; "Mr. Huang knew what she was, or secrets were compromised"; "the president and other officials were warned". A source saying Mr. Huang did not know `disputes` `huang_knowledge`; a source saying their dealings were routine `disputes` `relationship`; the president saying he was not told `disputes` `who_was_told`.

### `basis`: how the article has the information at that place. Exactly one of:
- `named_on_record`: a person the article names, speaking or writing in their own name (a named spokesperson, public remarks, a letter, a post); later references to the same named person too
- `institution_on_record`: a company, agency, board, embassy or office speaking for itself: a statement, an announcement, its own website or filing, a spokesperson the article does not name, a refusal to comment
- `institution_conclusion`: a conclusion, suspicion or action that the article ascribes to an agency or to "U.S. intelligence", "American spy agencies", "the U.S. government" and the like, where the article does not say the body stated it on the record ("U.S. intelligence determined", "American spy agencies concluded")
- `unnamed_people`: people or officials the article does not name: "U.S. officials", "people briefed on the matter", "a person with knowledge", unnamed analysts, workers or associates, and later references to them ("the people said", "they said")
- `record_available`: a public record, or one the article says the paper obtained or viewed: corporate, trade or court records, filings, data platforms, websites, photographs, public posts, "documents viewed by The Times"
- `material_described`: classified or internal material (surveillance, intelligence, a memo, private messages) whose content the article relays without saying the paper itself saw it
- `paper_observation`: what the paper's own reporters saw, visited, checked or could not find
- `earlier_report`: an earlier report by this paper or another news organization, cited as such

Decide `basis` from the article's words at that place. Do not carry a judgment over from another article.

Then exactly one closing line per article: `{"id": "<article id>", "role": "page_done", "n": <number of claim lines you wrote for it>}`. That number must equal the number of lines `lines.jsonl` has for the article.

## Rules
- **Only what the article says.** Nothing from memory, nothing from another article, nothing looked up.
- **Character for character.** `statement` must be findable in the article's `text` as an exact substring after collapsing runs of whitespace to one space. Keep the text's own quotation marks, apostrophes, dashes and letter forms. Do not join two passages with an ellipsis. Before you close an article, run a check of your own over its lines and fix any that fail.
- **Your own judgment on every line.** Scripts may load and print text and check your output, but must not assign `claim`, `stance` or `basis` by keyword.
- **Never guess who an unnamed source is.** No judgments of reliability. No adjectives of your own.
- Do not write into any folder but this one.

## Resume
If `out/claims.jsonl` already has a `page_done` line for an id, skip that article. Append only; to correct a line, append a line with the same `id` and `n` plus `"replaces": true`.

## Report
When every article has its closing line, write `out/REPORT.md`: a table of `claim` by `basis`; a table of `claim` by `stance`; any line you could not file and why; any claim whose definition you found unclear, with the line numbers. End with one line: `claims: complete` or `claims: incomplete <reason>`. Your final message is that same line.
