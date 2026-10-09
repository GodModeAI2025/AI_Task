# Ausführlicher Umsetzungsplan: AI Task

Stand: 9. Oktober 2026. Dieser Plan entsteht vor der Implementierung. Zielrepository: ausschließlich GodModeAI2025/AI_Task; das anfangs leere Repository wird unter AI_Task bearbeitet. Referenzrepositories werden nur gelesen.

## 1. Analyse und Ziel

AI_first_CRM (0ce5cef298ae9bb335811366b00d6844b8099bb4) ist kein klassischer Server: Ein Agent bedient einen portablen Wissensraum aus Markdown, strukturierten Datensätzen, Quellen, Verlauf und generierten HTML-Ansichten. Der Skill ist die Bedienoberfläche. Änderungen werden vorbereitet, an Hashes gebunden, unter Schreibsperre angewandt und überprüft. Daten sind von belegten Wissensaussagen getrennt. Identität und Inhaltspolitik werden vor dem Anlegen vereinbart.

things (26095aea1a7ebf7c431477a57e10d1d9c69e933e) ist dagegen eine Web-App mit REST API, CLI, SQLite/Drizzle, Anmeldung und laufendem Server. Fachlich relevant sind Bereiche, Projekte, Projektüberschriften, Aufgaben, Checklisten, Tags und Wiederholungsvorlagen. Aufgaben enthalten status (auch null für Eingang), isSomeday, scheduledDate, deadline, isEvening, listId, headingId, templateId, completedAt, trashedAt und isLogged. Termin und Deadline sind unabhängig. Ansichten: Eingang, Heute, Demnächst, Jederzeit, Irgendwann, Logbuch und Papierkorb. Wiederholung und automatisches Archivieren können dort durch Lesen von Ansichten ausgelöst werden.

**Ziel:** dieselbe Gesprächs- und Wissensraumarchitektur wie AI_first_CRM, mit dem Aufgabenmodell von things. Ein installierbarer Skill und eine offline ausführbare Python-Laufzeit, kein Klon der React-App. Bedienung in natürlicher Sprache, Daten in menschenlesbaren Dateien, reproduzierbare schreibgeschützte Browseransichten. Ein synthetischer Beispielraum macht das Ergebnis sofort prüfbar.

## 2. Erfolgskriterien

- SC01: Paket enthält einen portablen ai-task Skill mit klarer Eingangsregel, Referenzen und ohne Abhängigkeit zu AI_first_CRM.
- SC02: Neuer Raum erhält bestätigte SOUL.md, CONTENT_POLICY.md, Schema, WIKI.md und leere Register; vorhandene Räume werden nicht überschrieben.
- SC03: Bereiche, Projekte, Überschriften, Aufgaben, Tags, Checklisten und belegte Wissensseiten lassen sich mit stabilen IDs erzeugen und aktualisieren.
- SC04: Änderungen tragen actor/origin, Vorschau und Hash; ein veränderter Plan oder Zwischenstand schreibt nichts. Eine lokale Sperre serialisiert konkurrierende Anwendungen. Versionierte unveränderliche Generationsstände und ein atomarer Zeiger verhindern halbe kanonische Transaktionen.
- SC05: Die sieben Hauptansichten, Projekt-/Bereichsfilter, Suche, Abendmarkierung und Deadline-Auswertung sind deterministisch und testen Kalendergrenzen.
- SC06: Erledigen, Abbrechen, Loggen, Papierkorb, Wiederherstellen, Projektabschluss und Checklistenänderungen funktionieren ohne harte Löschung. Undo erstellt eine neue Generation und bewahrt Geschichte.
- SC07: JSON-Import/Export hat Vorschau, Upsert über stabile IDs, Fremdschlüsselprüfung und vollständigen Roundtrip; fremde things-Felder werden nicht stillschweigend weggeworfen.
- SC08: Wiederholungen erzeugen beim ausdrücklichen Aufruf Tages-/Wochen-/Monatsaufgaben mit Checklisten und Tags idempotent; ungültige/komplexere RRULEs werden erklärt und verweigert.
- SC09: Wissen referenziert registrierte Quellen mit Locator, kann auf Datensätze verweisen und ist im Browser und Suchergebnis auffindbar.
- SC10: Releaseprüfung erkennt Manipulation, HTML enthält keine ausführbaren Nutzdaten und benötigt weder Netzwerk noch Server.
- SC11: Paket, Prüfsumme, CI und Regressionstests sind reproduzierbar; README benennt tatsächliche Grenzen und Installation.

## 3. Architektur und Entscheidungen

### Speicherung

