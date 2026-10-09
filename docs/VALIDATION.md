# Abnahme am 9. Oktober 2026

## Verifiziert

- AI_Task war vor Beginn leer. Änderungen und lokale Arbeitsdateien liegen ausschließlich in AI_Task. Beide Referenzrepositories wurden nur gelesen.
- Ausführlicher Plan als erster Commit: 63ff69f. Verhaltensprüfungen als zweiter Commit: d2ffef2. Ihr erster Lauf schlug erwartungsgemäß wegen fehlender Laufzeit fehl.
- `python3 tools/check.py`: 18 Regressionstests erfolgreich auf Python 3.9, anschließend Beispielintegrität, Skillreferenzen und zweifacher reproduzierbarer Paketbau erfolgreich.
- Skill-Creator `quick_validate.py ai-task`: Skill is valid.
- Schutzfälle geprüft: veralteter/veränderter Plan ohne Pointerwechsel, konkurrierende Anwendung mit genau einem Gewinner, blockierte lokale Sperre, künstlicher Fehler vor Pointerwechsel mit lesbarem Vorzustand, beschädigtes Markdown, Symlink und ID-Pfadtraversal.
- Fachfälle geprüft: Hierarchie/Fremdschlüssel, Checklisten, Datum/Deadline/Abend, Lifecycle/Undo, JSON-Roundtrip, unbekannte Felder, Monatsanker 31 ohne Februar-Verschiebung, Wochen-BYDAY, keine doppelten Wiederholungsinstanzen, begrenzte Nachholung, belegte Wissensseiten und Suche.
- Frozen Skill bleibt nach Entfernung des Test-Ausgangsraums eigenständig abfragbar; Snapshot-Hash und Recordinhalt sind erhalten.
- HTML-Nutzdaten sind escaped. Strukturprüfung bestätigt eindeutige IDs, vorhandene Navigationsziele und keine externen Bild-/Stylesheet-/Frame-Ressourcen. Die Offline-Demo entspricht bytegenau dem Renderer des verifizierten Beispiels.
- `git diff --check`: keine Fehler. Paketprüfung: gültiges ZIP, relative enthaltene Pfade, SKILL.md vorhanden und keine temporären Dateien.

## Keine darüber hinausgehenden Zusagen

Das Öffnen der lokalen file:-HTML-URL wurde vom Computer-Use-Browser aufgrund seiner Protokollrichtlinie abgelehnt. Keine visuelle Browser-/Mobilprüfung und keine Prüfung realer Skillnutzung in einer fremden Agentensitzung. Die HTML-Suche wurde strukturell geprüft; ihre interaktive Browserausführung ist nicht als getestet ausgewiesen. Eine bestandene Strukturprüfung ersetzt keine visuelle Abnahme.

GitHub Actions wird durch den Push ausgelöst; ihr Remote-Ergebnis ist gesondert zu prüfen. Kein GitHub-Pages-Deployment, keine globale Skillinstallation, keine echten Benutzerdaten, keine Live-Anbindung an things, keine verteilte Sync-Prüfung. Die Funktionalität ist auf den dokumentierten Lieferumfang begrenzt.

Die ausführlichen Grenzen stehen in ../ai-task/references/coverage.md. Das Paket enthält seine eigene Lizenz und NOTICE; Referenzquellcode wird nicht mitgeliefert.

## Landingpage-Ergänzung

Landingpage unter docs/index.html, synthetische Offline-Demo separat unter docs/demo.html. Impressumslink entspricht dem Link der geprüften Referenzseite; Ziel am 9. Oktober 2026 per HTTP mit Status 200 geprüft. Download und SHA-256 liegen auch im Pages-Verzeichnis und werden beim Paketbau synchronisiert. Keine Inspirationshinweise in der Landingpage. Kein Tracking und keine externen Fonts.

## OKR-Abnahme — 9. Oktober 2026

30 Regressionstests bestehen. Neue Fälle prüfen die Rechenregeln für Steigern/Senken/Binär, unbekannte Werte und unvollständige Mittelwerte, Übererfüllung/Regression, kritische KRs, Zuversicht und Aktualität, historische Stichtage, Korrekturketten, unveränderliche Messwerte auch an der Apply-Grenze, gesperrte Messdefinitionen, Quellenprüfung, Aufgabenabschluss ohne KR-Fortschrittsänderung, Check-in/Abschlussreview, /1→/2-Migration ohne Änderungen alter Generationen, Undo über die Versionsgrenze, alte Bundles, OKR-Roundtrip und Frozen-Skill.

Alle alten und neuen Demo-Generationen werden unverändert verifiziert. Die aktualisierte Demo entspricht dem Renderer des aktiven Standes. HTML-IDs sind eindeutig; sämtliche Fragmentverknüpfungen zeigen auf bestehende Ziele. Das entpackte .skill-Paket führt die OKR-Abfrage eigenständig aus und berechnet im Beispiel exakt 7/15 = 46,666… %. Paketbau ist reproduzierbar; Skill-Validator erfolgreich. Eine visuelle Browserprüfung ist weiterhin nicht als durchgeführt ausgewiesen.

Lieferumfang: Objectives, Key Results, belegte Messpunkte/Korrekturen, Verknüpfungen, Reports/HTML, Reviews, Migration, Skill-Vertrag, Beispielzyklus und aktualisierte Landingpage/Downloads. Keine Live-Datenanbindung oder Prognose zugesagt. Die Entscheidung über Zielerreichung bleibt ein ausdrücklicher Review.

## Durchgängiger Demo-Rundgang

Demo ergänzt um zweiten Messzeitpunkt für alle drei Einstiegs-KRs, unterstützende Aufgabencheckliste, ambitioniertes Lernziel mit fehlender Zufriedenheitsmessung und 50% ausdrücklich unvollständigem Teilmittel sowie einen abgeschlossenen September-Pilot mit binärem Ergebnis und Abschlussreview. Sämtliche neuen Messwerte sind im synthetischen Quelltext belegt. Landingpage führt direkt zu diesen drei Situationen. Demo ist sichtbar als synthetisch gekennzeichnet und enthält einen Rückweg zur Landingpage. Die öffentliche Demo-Hülle wird separat erzeugt; kanonische alte HTML-Generationen bleiben unverändert. Ankerprüfung und 30 Regressionstests erfolgreich.
