# Conversation workflows

## Capture and clarify

“Halte fest: Lieferanten anrufen.” Capture an inbox task with status=null. Do not invent a date. “Plane das morgen im Projekt Launch.” Resolve tomorrow in the agreed timezone, identify the exact project (ask if names collide), then propose active status, listId and scheduledDate. The deadline stays independent.

## Today and review

“Was ist heute wichtig?” Query today and surface deadlines, overdue tasks, evening flags and checklist progress. Read linked knowledge and cite why the task matters when evidence exists. Reading does not spawn repeats or log prior completions. “Mach die Wochenübersicht” combines inbox, upcoming, anytime, someday and unfinished project records; recommend changes as proposals, never silently reschedule.

## Lifecycle

“Erledige die Lieferantenaufgabe.” Find its stable ID and complete it. “Abbrechen” means cancel; “weglegen” may mean someday or trash, so clarify if context does not resolve it. “Ins Logbuch” logs terminal tasks. Restore preserves the status held before task trashing. Project completion leaves unfinished tasks visible; tell the user how many remain. A trashed project's children must be rehomed or trashed within the same explicit plan, otherwise validation refuses it.

## Repeat

“Jeden Montag den Status prüfen.” Create a weekly template, BYDAY=MO, with a confirmed first matching date as nextOccurrence and repeatAnchor. “Lege die jetzt fälligen Wiederholungen an.” Tick explicitly. Review the planned instances; it copies notes/tags/checklists and resets check completion. No scheduler is installed. To stop a template with active instances, keep its source reference intact: move its nextOccurrence into the future or propose an explicit reviewed change to the referencing instances before trashing the template.

## Evidence

“Warum machen wir diese Aufgabe?” Search task notes and linked knowledge. If only a task exists, describe its stored state and say that a supporting decision source is missing. “Das wurde in diesem Protokoll beschlossen.” Register the faithful text using a logical filename or URL and cite the exact paragraph in a new knowledge claim. Add a task/project link. Do not promote suggestions to decisions or infer an unsupported causal relationship.

## Import and undo

Review all IDs and unknown fields first. Produce the AI Task bundle and import-plan, then show insertions and changed fields. Do not say that arbitrary things JSON is supported: API/SQLite adapters are not included. Export is lossless for the documented records. “Mach die letzte Änderung rückgängig.” Show the preceding generation's content as the proposed new state; explain that subsequent changes will also be absent if the user is referring to an older operation. Immediate undo applies to the immediate parent only. History is preserved.

## Frozen knowledge skill

“Gib dieses Aufgabenwissen als Skill weiter.” Check sharing scope and sensitive content, pick an authorized new destination and valid lowercase skill name. Freeze the verified generation and report its date/hash. It includes the complete selected space; per-record redaction is not implemented. If the user wants a subset, prepare a separate reviewed space first. Do not externally publish or install as a side effect.
