---
name: capturing-doc-screenshots
description: Use when a documentation page (Mintlify or other MDX docs) needs a screenshot of a running web app, when a picture needs highlighted regions or numbered callouts that a step list refers to, or when existing captures must be refreshed after a UI change.
---

# Capturing doc screenshots

## Overview

A screenshot in the docs is produced by a script committed in the repository,
and its callouts are painted into the live page from element locators. The next
UI change reruns the script and every picture comes back, callouts included.

## Before anything else

Look for an existing capture script: the README, and
`grep -rl --exclude-dir=node_modules "screenshot(" .`. If one exists, add a shot
to its list and rerun that one shot. A second script beside it is a second thing
to keep in step.

A first script goes in the package that already depends on Playwright, in its
`scripts/` folder, and runs with the runtime that package uses. When no package
does, it goes in `docs/scripts/` with a `package.json` there naming
`playwright-core` as a dev dependency and a `.gitignore` for its `node_modules`.

## The deliverable

One capture is these five things together:

1. A shot entry in the script's list: name, route, the account to sign in as
   when the app has sign-in, an optional `prepare` that opens the menu or tab,
   and `focus`, the controls to mark in the order the reader uses them.
2. Locators by role and visible name, `getByRole("button", { name: /Save/ })`,
   with a CSS selector only for a control that exposes no name.
3. The overlay painted in the page: `drawFocus` in [annotate.ts](annotate.ts)
   measures each locator and appends a fixed layer holding an outline and a
   numbered badge. Copy that file into the script's folder and import `drawFocus` from it.
4. One image per shot at one fixed viewport (1440 by 900, `deviceScaleFactor: 2`
   so text stays sharp), converted to WebP with
   `magick shot.png -quality 82 shot.webp` and the PNG removed.
5. The MDX that shows it:

```mdx
<Frame caption="What the screen is, in one line.">
  <img src="/images/admin-services.webp" alt="The AI services screen with the key button marked 1 and Use AWS default marked 2" />
</Frame>

<Steps>
  <Step title="Add API key">What the reader does with control 1.</Step>
  <Step title="Use AWS default">What the reader does with control 2.</Step>
</Steps>
```

Step N is badge N. The caption names the screen, the alt text says where the
numbers sit, and the steps carry the instructions. Prose already on the page
about those controls moves into the steps, and a heading that introduced only
one of them goes with it.

## Shot example

```ts
{
  name: "admin-services",
  path: "/admin/services",
  account: "admin",
  prepare: (page) => page.getByRole("tab", { name: "Models" }).click(),
  focus: [
    { step: 1, target: { role: "button", name: /^(Add|Update) API key$/ } },
    { step: 2, target: { role: "button", name: "Use AWS default" } },
  ],
}
```

## Running

- Sign in through the real flow once per account, then open a fresh page per
  shot. A screen holding an event stream leaks across thirty shots on one page.
- Wait for `networkidle` plus a beat for transitions, then paint, then shoot.
- Accept shot names on the command line, so one shot reruns in seconds and a
  full run happens only when the UI changed everywhere.
- Open the image and look at it. Each badge sits on its control and hides no
  label; a badge that would cover the label above a field takes
  `corner: "right"`. A badge on a disabled control gets a sentence in its step
  saying why it is disabled in the picture.
- Run the prose checker over the steps and caption, as for any docs prose.

## Quick reference

| Need | Do |
|---|---|
| A dialog or card rather than the whole screen | `await locator.screenshot({ path })` after painting |
| Sample data that must not ship | `page.screenshot({ mask: [locator] })`, or a `prepare` that rewrites the text |
| A page taller than the viewport | `fullPage: true` with the viewport width unchanged |
| Light and dark variants | Two shots and two `<img>` tags with `className="block dark:hidden"` and `"hidden dark:block"`, only when the site renders both themes |

## Common mistakes

| Mistake | Fix |
|---|---|
| Script written in a temp folder and deleted after the run | The script is part of the deliverable. Commit it beside the docs. |
| `button.primary`, `.danger` | Role and name. Classes are styling and change without notice. |
| Boxes drawn onto the PNG with ImageMagick coordinates | Paint in the page. A coordinate is stale on the next build. |
| Numbers listed in the caption, then "(1)" after words in the prose | One `<Steps>` list, step N is badge N. |
| PNG at whatever viewport the browser opened | Fixed viewport, DPR 2, WebP. |
| Full run to refresh one image | Filter by shot name. |
