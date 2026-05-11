# Contributing to Awesome Machine Learning

Thanks for helping improve this machine learning resource list. This repository
is a curated Markdown index organized by language and resource type, so
contributions should keep the list accurate, useful, and easy to scan.

## Setup

1. Fork the repository and clone your fork.
2. Create a branch for your change:

   ```bash
   git checkout -b docs/update-ml-resource
   ```

3. Edit `README.md` or one of the companion resource files such as `books.md`,
   `courses.md`, `blogs.md`, `events.md`, or `meetups.md`.
4. Preview the Markdown locally before opening a pull request.

No package install or build step is required for normal documentation updates.
The script under `scripts/` is only for regenerating R package entries and is
not needed for routine list edits.

## What to Contribute

Good contributions include:

- Machine learning frameworks, libraries, tools, datasets, books, courses,
  blogs, events, and meetups.
- Corrections for moved repositories, stale project names, or broken links.
- Clearer descriptions for existing entries.
- Deprecation notes for projects that are explicitly unmaintained or have not
  been updated for several years.

Avoid adding:

- Affiliate links, promotional copy, or sponsored blurbs.
- Duplicates of resources that already appear in the list.
- Projects unrelated to machine learning, data science, or supporting tools.
- Links that do not resolve or only point to placeholder pages.

## Entry Style

Use the existing list format:

```markdown
* [Project Name](https://example.com/project) - Short, factual description.
```

Keep descriptions concise and neutral. Mention the language, framework family,
or machine learning task when it helps readers compare similar resources.

## Organization

- Put new libraries in the correct language and topic section.
- Put learning material in the companion file that matches the resource type.
- Keep the Markdown table of contents in sync if you add or rename headings.
- Preserve existing deprecation wording when updating deprecated entries.

## Validation

Before opening a pull request, run:

```bash
git diff --check
```

Also manually verify that any new or changed links open successfully. For
larger link updates, `curl -I <url>` is enough to confirm that the target
responds.

## Pull Request Guidelines

When opening a pull request:

- Explain what changed and why.
- List any links you added, removed, or fixed.
- Note how you checked the Markdown or links.
- Keep unrelated formatting changes out of the same PR.

Small, focused pull requests are easier to review and merge.
