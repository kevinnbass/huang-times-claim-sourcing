# Task: list every attribution in thirteen saved newspaper articles and say what kind of source each one is

Owner: the session that built the figure, 2026-11-13.

You are running headless in the folder lanes/origin1a. Work only inside it. Do not use the network at all: everything you need is in `shards/`.
This is for a private research project on how one news story was reported (the Nvidia chief executive's resignation, Oct 29 to Nov 12, 2026). Nothing here is published. A script will check your output against the article text, character for character, and a person will then read it. A second reader is doing the same task separately; the two lists will be compared.

## Input
`shards/shard-01.jsonl`: one JSON object per line, one per article, with keys `id`, `url`, `outlet`, `title`, `author`, `date`, `text`. The text is a PDF text layer: page headers (a shortened headline, "3 of 12", a shortened address, a timestamp), photo credits and newsletter prompts are mixed in. Ignore them.

## What counts
An **attribution** is a place where the article says where a piece of information or a statement comes from: a person said, wrote, told, confirmed, denied or declined to comment; a company or agency said; a document, record or dataset shows; another news organization reported; officials or other people the article does not name said. Information the article states in its own voice, with no source given, gets no line.

Read each article yourself, in full, in order (a search for the word "said" is not reading; scripts may load and print text for you, but the judgment is yours). For each attribution append one JSON line to `out/attributions.jsonl`:
- `id`: the article id
- `role`: `attribution`
- `n`: a running number within the article, from 1, in the order the attributions appear
- `source_type`: exactly one of
  - `named_person`: a person the article names, including a named spokesperson ("John Rizzo, a spokesman for Nvidia") and the named author of a letter or post; later references to the same named person ("Mr. Rizzo said", "he added") are also `named_person`
  - `institution`: a named company, agency, government or other body speaking as itself, or through a spokesperson the article does not name ("Nvidia said", "a spokeswoman for the Commerce Department said", "the White House declined to comment")
  - `document`: a document, record, filing, dataset, memo or published statement the article cites as the source ("according to trade records obtained from ImportGenius", "according to the prospectus", "documents viewed by The Times")
  - `own_observation`: what the article says its own reporters saw, visited, checked or found themselves ("recent checks by The New York Times found")
  - `other_outlet`: another news organization's reporting ("The Wall Street Journal reported")
  - `unnamed`: people the article does not name and who are not speaking for an institution on the record: "people briefed on the surveillance", "U.S. officials", "a person with knowledge of the matter", "five people who worked at the company", "analysts"; later references to them ("the people said", "they said") are also `unnamed`
- `source`: the article's own words for the source at that place, copied character for character as one unbroken run of the text, at most 20 words (for example "people briefed on the surveillance", "Mr. Rizzo", "trade records obtained from ImportGenius")
- `quote`: one unbroken run of the article text, copied character for character, at most 35 words, that contains the source words and the attributing words (for example "people briefed on the surveillance said")
- `topic`: exactly one of `intelligence_and_relationship` (the intelligence assessment, the surveillance, the memo's contents, the relationships), `government_handling` (what officials, agencies or Congress knew, said, did or decided, export approvals included), `company` (statements and actions of Nvidia, its board or its chief executive; governance; succession), `business` (markets, finance, the industry, another company's stock offering), `background` (biography, history, scene-setting)
- `anonymity_reason`: for `unnamed` only: the article's own words for why the source is not named, copied character for character as one unbroken run, at most 35 words (for example "who spoke on the condition of anonymity because the findings are drawn from classified intelligence"); empty if the article gives none at that place

Counting rules:
- One line per attribution instance. A sentence that says "X said" once is one line. A quotation that runs over several sentences under one attribution is one line. A sentence that attributes to two different sources gets two lines.
- If the same source is attributed again in a later sentence, that is a new line.
- A sentence such as "The account is based on interviews with people briefed on the surveillance" is one `unnamed` line.
- Do not count captions, photo credits, bylines, reporter biographies, corrections or page furniture.

Then exactly one closing line per article: `{"id": "<article id>", "role": "page_done", "n": <number of attribution lines you wrote for it>}`.

## Rules
- **Only what the article says.** Nothing from memory, nothing from another article, nothing looked up.
- **Character for character.** `source`, `quote` and `anonymity_reason` must each be findable in the article's `text` as an exact substring after collapsing runs of whitespace to one space. Keep the text's own quotation marks, apostrophes, dashes and letter forms exactly as they are. Do not join two passages with an ellipsis. Do not let a run cross a page header. Before you close an article, run a check of your own over its lines and fix any line that fails.
- **Never guess who an unnamed source is**, and do not merge unnamed sources: write each instance as the article has it.
- **No judgments.** Do not say whether a source is reliable or an attribution adequate. No adjectives of your own.
- Do not write into any folder but this one.

## Resume
If `out/attributions.jsonl` already has a `page_done` line for an id, skip that article. Append only; to correct a line, append a line with the same `id` and `n` plus `"replaces": true`.

## Report
When every article has its closing line, write `out/REPORT.md`: for each article, the number of lines by `source_type`; totals; anything you declined or could not do. End with one line: `attributions: complete` or `attributions: incomplete <reason>`. Your final message is that same line.
