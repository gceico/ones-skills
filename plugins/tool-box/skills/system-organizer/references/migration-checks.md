# Migration checks

Use these when implementation is authorized. Scale the checks to the change; do not create a permanent migration service for a small library.

## Before edits

- Inspect current working-tree changes and relevant history. Preserve unrelated and concurrent work.
- Identify canonical sources and entry points, including consumers outside the folder being moved.
- Inspect the contents, not just names. A candidate may contain unique data or an already-used procedure.
- Choose recovery for deletions: a verified existing copy, version history that actually contains the latest content, or a backup outside the active system. A staged file may differ from the working copy.
- Record a small old-path → new-path map for the current task. Do not create redundant redirect files unless an actual consumer needs them.

## During edits

- Rebase relative links from each file's original location to its destination. Update literal paths, resource IDs, image links, command references, loaders and manifests as well as Markdown links.
- Avoid broad replacements inside captured examples, URLs, citations and source excerpts. Preserve factual content and label any deliberate edits.
- Merge overlapping guidance around the approved decision. Do not leave two competing strategies under cleaner folder names.
- Read final entry points: do they load only relevant references and preserve the expected author, input, output, modes and approval behavior?
- Leave independent plugins' engines and operational state untouched unless changes to them are explicitly part of the task.
- Remove empty obsolete containers after the migration succeeds, not before verifying destinations.

## Verify

- Check local targets and relevant anchors; distinguish real links from template placeholders.
- Search for retired names and paths across instructions, entry points, references, scripts and packaging. Inspect remaining hits rather than blindly replacing all of them.
- Validate the changed skills/manifests with the available host tooling. Retain necessary supported fields rather than stripping them just to satisfy an unrelated validator.
- Exercise changed scripts when paths or behavior were affected. Read representative workflow routes, or run isolated trials if that would establish meaningful confidence.
- Compare retained examples and unique artifacts with their originals. Verify a backup exists before removing the only working copy.
- Check the change set for unrelated edits and accidental new data archives. Stop optional verification when the remaining risk is resolved.

## Useful behavioral cases

Choose cases that match the change. A small system rarely needs all of these:

1. A user requests only an audit: produce findings without moving files.
2. A broad capability and its shortcut: both reach one maintained procedure, preserving special modes.
3. A client record has no verified remote copy: preserve it or prepare a handoff, never report a completed transfer.
4. The project already supports two hosts through one tree: maintain the existing packaging and avoid duplicate procedures.
5. A plugin is missing: provide a useful partial result from supplied material without inventing tool access.
6. A historical framework contradicts the approved direction: remove its authority and repair callers rather than just moving it.

Report local schema/path checks separately from actual workflow, native installation or remote-system tests. If migration is incomplete, list the exact unresolved item and destination needed; do not call the whole cleanup complete.
