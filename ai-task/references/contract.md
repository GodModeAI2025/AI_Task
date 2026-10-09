# Contract and internal runtime

The runtime is `scripts/task.py` relative to the loaded skill. It uses only Python standard library. These commands are for the agent; conversational requests are the user interface.

## Storage

```
<room>/meta/CURRENT                         active generation SHA-256
<room>/meta/generations/<sha256>/
  SOUL.md                                 agreed identity
  WIKI.md                                 entrypoint
  schema/settings.json
  schema/CONTENT_POLICY.md                 preserve / disclose / soft-delete-only
  state.json                              structured snapshot
  records/{area,project,heading,task,tag}/<id>.md
  wiki/<knowledge-id>.md                   claims and record links
  sources/<source-id>.md                   faithful text and logical reference
  graph/index.html                        generated read-only offline browser
  manifest.json                           exact file hashes
<room>/.ai-task.lock/                      transient local exclusive writer lock
```

Every published generation is immutable by convention and checked on each read. CURRENT changes atomically after generation validation. A reader captures it once. Markdown and state.json must exactly agree; edits to either are refused. JSON-object frontmatter is valid YAML 1.2 and supports arrays without a YAML library. Open the Markdown directly to inspect; use the runtime to change it. There are no root-level mutable record mirrors. Hashes detect accidental alteration, not a hostile actor able to rewrite the entire space and pointer. Filesystem permissions remain the host's responsibility.

Local mkdir lock coordinates cooperating writers on the same filesystem. It is not a OneDrive/SharePoint distributed lock. Process interruption before pointer replacement leaves the prior generation readable. A hard power failure has filesystem-dependent durability; no distributed/power-loss guarantee is made. Staging remnants and stale locks are never automatically broken. History grows without pruning. Undo republishes the immediate parent's content as a new generation; it is not a multi-level cursor or an external side-effect reversal.

## Inputs and fields

Identity JSON has exactly purpose, audience, language, timezone (IANA), tone, boundaries, all nonempty strings. Policy is fixed: preserve history, disclose conflicts, soft deletion only.

Records require id and title. IDs: area_, prj_, hdg_, tsk_, tag_, src_, knw_ followed by 1–100 ASCII letters/digits/underscore/hyphen. Common fields: notes, position, createdAt, updatedAt, trashedAt. Dates are YYYY-MM-DD, not instants; provenance is per generation. actor, origin, operation, date and parent form that generation's event. This intentionally simplifies things' millisecond timestamps.

| Kind | Additional fields |
|---|---|
| area, tag | none |
| project | areaId, status (active/completed/trashed), completedAt |
| heading | projectId (required), isBacklog |
| task | status (null/active/completed/cancelled/trashed), isSomeday, scheduledDate, deadline, isEvening, listId, headingId, isTemplate, rrule, nextOccurrence, repeatAnchor, templateId, completedAt, isLogged, tags (tag IDs), checklist, previousStatus (trash bookkeeping) |
| source | reference (portable logical reference or URL), text (faithful source text) |
| knowledge | claims (nonempty), recordIds |

Checklist item: `{ "id": "chk_read", "title": "Read", "completed": false }`. Claim: `{ "text": "Decision text", "sourceId": "src_meeting", "locator": "Section 2, paragraph 1" }`. recordIds link to any known record. Structural validity is not evidentiary quality.

Dates and flags are checked. References must exist; active task/container references may not target the trash. There is no implicit cascade. Unknown record fields are rejected. Do not silently map an unfamiliar things API response to this schema. There is no implicit authentication or userId table.

## Commands

Use `python3 <skill-root>/scripts/task.py <command> --room <authorized-room>`. Choose the equivalent Python 3.9+ launcher on Windows. Resolve all input/output paths transiently; never persist machine-specific paths.

| Command | Extra inputs | Result |
|---|---|---|
| init-plan | --input identity.json, optionally --today | full proposal, no room writes |
| plan | --input actions.json --today YYYY-MM-DD --actor agent/name --origin USER_REQUEST | hash-bound proposal |
| import-plan | --input bundle.json --today YYYY-MM-DD --actor agent/name | upsert proposal, preserving timestamps |
| preview | --input proposal.json | full before/after, identity, policy and hash |
| apply | --input proposal.json --expect-sha256 HASH | verified generation; zero writes for stale/tampered plan |
| query | --view VIEW --today YYYY-MM-DD, optionally --scope ID | task records |
| search | --term TEXT | matches across data, sources and knowledge |
| verify | none | verified active generation and event |
| export | none | ai-task-bundle/2 JSON |
| freeze | --destination NEW_DIRECTORY --name knowledge-name | read-only skill with verified snapshot |

For JSON output use --output FILE outside the canonical room, otherwise stdout. Plans contain complete proposed content; keep them in an authorized private staging location. Show previews via the agent, not raw command tutorials. Delete temporary plans after use according to the host's authorized cleanup rules. CLI errors return status 2 and an error JSON; a failing command is not successful delivery.

Actions are an array, maximum 10,000 entries. Formats:

```
{"op":"upsert","kind":"task","record":{"id":"tsk_call","title":"Call","status":"active","scheduledDate":"2026-10-09"}}
{"op":"complete","id":"tsk_call"}
{"op":"cancel","id":"tsk_call"}
{"op":"log","id":"tsk_call"}
{"op":"trash","kind":"task","id":"tsk_call"}
{"op":"restore","kind":"task","id":"tsk_call"}
{"op":"complete","kind":"project","id":"prj_launch"}
{"op":"tick"}
{"op":"undo"}
```

Upsert merges supplied fields with the existing record and validates the entire resulting state; provide null to clear optional dates/references. Unknown action keys are refused. Undo must be the only action. Import is an upsert: absent records are retained, never removed. Conflicting same-ID values overwrite only through the reviewed proposal. Bundle shape: `{"format":"ai-task-bundle/2","records":{"area":{},"project":{},"heading":{},"task":{},"tag":{},"source":{},"knowledge":{},"objective":{},"key-result":{},"measurement":{},"review":{}}}`. Collections are dictionaries keyed by record ID, with full records as values.

RRULE: DAILY/WEEKLY/MONTHLY, optional positive INTERVAL (up to 9999), WEEKLY optionally BYDAY=MO,TU,... . DTSTART is repeatAnchor. nextOccurrence must match the rule. Months without the anchored day are skipped. Tick handles at most 366 total due occurrences per plan and leaves source templates intact. No COUNT, UNTIL, BYMONTHDAY, BYSETPOS or YEARLY; unsupported rules fail before writing.

## OKR and format versions

The active state format is ai-task-state/2, with additional objective, key-result, measurement and review collections. Old /1 generations and /1 bundles remain supported. Read [okr.md](okr.md) for schemas, scoring, review, correction and migration. Query OKR with `okr --today YYYY-MM-DD`; the report is also stored as schema/okr-report.json inside each /2 generation.
