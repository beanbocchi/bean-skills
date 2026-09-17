# Catalogue of AI writing tells

Condensed from Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) into
what a writer needs. Each entry says what the habit looks like, why a
model produces it, and what a person writes instead. Examples of the habit sit in
fenced blocks so the checker script skips them.

Sections marked "current" describe habits measured in 2026 output from Claude
models with a strong style prompt. They are not on the Wikipedia list; the older
tells had already been trained or prompted away, and these are what remained.

Contents
1. Content habits
2. Sentence habits
3. Formatting habits
4. Talking to the reader
5. Change descriptions (commits, PRs, changelogs)
6. What a person leaves in
7. Not tells: do not overcorrect
8. The same habits in Vietnamese

## 1. Content habits

### Significance inflation

The subject is made to matter by saying that it matters. Any fact gets a trailer
about its role, legacy, or the broader trend it reflects. This is regression to
the mean: the specific fact is rare in training data, the praise is common, so
the model swaps one for the other.

```text
The department model plays a pivotal role in the portal's governance story,
underscoring ECV's commitment to accountability and reflecting a broader shift
toward responsible enterprise AI.
```

A person states the fact and stops:

```text
Every request is billed to exactly one department.
```

Watch for: stands as, serves as, is a testament to, plays a crucial/pivotal/key
role, underscores/highlights the importance, reflects a broader, marks a shift,
turning point, setting the stage, indelible mark, deeply rooted, evolving
landscape, enduring legacy, focal point, contributing to the.

### Superficial analysis

A sentence ends with a participle clause that tells the reader what the fact
means: ", ensuring...", ", highlighting...", ", fostering...", ", making it...".
The clause adds no information; it is the model narrating its own approval.

```text
Blocks are stored per department, ensuring flexibility while maintaining
control.
```

Cut the clause. If the consequence matters, give it its own sentence with its
own fact:

```text
Blocks are stored per department. A block in Finance changes nothing for Sales.
```

### Slogan closers (current)

A paragraph or section ends on a short, quotable sentence that restates it as a
maxim. It is the modern form of "In conclusion". In five independent drafts of
one page, three ended the same paragraph with the same slogan.

```text
Members already in another department are listed in the confirmation dialog,
because moving them recharges their spend. Nobody's cost moves silently.
```

```text
Groups decide what people may do; departments decide what it costs.
```

The paragraph ends on the fact before the slogan. A closing paragraph that
restates the page is cut whole.

### Reassurance clauses (current)

A fact is followed by a clause telling the reader how it helps them: ", so there
is one place to look", ", so a new model needs no per-department setup", ", so
you never have to think about it". Four or five per page. The participle version
(", ensuring...") is the same habit.

Keep the fact. Add a consequence only as its own sentence carrying a new fact: a
number, a case, a failure.

### Promotional register

Neutral prose drifts toward a brochure: seamless, robust, vibrant, boasts,
showcases, groundbreaking, renowned, enterprise-grade, best-in-class, commitment
to excellence, unlock, empower, elevate, journey, transformative. Newer models
are subtler than older ones: fewer superlatives, same register.

```text
The portal delivers a seamless, secure and scalable experience across a diverse
array of departments.
```

Give the reader the thing they would check:

```text
One sign-in, one budget per department, and every model call in the audit log.
```

### Weasel attribution

Opinions are handed to a crowd nobody can find: experts argue, observers have
noted, industry reports show, it is widely recognised, many teams. Often the
crowd is one source, or none.

Name the source or own the claim: "The July 2025 Economist piece found..." or
"I think...". A claim that allows neither is cut.

### Challenges and future outlook

Long pieces end with a formula: "Despite its strengths, X faces several
challenges..." then a vaguely hopeful paragraph, sometimes under a heading such
as "Challenges", "Future outlook", "Looking ahead", "Conclusion". The structure
is the tell, not the word "challenge".

End when the content ends. If there are open problems, list the actual problems
with owners or dates.

### Notability and coverage

