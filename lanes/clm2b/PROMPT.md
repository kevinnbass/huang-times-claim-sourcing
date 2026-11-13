# Task: for 79 listed attributions, say whether the source itself states a proposition or only comments on it

Owner: the session that built the figure, 2026-11-13.

You are running headless in the folder lanes/clm2b. Work only inside it, and do not read any other lane's folder. Do not use the network at all: everything you need is in `shards/`.
This is for a private research project on how one news story was reported (the Nvidia chief executive's resignation, Oct 29 to Nov 12, 2026). Nothing here is published. A second reader is doing the same task separately; the two will be compared line by line.

## Input
- `shards/articles.jsonl`: eleven articles, one JSON object per line: `id`, `title`, `date`, `text`. The text is a PDF text layer: page headers, photo credits and newsletter prompts are mixed in. Ignore them.
- `shards/lines.jsonl`: 79 attributions found in those articles, one per line: `id` (the article), `n` (its running number within the article, in reading order; numbers are not consecutive because this is a subset), `source` (the article's words for the source), `quote` (the article's words containing the source and the attributing words) and `proposition` (a statement that earlier readers filed this attribution under, as supporting it). The list is fixed: do not add, drop or renumber lines.

## What to do
Read each article in full. For every listed line, find the place in the article, read what the source is reported as saying or showing there, and decide one thing: `mode`. Append one JSON line per attribution to `out/modes.jsonl` with the keys `id`, `n`, `role` (always `mode`), `mode`, `statement`.

### `mode`: exactly one of
- `states`: at this place the source itself is reported as stating the proposition: saying it, concluding it, determining it, believing or suspecting it, admitting or confirming it, or (for a document, surveillance or intelligence) showing it. A restatement of an earlier news report that stated the proposition is also `states`. It need not be the proposition's exact words; it must be the source's own assertion that the thing is so.
- `comments`: the source does not itself state the proposition at this place. It reacts to it, takes it as given, explains why such a thing would be plausible or what would follow from it, gives general background, or says something else. An outside analyst's general remark and a politician's reaction to the reports are `comments` unless the person is reported as asserting, as their own statement, that the thing is so.

Decide from the words the article gives the source at that place, not from who the source is and not from what other places in the article say.

### `statement`
The article's own words for what the source says or shows at that place: one unbroken run of the article text, copied character for character, at most 40 words, not crossing a page header.

Then exactly one closing line per article that has listed lines: `{"id": "<article id>", "role": "page_done", "n": <number of mode lines you wrote for it>}`.

## Rules
- **Only what the article says.** Nothing from memory, nothing from another article, nothing looked up.
- **Character for character.** `statement` must be findable in the article's `text` as an exact substring after collapsing runs of whitespace to one space. Before you close an article, run a check of your own over its lines and fix any that fail.
- **Your own judgment on every line.** Scripts may load and print text and check your output, but must not assign `mode` by keyword.
- **No judgments of reliability or truth.** Whether the proposition is true is not the question; only whether this source, here, states it.
- Do not write into any folder but this one.

## Resume
If `out/modes.jsonl` already has a `page_done` line for an id, skip that article. Append only; to correct a line, append a line with the same `id` and `n` plus `"replaces": true`.

## Report
When every article has its closing line, write `out/REPORT.md`: counts of `mode` by proposition; any line you found hard to decide, with its number and one sentence on why. End with one line: `modes: complete` or `modes: incomplete <reason>`. Your final message is that same line.
