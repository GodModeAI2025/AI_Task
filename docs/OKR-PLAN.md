# OKR-Erweiterung — Plan vor Umsetzung

9. Oktober 2026. Ziel: die vorgeschlagene Zielebene vollständig in AI_Task integrieren. Nur dieses Repository wird geändert.

## Lieferumfang und Abnahme

1. Objectives mit Zeitraum, Verantwortlichem, verbindlich/ambitioniert und Status.
2. Key Results mit Messrichtung (steigern/senken/binär), Ausgangswert, Ziel, Einheit, Messmethode, Kritikalität und Verknüpfungen zu Aufgaben/Projekten.
3. Datierte Messpunkte mit Wert, Quelle und Locator; kein automatischer Fortschritt aus Aufgabenabschluss. Historie und Vorschau bleiben erhalten.
4. Rechenregeln: (Ist−Ausgang)/(Ziel−Ausgang), Senken äquivalent, binär 0/1. Rohfortschritt erhalten, Anzeige auf 0–100 % begrenzen. Gleichgewichteter Durchschnitt nur bei vollständiger Messabdeckung; sonst unbekannt mit separat gekennzeichnetem Teilmittel. Kein automatischer Erfolg aus Durchschnitt; kritische Ergebnisse sichtbar. Zuversicht und Aktualität separat.
5. Review-Datensätze für wöchentliche Check-ins und Abschluss: Hindernisse, Erkenntnisse, nächste Aufgaben und bestätigtes Ergebnis. Neue Messungen nur aus belegten Daten.
6. Reine OKR-Abfrage und HTML-Übersicht mit Quellen, Fortschritt, Messwerten, Aktualität, Links, Reviews; synthetischer Beispielzyklus. Landingpage, Skill, JSON-Import/Export und Frozen-Skill berücksichtigen OKR.
7. Kompatibilität: altes Format /1 bleibt exakt verifizierbar, einschließlich alter HTML-Bytes. Neue Bearbeitung migriert im normalen hashgebundenen Plan zu /2. Alte Generationen unverändert. Undo in alte Inhalte wird als /2 neu veröffentlicht. Alte JSON-Bundles werden angenommen; neue Bundles sind /2.

## Architekturentscheidung

Die bisherige Runtime wird als eingefrorenes legacy_task.py erhalten, um alte Generationen bytegenau zu prüfen. Die aktive task.py erhält /2 und verwendet okr.py für Validierung, Berechnungen und HTML. Keine externe Bibliothek. Neue Typen objective, key-result, measurement, review. Messpunkte sind nach Erstellung unveränderlich; Korrekturen erzeugen einen neuen Punkt mit explizitem supersedes. Gleicher KR/Tag ohne explizite Korrektur ist mehrdeutig und wird verweigert. As-of-Abfragen berücksichtigen keine künftigen Messungen. Ausgangs-/Zieländerungen nach Messbeginn sind verweigert; neues KR mit begründeter Verknüpfung oder neuer Zyklus statt nachträglicher Umdeutung.

## Reihenfolge und Checks

- Bestandsprüfung und dieser Plan.
- Schema/Rechenmodul und /1→/2-Kompatibilität.
- Tests: Rechnen in beide Richtungen, unbekannt, Übererfüllung, Regression, binär, gleiches Ziel/Ausgang, As-of, Aktualität, Quellen, Korrektur, unveränderliche Messungen, Aufgabenabschluss unabhängig, Reviews, Migration/Undo/Import/Frozen.
- HTML, Beispiel, Skill und Landingpage ergänzen.
- Gesamtsuite, Paketvalidator, Integrität aller Beispielgenerationen, Paket reproduzieren. Commit/Push und Remote-CI/Pages prüfen.

Keine Live-Messintegration, keine automatischen Prognosen, keine allgemeine 70-Prozent-Erfolgsampel. Das erste Modul verwendet gleiche Gewichte. Ein vollständiger Score ist Orientierung; die abschließende Bewertung wird im Review explizit festgehalten. Bestehende Aufgaben müssen keinen OKR-Verweis erhalten.

## Ergebnis

Alle sieben Lieferpunkte umgesetzt. 30 Tests, Skill-Validator, Demo-Generationsprüfung, HTML-Ankerprüfung und eigenständige Ausführung aus entpacktem Paket erfolgreich. Fortschritt im synthetischen Beispiel: 7/15. Alter Renderer und alte Verträge sind in legacy_task.py eingefroren. Neue Berechnungen und Ansichten liegen in okr.py. Vollständige Nachweise und verbleibende visuelle Prüfgrenze in VALIDATION.md.