Ein Raum besitzt `meta/CURRENT` und unveränderliche Generationen unter `meta/generations/<sha256>/`. Jede Generation enthält `records/<kind>/<id>.md`, `wiki/<id>.md`, `sources/<id>.md`, `schema/settings.json`, `SOUL.md`, `schema/CONTENT_POLICY.md`, `WIKI.md`, `graph/index.html`, `manifest.json` und `state.json`. JSON-kompatible YAML-Frontmatter hält verschachtelte Listen ohne externe YAML-Bibliothek lesbar. state.json ist ein abgeleiteter vollständiger strukturierter Snapshot, der bytegenau gegen die Markdown-Dateien geprüft wird. CURRENT wird als letzter Schritt atomar ersetzt. Leser lösen CURRENT genau einmal auf und lesen einen abgeschlossenen Stand. Alte Generationen bleiben erhalten. Ein Release ist genau eine veröffentlichte Generation; ein zweiter separater Releasevorgang ist nicht nötig.

Alternative verworfen: Einzeldateien direkt überschreiben, weil Prozessabbruch halbe Änderungen erzeugt. Alternative verworfen: CRM-Laufzeit komplett kopieren, weil CRM-Komplexität, Begriffe und Nebenfunktionen hier keinen Nutzen bringen. Der Mechanismus ist eine eigenständige Implementierung, keine Behauptung identischer CRM-Dateikompatibilität.

### Transaktion

Planformat `ai-task-plan/1`: base generation, vollständiger vorgeschlagener Zustand, actor, origin, operation und SHA-256. Apply erwartet exakt den gezeigten Planhash, prüft aktuelle Basis und komplette Integrität, validiert Beziehungen und schreibt unter exklusiver lokaler mkdir-Sperre. Neue Generation wird in einem Staging-Verzeichnis fertiggestellt und atomar umbenannt. Ein Prozessabbruch kann eine unveröffentlichte Generation hinterlassen; er korrumpiert nicht CURRENT. Sperren werden nicht automatisch gebrochen. Der Mechanismus ist für einen lokalen gemeinsam genutzten Dateisystempfad gedacht; keine verteilte OneDrive-/SharePoint-Sperre.

### Modell

`area`, `project`, `heading`, `task`, `tag`, `source`, `knowledge` mit typabhängigem Schema. Aufgaben bewahren die things-Feldnamen. Checklisten und Tagreferenzen liegen bei der Aufgabe. Quellen tragen title, reference und originalen Text; Wissensseiten enthalten Aussagen mit sourceId/locator, verlinkte recordIds und notes. Für Inhaltskonflikte gelten Erhalt und Offenlegung. Keine erfundenen Belege, Credentials oder Benutzeridentitäten.

### Ansichten

Ansichten sind reine Funktionen, ohne implizite Schreibzugriffe. Heute zeigt aktive geplante Aufgaben bis heute und überfällige Deadlines sowie heute erledigte/abgebrochene Aufgaben, solange nicht geloggt. Demnächst zeigt zukünftige Plantermine; Deadline ist zusätzlich separat sichtbar. Eingang: status=null. Jederzeit: aktive, nicht aufgeschobene Aufgaben ohne zukünftigen Plantermin. Irgendwann: isSomeday ohne Plantermin. Logbuch: isLogged, Papierkorb: trashedAt/status=trashed. Templates erscheinen getrennt. Diese Semantik wird als bewusste, dokumentierte Vereinfachung gegenüber dem things-Server getestet.

### Wiederholung

Unterstützte RRULE-Teilmenge: FREQ=DAILY/WEEKLY/MONTHLY, INTERVAL und bei WEEKLY BYDAY. Monatsintervalle bleiben am ursprünglichen Tag verankert; fehlende Monatstage werden übersprungen. Fällige Instanzen entstehen durch explizites tick, nie durch Query. Instanz-ID aus Template-ID und Datum; max. 366 Instanzen je Plan verhindert unbeschränkte Nachholung. Vollständiges RFC 5545, COUNT/UNTIL, stündliche Wiederholung werden verweigert statt falsch approximiert.

### Sicherheit und Portabilität

Nur Python-Standardbibliothek (3.9+). Keine Netzwerkanfragen, Login-Daten, Mail-/Kalendersynchronisierung oder ausführbare Automatismen. Pfade stammen ausschließlich aus validierten IDs; Symlinks im Raum werden verweigert. HTML escapt alle Nutztexte; Such-/Filterlogik ist statisch. Datum wird vom Agenten anhand der vereinbarten Zeitzone als YYYY-MM-DD übergeben; keine stillschweigende UTC-Lokaldatumumrechnung.

## 4. Umsetzung mit Dateien und Checks

