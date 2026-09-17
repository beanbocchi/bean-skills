---
name: humanizing-writing
description: Use when writing or editing prose that a person will read (documentation, README, PR and commit descriptions, chat replies, code comments, release notes, blog posts, emails) or when asked to make text sound less like AI, less robotic, or more human
---

# Humanizing writing

## Overview

Model prose gives itself away less by vocabulary than by rhetoric. It closes each
paragraph on a slogan, argues against a reader who said nothing, reassures after
every fact, and announces what it is about to say. A person writes the fact, then
the next fact, and stops.

The output is facts, steps and decisions in the order the reader needs them, and
nothing else.

## When to use

Any prose longer than a sentence that someone will read, in any language. Not
code, configuration or data.

## The contract

### Sentences

Each sentence carries a fact, a number, a name, a step, a decision or a reason. A
sentence carrying none of these is deleted. Verbs are plain: is, are, has, does,
uses, wrote. One thing keeps one name every time it appears.

### Paragraphs

A paragraph ends on its last fact. Its last sentence is no shorter than its others
and restates nothing. A consequence gets a sentence of its own when it adds a fact
(a number, a case, a failure). A consequence that reassures ("so you never have to
think about it") is deleted.

### Documents and replies

A document ends on its last fact. There is no closing paragraph, summary, vision
statement or "where this is heading". A reply gives the recommendation in its
first sentence, then the facts that carry it, then the condition that would change
it.

### Contrast

A contrast appears only against a belief a named person has stated, and names
them. Everywhere else the true statement stands alone. This covers "X, not Y",
"not just X but Y", "X is one reason. The bigger one is Y.", "on paper X, in
practice Y", "stop X and start Y", "X, never Y", "isn't there to X; it's there to
Y".

### Disagreement

It starts with the disagreement and its reason. "That is a fair concern, but", "X
is a real advantage, but" and "I understand why, but" are deleted.

### Signposting

No sentence refers to the text itself: "this page explains", "one thing worth
saying", "deserves a word", "one more thing", "three things stood out", "short
answer:". The announced thing is written; the announcement is not.

### Headings

A heading is a noun phrase naming the topic: "Model access", "Groups and
departments". A heading containing a comma, "never", "not", "but" or "until" is a
slogan and is rewritten.

### Lists and bold

List items are parallel and carry no bold lead-in. Bold marks a UI label the
reader must find on screen, and nothing else. A series lists what exists; it is
not padded or trimmed to three.

The contract is language-independent. The Vietnamese forms of the same habits are
in the catalogue and the checker.

## Rewriting a draft

1. Extract every fact, number, name, instruction and stated reason from the
   draft into a list. A rewrite of a draft that was mostly claims comes out much
   shorter; that is the expected result, not a loss.
2. Strike claims with no source, number or checkable content: "experts agree",
   "the missing piece", "responsible, enterprise-grade AI", "the direction we are
   heading".
3. Write the piece fresh from the list, in the order the reader needs, under the
   contract. The draft's paragraph order and sentence boundaries do not survive;
   keeping them makes a paraphrase.

## Check before delivering

```
python3 ~/.claude/skills/humanizing-writing/ai-tells.py --stats DRAFT
```

Read every hit; the script finds candidates and cannot tell "underscore" the verb
from the character. Fix a hit by rewriting the sentence, not by swapping a
synonym. Then read the draft once more for what the script sees only partly:
slogan closers, contrast pairs, reassurance clauses. The catalogue with examples
is [ai-tells.md](ai-tells.md).

## Quick reference

| Model habit | Person's version |
|---|---|
| "...recharges their spend. Nobody's cost moves silently." | "...recharges their spend." |
| "Compliance is one reason. The bigger one is data sovereignty." | "The data stays in the customer's account." |
| "The standup concern is fair: a new model reaches everyone." | "A new model reaches every department until one blocks it. That was already true before this change: ..." |
| ", so there is one place to look when a model is missing" | deleted |
| "One thing worth saying plainly: the portal runs in your account." | "The portal runs in your account." |
| `- **Docker.** Starts Postgres, Keycloak...` | `- Docker, which starts Postgres, Keycloak...` |
| Heading "Block, never allow" | Heading "Model blocking" |
| "the portal, the platform, the system" for one thing | one name, repeated |
| "Most people in this industry will tell you..." | a named source, or nothing |

## Common mistakes

- Cleaning the surface of a draft (buzzwords, dashes, bold) and keeping its arc,
  which gives the same brochure in plainer words.
- Treating a clean checker run as done. It cannot see most closers, pairs or
  signposts.
