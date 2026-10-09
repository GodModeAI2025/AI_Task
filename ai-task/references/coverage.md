# Delivered scope and boundaries

AI Task ist ein eigenständiger Aufgaben-Wissensraum mit Gesprächsbedienung und portabler Dateispeicherung.

| Capability | This delivery |
|---|---|
| OKR goals and reviews | Objectives, measurable KRs, evidence-linked immutable measurements, task/project links, check-ins and closeouts |
| OKR scoring | Increase/decrease/binary, raw and clamped progress, complete-only average, confidence and freshness separately |
| Conversational task capture, processing and updates | Skill + deterministic Python helpers |
| Areas, projects, headings, tags, task checklists | Stable IDs, validated relations |
| Schedule, deadline, evening, someday | Separate fields, exact local dates |
| Inbox/Today/Upcoming/Anytime/Someday/Logbook/Trash | Read-only queries and offline HTML |
| Project and area views | Scoped task groups and completion counts |
| Complete, cancel, log, trash, restore | Explicit transitions, no hard deletion |
| Repeating templates | DAILY/WEEKLY/MONTHLY, INTERVAL, weekly BYDAY; explicit catch-up |
| Source-linked knowledge | Registered faithful text, claims with locator, task/project links |
| Search | Case-insensitive substring across all records; browser task/knowledge card filter |
| Preview, concurrency and rollback | Hash-bound plans, one local writer, immutable generations, immediate-parent undo |
| Import/export | Documented JSON bundle, ID upsert, unknown fields refused |
| Frozen skill | Verified full dated snapshot and read-only skill instructions |
| Distribution | Standalone .skill ZIP and SHA-256, Python-only checks |

No running web server, account system, API-key storage, SSE, multiuser permissions, drag-and-drop editing, rich text editor, phone notifications, live things API/SQLite migration, mail/calendar connection, background jobs or per-view custom ordering. No CSV/XLSX import in this delivery. No full RFC 5545 parity. No automated evidence-quality judgment, cryptographic signature or hostile-filesystem protection. No OneDrive/SharePoint distributed lock or sync-state guarantee.

Views intentionally differ from the source server: reads never spawn templates or auto-log; due deadlines also surface in Today; dates are day strings; project/area groups include logged tasks for accurate completion counts. Records in a completed project remain visible until explicitly changed. Imported field values remain unmodified. Built-in HTML labels are German; conversation language follows identity, but multilingual browser rendering is not implemented.

A structurally verified claim is not necessarily true. Actor/origin are per generation, not authenticated identities. History retains old text including previously removed confidential values; soft deletion is not GDPR erasure. Plan and export files can contain the same private data as the space. No history pruning or secure erasure tool is included.
