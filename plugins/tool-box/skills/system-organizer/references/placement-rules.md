# Placement rules

These rules were distilled from an iterative reorganization of a real agent library. The reusable lesson is clear ownership and restrained scope. The source team's business, tools and exact directory names are not required.

## Choose by purpose

| Material | Natural home | Reason |
| --- | --- | --- |
| Approved strategy, positioning, audience, offer boundaries | Shared knowledge | Several workflows must make consistent decisions |
| Editorial, brand or measurement rules used across capabilities | Shared knowledge | One rule should not drift across copies |
| A bounded reusable procedure | Skill entry point | Describes when to use it and how to reach the outcome |
| A focused action users request directly | Command-like entry point | Gives convenient access without duplicating the procedure |
| Specialist method, tool/API notes, profile or curated example | Owning skill's references | Load it only when that procedure needs it |
| Deterministic executable helper | Owning skill's scripts | Keep executable behavior distinct from guidance |
| Input fixture or demonstration image | Owning skill's references by default | It teaches or verifies the procedure rather than recording live work |
| Runtime asset required by a loader or packaging contract | Existing required location | Function and compatibility outweigh cosmetic flattening |
| CRM/CMS records, meetings, campaign plans, reports, finished copy | User's operational system | These are live records and outputs, not canonical instructions |
| Empty reusable template | Shared knowledge or owning references | Place by actual users, separately from completed copies |
| Old baseline, rollout calendar or consolidation log | Operational history | Preserve provenance without loading it as current policy |

A repository can itself be the chosen system of record. Confirm the user's boundary instead of assuming operational data must always be remote. For a guidance-only repository, do not import and continuously synchronize business data into it.

## Shared versus specialist

Ask: do multiple workflows own decisions governed by this rule, or does one specialist own the contract?

- ICP used for sales, content and search belongs in shared strategy.
- A general prose-editing rule used by several workflows belongs in shared writing guidance.
- A search provider's request parameters belong beside the search skill.
- Another skill consulting a blog output profile does not create a second owner. Keep that format contract with the writing skill.
- Do not promote a specialist reference into knowledge merely because several links point to it or because another skill delegates that specialist task.

## Skills and shortcuts

Name broad capabilities by their outcome: Content, Sales, Search or another vocabulary the user understands. Do not invent an umbrella department whose only job is routing to obvious specialists. A naming suffix such as Studio is optional and local.

A short skill may be valuable. A command-like action may still have complex modes. Preserve behavior when changing its presentation. A focused action can be a small portable skill if that is how the supported hosts expose shortcuts. Do not reintroduce separate command files when the project already uses one shared skill tree across platforms.

Keep one implementation behind a broad mode and its shortcut. Separate provider manifests and lightweight adapters are acceptable when required; duplicated provider-specific procedures are not a default architecture.

## Minimal nesting

Start with `SKILL.md`, a flat `references/` for named profiles/examples/guides, and `scripts/` when executable helpers exist. Prefer descriptive filenames such as `blog-profile.md`, `offer-workflow.md`, or `example-report.md` over stacked `references/examples/blog/` folders.

Flatten only when it improves navigation without breaking required asset paths, loaders or a large collection's useful grouping. Shared brand assets need not move into one studio. Do not create empty folders to satisfy a template.

## Canonicality and evidence

An approved strategy outranks abandoned research and historical performance prescriptions. Code establishes implementation facts, not the user's business priorities. A dated observation is evidence with a period and limits, not a permanent posting quota, mandatory CTA or disqualification rule.

Keep concise reusable messaging in Brand or strategy. Full homepages, profiles and client offers belong with the operational record or deployed source. Curated teaching examples can remain beside a skill when their instructional purpose is explicit; do not accumulate every published piece as an example.

Remove irrelevant or conflicting personal-profile material only after checking dependencies and recoverability. Do not preserve an obsolete framework merely to avoid deleting a file, and do not erase its unique historical evidence merely to tidy a folder.

## Generalize a conversation

Extract the decisions, their reasons, corrections and boundaries. Classify them:

- General: one canonical procedure, actual dependency inspection, progressive loading, repair consumers when moving files, preserve useful behavior.
- Local preference: names, exact folder categories, flattening conventions, chosen operational platform.
- Historical/operational: client facts, metrics, rollout dates, drafts, old stack descriptions.
- Host-dependent: command exposure, manifest shape, installation steps, tool names.

Turn general rules into the method, local preferences into defaults to discover, and host-dependent details into checks against the existing system. Omit private names, prices, IDs, client records and absolute author paths from a shareable skill unless they are explicitly required and approved.
