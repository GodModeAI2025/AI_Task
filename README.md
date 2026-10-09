# AI Task

**Deine Aufgaben beginnen mit einem Gespräch. Ihr Kontext bleibt als Wissen erhalten.**

Du sagst deinem Agenten, was du erreichen möchtest. AI Task ordnet Aufgaben, Bereiche, Projekte und nächste Schritte in einem portablen Wissensraum. Entscheidungen bleiben mit ihren Quellen verknüpft. Eine lokale Browseransicht gibt dir Überblick; der Agent übernimmt Änderungen.

AI Task ist ein eigenständiger, lokal ausführbarer Aufgaben-Wissensraum.

[Ausführlicher Plan](docs/PLAN.md) · [Skill](ai-task/SKILL.md) · [Paket](dist/ai-task.skill) · [Prüfsumme](dist/ai-task.skill.sha256) · [Landingpage](https://godmodeai2025.github.io/AI_Task/) · [Offline-Demo](docs/demo.html) · [Funktionsgrenzen](ai-task/references/coverage.md)

## Was du bekommst

- Eingang, Heute, Demnächst, Jederzeit, Irgendwann, Logbuch und Papierkorb.
- Bereiche, Projekte und Überschriften; Checklisten, Tags, Plantermine, Deadlines und Abendaufgaben.
- Wiederholungsvorlagen für Tage, Wochen und Monate, mit ausdrücklicher Nachholung fälliger Aufgaben.
- OKR-Ziele, messbare Key Results und belegte Messpunkte; Fortschritt, Zuversicht und Aktualität getrennt.
- Wöchentliche Check-ins und Abschlussreviews mit verknüpften nächsten Aufgaben.
- Aufgabenwissen mit registrierten Quellen, Aussagen, Belegstellen und Verknüpfungen zu Aufgaben oder Projekten.
- Vorschauen, Hashprüfung, lokale Schreibsperre, unveränderliche Versionsstände und Rückgängig-Funktion.
- JSON-Import/Export und ein eingefrorener, abfragbarer Wissens-Skill zum Weitergeben.
- Ein installierbares Agent-Skills-Paket mit Python-Laufzeit ohne zusätzliche Python-Bibliotheken.

## Starten

Du brauchst einen Agenten mit Skill- und Dateizugriff, Python 3.9+ sowie IANA-Zeitzonendaten (auf macOS/Linux üblich). Öffne oder entpacke das ZIP-Paket `dist/ai-task.skill` und installiere den enthaltenen Ordner `ai-task` im Skill-Verzeichnis deines Agenten, beispielsweise `~/.codex/skills/` oder `~/.claude/skills/`. Die Prüfsumme gehört zum selben Repository-Stand. Starte anschließend eine neue Agentensitzung.

Sag deinem Agenten:

> Nutze ai-task. Lege in meinem ausgewählten Ordner einen Aufgaben-Wissensraum an. Ich plane meine Arbeit auf Deutsch, Zeitzone Europe/Berlin. Zeig mir zuerst den Vorschlag für Zweck, Identität und Regeln.

Der Agent klärt die fehlenden Angaben und zeigt den konkreten Vorschlag vor dem Anlegen. Deine echten Aufgaben werden nicht mit Beispieldaten vermischt. Die Helfer bedient der Agent; du beschreibst dein Anliegen.

| Du sagst | AI Task macht daraus |
|---|---|
| „Halte fest: Lieferanten anrufen.“ | eine unzugeordnete Aufgabe im Eingang |
| „Plane sie morgen im Launch-Projekt.“ | einen konkreten Plantermin und eine Projektzuordnung |
| „Was muss heute passieren?“ | Aufgaben mit Terminen, Deadlines und offenem Kontext |
| „Das Briefing ist erledigt.“ | eine nachvollziehbare Statusänderung |
| „Jeden Montag das Projekt prüfen.“ | eine Wiederholungsvorlage mit bestätigtem Startdatum |
| „Warum machen wir das?“ | eine Antwort aus dem verknüpften Wissen mit Belegstelle |
| „Mach die letzte Änderung rückgängig.“ | eine Vorschau des vorigen Inhalts als neuer Stand |
| „Gib diesen Wissensraum als Skill weiter.“ | einen geprüften, datierten Snapshot mit Abfrageanleitung |

## Deine Dateien bleiben nachvollziehbar

Ein Versionsstand enthält `records/` für Aufgaben und Struktur, `wiki/` für belegtes Wissen, `sources/` für Quelltext, `schema/` für Regeln und `graph/index.html` für die Ansicht. Die abgeschlossenen Stände liegen unter `meta/generations/`; `meta/CURRENT` zeigt auf den aktiven Stand. Bei einer Änderung entsteht erst ein vollständiger neuer Stand, dann wechselt der Zeiger atomar. Die Laufzeit prüft alle Dateien gegen ihren erwarteten Inhalt.

Markdown ist lesbar, aber Änderungen erfolgen über den Skill. Direkte Bearbeitung kanonischer Dateien wird als Integritätsfehler erkannt. Der Verlauf bewahrt auch frühere private Werte; Papierkorb ist keine sichere Löschung. Dateiberechtigungen bleiben deine Verantwortung.

## Demo ansehen

Lade dieses Repository herunter und öffne `docs/demo.html` lokal. Es enthält ausschließlich **synthetische** Beispiele, keine echten Aufgaben. Die Datei funktioniert offline, auch ohne Python oder laufenden Server. Der vollständige Beispielraum liegt in `examples/demo/`. Die Ansicht ist schreibgeschützt; Suche und Navigation funktionieren im Browser. Terminansichten zeigen den Stand vom **9. Oktober 2026**, nicht automatisch den heutigen Tag.

## Grenzen

Kein gehosteter Dienst, keine Anmeldung, Live-Synchronisierung oder Hintergrundjobs. Ansichten bearbeiten keine Aufgaben. Die Wiederholung deckt eine dokumentierte RRULE-Teilmenge ab. JSON-Import erwartet das AI-Task-Bundle, keine beliebige things-API-/SQLite-Datei. Sperren gelten lokal, nicht verteilt über OneDrive oder SharePoint. Der Skill verschickt keine Daten; was dein gewählter Agent verarbeitet, hängt von seinem Anbieter und deinen Einstellungen ab.

Die Browserbeschriftung ist Deutsch. Sprache und Ton deiner Antworten können durch die Identität festgelegt werden. [Vollständiger Vertrag](ai-task/references/contract.md) und [Abdeckung](ai-task/references/coverage.md).

## Entwickeln und prüfen

`python3 tools/check.py` prüft die Regressionstests, Skillreferenzen, Beispielintegrität und reproduzierbare Paketierung. `python3 tools/package.py` baut das Paket und seine SHA-256-Datei. Beides läuft ohne Netzwerk. Temporäre Testdaten bleiben unter `work/` und werden nach erfolgreichen Testfällen entfernt.

[Quellenanalyse](docs/SOURCES.md) dokumentiert die exakt gelesenen Commit-Stände. [Abnahme](docs/VALIDATION.md) hält die lokalen Nachweise und verbleibenden Grenzen fest.

Apache License 2.0. Siehe [LICENSE](LICENSE), [NOTICE](NOTICE) und [Drittanbieterhinweise](THIRD_PARTY_NOTICES.md).

## Ziele & Wirkung mit OKR

„Lege für dieses Quartal ein Ziel für verlässliches Onboarding an. Die Erfolgsquote soll von 40 auf 80 Prozent steigen.“ Der Agent klärt Messmethode, Verantwortlichen und Zeitraum. Messungen brauchen Quelle und Belegstelle. Erledigte Aufgaben erhöhen den OKR-Fortschritt nicht automatisch.

Die [Demo](https://godmodeai2025.github.io/AI_Task/demo.html#okr) zeigt ein zusammenhängendes synthetisches Projekt: drei KRs mit Messverlauf und 46,7 % Fortschritt, ein ambitioniertes Lernziel mit Messlücke und einen abgeschlossenen Pilot mit binärem Ergebnis und Abschlussreview. Fehlende Werte bleiben unbekannt. Alte Räume werden über die nächste bestätigte Änderung migriert; ihre bisherigen Versionsstände bleiben erhalten. [OKR-Vertrag und Berechnungen](ai-task/references/okr.md) · [Umsetzungsplan](docs/OKR-PLAN.md).