Text about a company or person recites where it was covered ("featured in
leading trade publications", "maintains an active social media presence")
instead of what the coverage said. The content of the coverage is the only part
worth a sentence.

## 2. Sentence habits

### AI vocabulary

Words that spiked after 2022 and cluster together. Where one appears, others
usually follow. Newer models overuse a smaller set than older ones.

Core set: additionally, align with, boasts, bolster, crucial, deep dive, delve,
emphasize, enduring, enhance, foster, garner, highlight (verb), interplay,
intricate, key (adjective), landscape (abstract), meticulous, pivotal, robust,
showcase, tapestry, testament, underscore (verb), valuable, vibrant.

Common companions: seamless, leverage, streamline, comprehensive, holistic,
cutting-edge, empower, unlock, navigate (abstract), realm, paradigm, synergy,
utilize, facilitate, notably, moreover, furthermore, transformative, journey,
granular, unprecedented, "in today's ...", "at its core", "when it comes to".

Take the list literally. "Underscore" the character, "highlight" a line of code
and "landscape" orientation are ordinary words. The tell is figurative use,
several at once.

### Dressed-up copulas

Simple copulas are replaced with dressed-up verbs: serves as, stands as,
functions as, represents, marks, boasts, features, offers, maintains, refers to.
One study measured a 10 percent drop in "is" and "are" in academic writing in
2023.

```text
Gallery 825 serves as LAAA's exhibition space and features four separate
rooms.
```

```text
Gallery 825 is LAAA's exhibition space. It has four rooms.
```

### Vague connection

Two things that have a specific relationship are said to be "associated with",
"connected to", "tied to" or "linked to" each other.

```text
In 2017 Doe was associated with the leadership of ExampleCorp.
```

```text
In 2017 Doe was CEO of ExampleCorp.
```

### Negative parallelism

The text argues with a reader who never said anything: "not just X, but Y",
"it's not X, it's Y", "no X, no Y, just Z", "Y rather than X". It reads as
clearing up a misconception that nobody held.

```text
This isn't just a deployment; it's a shift in how departments work.
```

State Y. If a real reader would believe X, say who believes it and why they are
wrong, in a sentence of its own.

### Two-sentence contrast (current)

The "not just X but Y" reflex survives as two sentences or a balanced pair:

```text
On paper it was a technical deployment. In practice it changed how departments
work.
Compliance is one reason. The bigger one is data sovereignty.
The budget isn't there to stop people. It's there so teams can keep experimenting.
Cost attribution is complete from the moment a user exists, not a setup step an
administrator can forget.
A recharge is confirmed, never discovered.
```

Each contrasts with a belief nobody stated. The second half alone is the
sentence. A contrast stays only when a named person holds the first half, and
the text names them.

### Concession frames (current)

A disagreement opens by granting the other side: "The standup concern is fair:",
"X is a real advantage, but", "I understand why you lean that way, but". In
Vietnamese: "là lợi thế thật, nhưng". The frame softens; it adds nothing the
reader can check, so the disagreement and its reason open the paragraph.

### Rule of three

Adjectives, phrases and bullets come in threes by reflex: "secure, scalable and
seamless", three bold bullets, three examples. Three feels complete, so the
model pads or trims to reach it.

A list holds what exists, whether that is two items, four, or exactly three.

### Elegant variation

The same thing is renamed each time it appears (the portal, the platform, the
solution, the system) because older models were penalised for repetition. A
person calls a thing by one name and repeats it.

## 3. Formatting habits

Title Case Headings: capitalising every main word. Sentence case is the human
default outside American newspaper headlines.

Bold sprinkled for emphasis, often the same word bolded each time it appears.
Bold belongs on a UI label the reader must find or a term at its definition,
and rarely more than once per screen.

Bold-header bullets: "- **Label**: explanation", a listicle skeleton. If the
items are parallel and short, a plain list works. If each needs a sentence of
explanation, write a paragraph.

Em dashes with spaces around them, doing the work of commas, colons and
parentheses. Use those instead. Curly quotes and apostrophes where straight ones
are expected. Emoji as bullets or heading decorations. Thematic breaks (---)
between every section. Tiny tables for two rows of facts that read better as a
sentence. A heading that contains only other headings. Skipped heading levels. A
heading repeating the document title above the first paragraph.

## 4. Talking to the reader

Chatter that belongs in a chat window, not in a document: "I hope this helps",
"Certainly!", "You're absolutely right", "Would you like me to...", "Let me
know", "Feel free to", "Here's a breakdown", "Let's dive in", "Happy coding".

Didactic notes: "It's important to note that", "It's worth noting", "Keep in
mind". Delete the frame and keep the fact; if the fact was not worth a sentence
on its own it was not worth noting.

Signposting (current): a sentence about the text instead of the subject. "This
page answers the question finance asks first", "that's what this post is about",
"the part worth writing about", "One thing worth saying plainly:", "The budgets
deserve a word", "One more thing, and it matters", "Three things stood out. The
first is...", "Short answer:", "Quan trọng nhất:". The announcement goes; the
thing announced stays.

Section summaries: "In summary", "In conclusion", "Overall", a closing paragraph
that restates the opening. Stop when the content stops.

Knowledge disclaimers and speculation about missing sources: "While specific
details are limited...", "based on available information", "as of my last
update". Say what is known, say what was not checked, no padding between.

Placeholders left in: [Company Name], (add link here), 2025-xx-xx.

## 5. Change descriptions

Commit messages, PR descriptions and changelogs written by models follow a
template that human summaries almost never use:

Canned assurance: "improved clarity, flow and readability", "ensures
consistency", "follows best practices", "for better maintainability".

Procedural negatives: "while preserving existing behaviour", "without breaking
changes", "retained all tests", "avoided modifying X". Nobody describes what
they did not do unless asked.

Emphasis on the presence of things instead of their content: "added
comprehensive tests", "added sourced documentation", "updated relevant files".

Parameter recitals: listing every flag, field and file touched with its markup.

A person writes what changed and what the reader must now do differently:

```text
Model access is a block list per department. Existing grants become blocks for
the complement; run the backfill before deploying.
```

### Rewrite as paraphrase (current)

Asked to make a draft "sound human", a model removes the em dashes, bold and
buzzwords and keeps everything else: the paragraph order, the weasel claim in
folksier words ("most people in this industry will tell you"), the puffery label
("responsible, enterprise-grade AI"), the vision closer ("the direction we're
heading"). Five of five rewrites of one blog draft kept all four. A rewrite
starts from the extracted facts, drops what has no source or number, and puts
the facts in the reader's order.

## 6. What a person leaves in

Measured across 25 years of Wikipedia, these are more common in human text than
in model text, and worth keeping:

Simple is, are, has, there is. Plain verbs: wrote, moved, used, tried, died,
not authored, relocated, utilized, attempted, passed away. Definite statements:
the first, the only, the best, when true. Honest hedges and intensifiers: very,
perhaps, probably, tends to. Ordinary wordiness: as a result of, in order to,
the fact that. Repeating the same noun. Sentences of very different lengths.
Saying "I" when it is your opinion. A specific number where a model would write
"significant".

## 7. Not tells: do not overcorrect

Perfect grammar is not a tell. Formal or academic register is not a tell; only
the specific words above are. Transition words are not a tell in isolation.
Mixed casual and technical register is normal for engineers. Markdown is normal
for developers. A single em dash or one "however" proves nothing. Detectors and
humans alike misjudge single texts; the signal is density and co-occurrence.

## 8. The same habits in Vietnamese

The structures carry over even though the vocabulary differs. In Vietnamese
replies watch for:

Contrast reflex: "không chỉ ... mà còn ...". Significance: "đóng vai trò quan
trọng / then chốt", "là minh chứng cho", "bước ngoặt", "dấu ấn". Summaries and
frames: "Tóm lại", "Nhìn chung", "Cần lưu ý rằng", "Điều quan trọng là".
Chatter: "Hy vọng thông tin này hữu ích", "Bạn có muốn mình...", "Hãy cho mình
biết nếu cần thêm". Brochure words: nâng cao, tối ưu hóa, toàn diện, mạnh mẽ,
liền mạch, hệ sinh thái, bức tranh toàn cảnh, tận dụng, đột phá, trải nghiệm
liền mạch, "một cách hiệu quả". Padding connectors at sentence starts: "Bên
cạnh đó", "Ngoài ra", "Hơn thế nữa", "Trên thực tế".

Frames measured in 2026 replies: "Câu trả lời ngắn:" as an opener (four of
five replies), "X là lợi thế thật, nhưng" before every disagreement (five of
five), "Quan trọng nhất:" before the main point (four of five), "Không phải vì
X, mà vì Y", and a slogan closer such as "Chạm một trong hai thì mở lại câu
hỏi".

A person answering in Vietnamese says the conclusion first, gives the two or
three facts that carry it, names the number that decides, and stops.