1. **Analyse/Plan (dieser Stand)** — docs/PLAN.md, docs/SOURCES.md, research/sources.json; Quellpfade und Commit-IDs dokumentieren. Check: Ausgangsrepo leer, beide Referenzen gelesen. Budget ca. 220 Zeilen. Deckt SC01–SC11.
2. **Verhaltensprüfungen vor Implementierung** — tests/test_runtime.py mit Fällen für Initialisierung, Lifecycle, veraltete/geänderte Pläne, Concurrency, Datumsansichten, Wiederholung, Referenzen, Importroundtrip, Manipulation und Undo. Erster Lauf soll an fehlender Laufzeit scheitern. Budget ca. 300 Zeilen. Deckt SC02–SC10.
3. **Laufzeit** — ai-task/scripts/task.py mit Bibliotheksfunktionen und internem JSON-CLI: init-plan, plan, apply, query, export, verify. Input-Aktionen: upsert, complete, cancel, log, trash, restore, tick, undo. Schema und Validation in derselben fokussierten Datei; falls deutlich über 1000 Zeilen, nach Verantwortung teilen. Budget ca. 800 Zeilen. Check: Regressionstests. Deckt SC02–SC10.
4. **Skill und Verträge** — ai-task/SKILL.md, ai-task/references/{contract,workflows,coverage}.md. Agent zeigt Ziel, Identität und Änderungen; nutzt vorhandene Autorisierung ohne überflüssige neue Bestätigung. Check: Skill-Validator und realistische Beispielabläufe. Budget ca. 280 Zeilen. Deckt SC01–SC09.
5. **Produktansicht und Beispiel** — HTML-Renderer im Runtime-Modul, examples/demo/ und docs/index.html mit rein synthetischen Daten; nachvollziehbare Bereiche, Projekt, Termine, Wiederholung, Quelle und Wissensseite. Check: HTML-Parsing, Nutzdaten-Escaping, Browser-Screenshot wenn Browser verfügbar. Budget ca. 180 zusätzliche Runtime-Zeilen. Deckt SC05, SC09–SC10.
6. **Paket und Lieferung** — tools/check.py, tools/package.py, .github/workflows/check.yml, README.md, LICENSE, NOTICE, THIRD_PARTY_NOTICES.md, dist/ai-task.skill und Prüfsumme. Check: Python-Tests, Validator, reproduzierbarer Paketbau, Git-Diff und Remote-Readback. Budget ca. 200 Zeilen. Deckt SC01, SC11.

Die Schritte werden in dieser Reihenfolge von einem Agenten umgesetzt. Es werden keine anderen Repositories geändert, keine globalen Skills installiert und keine bestehenden Aufgaben importiert. Kein Deployment oder GitHub-Pages-Umschalten. Der fertige Stand wird in AI_Task committet und auf dessen main gepusht; Referenzrepository-Branches bleiben unangetastet.

## 5. Abnahme, Risiken und Grenzen

Abnahmebefehle: `python3 tools/check.py`, `python3 tools/package.py`, Skill quick_validate, Paket-Prüfsumme, Remote-Commit-Abgleich. Testdaten und temporäre Artefakte bleiben innerhalb AI_Task.

Wichtige Risiken: Generationsgeschichte wächst; kein automatisches Pruning. Keine verteilte Konfliktauflösung. JSON-Import verlangt das dokumentierte Bundleformat, keine automatische SQLite-/API-Migration. Die Fachstruktur stammt aus things; die vollständige Web-App, Auth, Drag-and-drop, SSE, CLI-Login, per-Ansicht-Sortierung und vollständige RRULE-Parität gehören nicht zur Lieferung. Die Wissensraumarchitektur folgt AI_first_CRM, dessen umfassende OKF-, GDPR-, XLSX-, Mail- und Kampagnenfunktionen sind hier nicht zugesagt.

Stopbedingungen: unerwartete bestehende Änderungen in AI_Task; fehlende Leseberechtigung für Quellen; beschädigter Generationenstand; unzulässige Fremdschlüssel oder RRULE; fehlgeschlagene Prüfungen vor Push. Keine Reparatur durch stilles Datenlöschen oder Sperrbruch.

## 6. Änderungs- und Ergebnisprotokoll

Wird nach den Prüfungen um tatsächlich gelieferte Funktionen, Abweichungen und Nachweise ergänzt.

### Gelieferter Stand

Alle sechs Umsetzungsschritte wurden ausgeführt. Die unabhängige Runtime umfasst 703 Zeilen und bleibt damit im vorgesehenen Modulbudget. 18 Tests bestehen; zusätzliche Prüfungen decken simultane Anwendung, einen Pointer-Schreibfehler und unabhängigen Frozen-Skill-Export ab. Die statische Demo wird aus dem verifizierten synthetischen Raum generiert. Paket, SHA-256 und CI-Konfiguration liegen vor.

Bewusste Präzisierung: Projekt-/Bereichsgruppen enthalten geloggte Aufgaben für korrekte Abschlusszahlen. Der Frozen-Skill-Export ergänzt den im Ziel beschriebenen portablen Wissensraum. Keine zusätzliche Laufzeitabhängigkeit. Browser-URL-Policy blockierte die visuelle Prüfung lokaler Dateien; keine Umgehung, verbleibende Grenze dokumentiert in VALIDATION.md. Keine fachliche Parität mit allen Serverfunktionen von things behauptet.
