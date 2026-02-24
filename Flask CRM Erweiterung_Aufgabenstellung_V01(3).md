# Flask CRM-Projekt – Aufgabenstellung Sommersemester 2025/26

## Projektübersicht

Aufbauend auf dem bestehenden **Flask CRM-System** (Customer Relationship Management) aus dem Wintersemester soll im Sommersemester eine **individuelle Erweiterung** geplant, dokumentiert und umgesetzt werden. Das Projekt kombiniert Softwareentwicklung mit professionellem Requirements Engineering, UML-Modellierung und agilem Projektmanagement nach SCRUM[^1].

> **Achtung:** Ein Remote - Repository mit entsprechendem Zugriff muss selbst erstellt werden. Es muss nicht Github verwendet werden. (Z.b. Codeberg)

---

## 1. Bestehendes CRM-System (Ausgangsbasis)

Das bestehende CRM-System umfasst folgende Kernfunktionalität[^1]:

- **Customer Management** – CRUD-Operationen für Kundendaten (Name, E-Mail, Firma, Telefon, Status)
- **Lead Tracking** – Verwaltung von Sales-Leads mit Wert, Quelle und Status
- **Contact History** – Dokumentation von Kundenkontakten (Telefon, E-Mail, Meeting, Notiz)
- **Dashboard** – Übersichtsseite mit Statistiken
- **MVC-Architektur** – Trennung in Model (`models.py`), View (`templates/`) und Controller (`app.py`)
- **In-Memory-Speicherung** – aktuell ohne persistente Datenbank

---

## 2. Individuelle Erweiterung (Auswahl)

Jeder Studierende wählt **eine** der folgenden Erweiterungen als Hauptfeature. Die Wahl muss bis zum Ende von Sprint 1 mit der Lehrperson abgestimmt sein.

### Erweiterungsoptionen

| Nr. | Erweiterung                        | Beschreibung                                                                                                            | Schwierigkeit  |
| --- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------- |
| 1   | **Datenbankintegration (SQLite)**  | Migration von In-Memory auf SQLite mit Flask-SQLAlchemy; persistente Speicherung aller Entitäten                        | ⭐⭐             |
| 2   | **User Authentication**            | Login/Logout mit Flask-Login; Registrierung, Passwort-Hashing, Session-Management, rollenbasierter Zugriff (Admin/User) | ⭐⭐⭐            |
| 3   | **REST-API**                       | JSON-basierte API-Endpunkte für alle CRUD-Operationen; API-Dokumentation (z. B. Swagger/OpenAPI)                        | ⭐⭐⭐            |
| 4   | **Such- und Filterfunktion**       | Volltextsuche über Kunden, Leads und Kontakte; Filter nach Status, Firma, Datum; sortierbare Tabellen                   | ⭐⭐             |
| 5   | **CSV/Excel Export & Import**      | Datenexport als CSV/Excel; Import-Funktion mit Validierung; Berichterstellung                                           | ⭐⭐             |
| 6   | **Dashboard-Visualisierung**       | Interaktive Charts (z. B. mit Chart.js oder Plotly); Umsatz-Pipeline, Lead-Quellen, Kundenstatistiken                   | ⭐⭐⭐            |
| 7   | **Pipeline-Management**            | Kanban-Board für Deal-Stages (New → Contacted → Qualified → Won/Lost); Drag-and-Drop-Funktionalität                     | ⭐⭐⭐            |
| 8   | **E-Mail-Benachrichtigungen**      | Automatische E-Mail-Benachrichtigungen bei neuen Leads, Statusänderungen; Integration mit Flask-Mail                    | ⭐⭐⭐            |
| 9   | **Aufgaben- und Terminverwaltung** | To-Do-Liste pro Kunde; Erinnerungen; Kalenderansicht für geplante Kontakte                                              | ⭐⭐             |
| 10  | **Eigener Vorschlag**              | Eigenständig formulierter Vorschlag mit Genehmigung der Lehrperson                                                      | nach Absprache |

Die Erweiterungen 1–3 gelten als **Basisvorschläge**. Die Basisvorschläge sollten auf jeden Fall implementiert werden.  Erweiterungen können bei entsprechendem Aufwand auch kombiniert werden (z. B. Datenbank + Authentication)[^27].

---

## 3. Requirements Engineering & UML-Dokumentation

Die gesamte Funktionalität (Basisfunktionen **+** gewählte Erweiterung) ist im Rahmen der Requirements-Engineering-Phase mit folgenden UML-Diagrammen zu dokumentieren.

### 3.1 Use-Case-Diagramm

Das Use-Case-Diagramm beschreibt die funktionalen Anforderungen aus Sicht der Akteure[^14][^26].

**Mindestanforderungen:**

- Identifikation aller Akteure (z. B. Admin, Sales-Mitarbeiter, Gast)
- Darstellung aller Use Cases des Basissystems und der Erweiterung
- Beziehungen: `<<include>>`, `<<extend>>`, Generalisierung wo sinnvoll
- Systemgrenzen klar eingezeichnet

**Beispielakteure:**

- **Sales User** – Kunden und Leads verwalten, Kontakte dokumentieren
- **Admin** – Benutzerverwaltung, Systemkonfiguration (falls Erweiterung 2)
- **Externer Dienst** – API-Konsument (falls Erweiterung 3)

### 3.2 Aktivitätsdiagramm

Das Aktivitätsdiagramm modelliert die Abläufe (Workflows) innerhalb des Systems[^20].

**Mindestanforderungen:**

- Mindestens **2 Aktivitätsdiagramme** für zentrale Prozesse:
  - Prozess 1: Ein Kernprozess des Basissystems (z. B. „Neuen Kunden anlegen")
  - Prozess 2: Der Hauptprozess der gewählten Erweiterung (z. B. „Login-Workflow")
- Entscheidungsknoten (Decisions/Guards), Parallelisierung (Fork/Join) wo sinnvoll
- Swimlanes für Akteure/Systemkomponenten empfohlen

### 3.3 Sequenzdiagramm (NEU)

Das UML-Sequenzdiagramm zeigt die zeitliche Abfolge von Nachrichten zwischen Objekten/Komponenten für einen konkreten Anwendungsfall[^15][^24].

**Mindestanforderungen:**

- Mindestens **2 Sequenzdiagramme**:
  - Sequenz 1: Eine typische CRUD-Operation (z. B. „Kunde anlegen" – Ablauf von HTTP Request → Controller → Model → Template → Response)
  - Sequenz 2: Ein Ablauf aus der gewählten Erweiterung (z. B. „User-Login" oder „API-Aufruf")
- Lifelines für: Browser/User, Controller (Flask Route), Model, Datenbank (falls vorhanden), ggf. externe Services
- Darstellung von: synchronen/asynchronen Nachrichten, Rückgabewerten, Aktivierungsbalken
- Verwendung von Combined Fragments (alt, loop, opt) wo sinnvoll

**Empfohlenes Tool:** PlantUML (Integration in VS Code möglich)[^29][^21]

```plantuml
@startuml
actor "Sales User" as User
participant "Browser" as B
participant "Flask Controller\n(app.py)" as C
participant "Customer Model\n(models.py)" as M
participant "Template\n(Jinja2)" as T

User -> B: Formular ausfüllen\nund absenden
B -> C: POST /customers/add
activate C
C -> C: request.form validieren
alt Validierung erfolgreich
    C -> M: add_customer(name, email, ...)
    activate M
    M --> C: Customer-Objekt
    deactivate M
    C -> C: flash("Erfolg", "success")
    C --> B: redirect(/customers)
    B -> C: GET /customers
    C -> M: get_all_customers()
    M --> C: [Customer-Liste]
    C -> T: render_template("customers.html", ...)
    T --> C: HTML
    C --> B: HTTP 200 + HTML
else Validierung fehlgeschlagen
    C -> C: flash("Fehler", "error")
    C --> B: redirect(/customers/add)
end
deactivate C
B --> User: Seite anzeigen
@enduml
```

### 3.4 Entity-Relationship-Diagramm (ERD)

Das ER-Diagramm dokumentiert die Datenbankstruktur des Systems.

**Mindestanforderungen:**

- Alle Entitäten mit Attributen und Datentypen
- Primärschlüssel und Fremdschlüssel markiert
- Kardinalitäten (1:1, 1:N, N:M) an allen Beziehungen
- Entitäten der Erweiterung integriert
- Notation: Chen-Notation oder Crow's Foot

**Basis-Entitäten:**

- `Customer` (id, name, email, company, phone, status)
- `Lead` (id, name, email, company, value, source, status)
- `Contact` (id, customer_id [FK], contact_type, notes, date)
- *Erweiterungsspezifische Entitäten* (z. B. `User`, `Task`, `Pipeline_Stage`, …)

---

## 4. Projektmanagement mit SCRUM (Jira)

Das Projekt wird als **SCRUM-Projekt** in Jira (oder einer vergleichbaren Software wie GitHub Projects, Trello, oder YouTrack) verwaltet[^16][^13].

### 4.1 Jira-Projektsetup

1. **SCRUM-Projekt anlegen** – Template „Scrum" in Jira verwenden[^31]
2. **Epics definieren** – Mindestens folgende Epics:
   - `Requirements & Design` – Alle UML-Diagramme und Dokumentation
   - `CRM Basisfunktionen` – Bestehende Funktionalität übernehmen/anpassen
   - `[Erweiterung X]` – Die gewählte individuelle Erweiterung
   - `Testing & Qualitätssicherung` – Tests und Bugfixes
   - `Deployment & Dokumentation` – Finalisierung
3. **User Stories formulieren** – Jede Funktionalität als User Story mit Akzeptanzkriterien[^37]

### 4.2 User-Story-Format

```
Als [Rolle]
möchte ich [Funktionalität],
damit [Nutzen/Ziel].

Akzeptanzkriterien:
- [ ] Kriterium 1
- [ ] Kriterium 2
- [ ] Kriterium 3
```

**Beispiel:**

```
Als Sales-Mitarbeiter
möchte ich einen neuen Kunden über ein Webformular anlegen können,
damit ich Kundendaten zentral im CRM-System verwalten kann.

Akzeptanzkriterien:
- [ ] Formular enthält Felder: Name, E-Mail, Firma, Telefon, Status
- [ ] Validierung: Alle Pflichtfelder müssen ausgefüllt sein
- [ ] Nach erfolgreichem Anlegen: Weiterleitung zur Kundenliste mit Erfolgsmeldung
- [ ] Ungültige E-Mail-Adressen werden abgewiesen
```

### 4.3 Sprint-Planung

Das Projekt wird in **4 Sprints** aufgeteilt (jeweils ca. 2-3 Wochen):

| Sprint   | Zeitraum (Beispiel) | Fokus                       | Deliverables                                                        |
| -------- | ------------------- | --------------------------- | ------------------------------------------------------------------- |
| Sprint 0 | Woche 1             | Setup & Planning            | Jira-Projekt eingerichtet, Erweiterung gewählt, GitHub Repo geklont |
| Sprint 1 | Woche 2             | Requirements & Design       | Use-Case-Diagramm, Aktivitätsdiagramm, ERD, Sequenzdiagramm         |
| Sprint 2 | Woche 3             | Implementierung Kern        | Basisfunktionen lauffähig, Erweiterung begonnen                     |
| Sprint 3 | Woche 4             | Erweiterung & Finalisierung | Erweiterung fertig, Testing, Dokumentation, Deployment              |

### 4.4 SCRUM-Zeremonien (dokumentiert)

Folgende Zeremonien sind zu dokumentieren (Screenshots/Protokolle in Jira oder separatem Dokument)[^40]:

- **Sprint Planning** – Welche Stories kommen in den Sprint? Story Points vergeben
- **Sprint Review** – Was wurde erreicht? Demo-Screenshots oder kurze Beschreibung
- **Sprint Retrospective** – Was lief gut? Was kann verbessert werden?
- **Daily Standup** – Mindestens 2 dokumentierte Einträge pro Sprint (Was habe ich gemacht? Was plane ich? Gibt es Blocker?)

### 4.5 Jira-Board-Konfiguration

Das Board soll mindestens folgende Spalten enthalten:

- **Backlog** → **To Do** → **In Progress** → **In Review** → **Done**

Story Points sind für jede User Story zu vergeben (Fibonacci-Skala empfohlen: 1, 2, 3, 5, 8, 13)[^28].

---

## 5. Technische Anforderungen

### 5.1 GitHub Classroom oder eigenes Version Control System

- Neuer GitHub Classroom Link wird bereitgestellt (Achtung: **7 Tage Gültigkeit** für Einladung!)
- **Regelmäßige Commits** – Mindestens 2 Commits pro Woche; aussagekräftige Commit-Messages
- **Branching-Strategie empfohlen** – `main` (stabil), `develop` (Entwicklung), Feature-Branches

### 5.2 Code-Qualität

- Einhaltung des **MVC-Patterns** (Model/View/Controller getrennt)[^1]
- **Docstrings** für alle Funktionen und Klassen
- **Validierung** aller Benutzereingaben serverseitig
- **Flash Messages** für Benutzer-Feedback
- **Custom Error Pages** (404, 500)
- **Responsive Design** (Mobile-Optimierung)

### 5.3 Projektstruktur (erweitert)

```
crm_system/
├── app.py                  # Controller (Flask Routes)
├── models.py               # Model (Datenklassen/ORM)
├── config.py               # Konfiguration (Optional)
├── requirements.txt        # Python-Abhängigkeiten
├── README.md               # Projektdokumentation
├── docs/                   # UML-Diagramme & Dokumentation
│   ├── use_case.puml       # Use-Case-Diagramm (PlantUML)
│   ├── activity.puml       # Aktivitätsdiagramm
│   ├── sequence.puml       # Sequenzdiagramm
│   ├── erd.puml            # ER-Diagramm
│   └── images/             # Exportierte Diagramme (PNG/SVG)
├── static/
│   ├── css/style.css
│   └── js/script.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── customers.html
│   ├── ... (weitere Templates)
│   └── 404.html
└── tests/                  # (Optional) Unit-Tests
    └── test_models.py
```

---

## 6. Bewertungskriterien

| Kategorie                    | Gewichtung | Details                                                                                                         |
| ---------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| **UML-Diagramme**            | 30%        | Use-Case (8%), Aktivitätsdiagramm (7%), Sequenzdiagramm (8%), ERD (7%) – Korrektheit, Vollständigkeit, Notation |
| **Implementierung**          | 35%        | Funktionalität (15%), Code-Qualität (10%), MVC-Einhaltung (5%), Erweiterung (5%)                                |
| **Projektmanagement (Jira)** | 20%        | Board-Setup (5%), User Stories (5%), Sprint-Dokumentation (5%), Retrospektiven (5%)                             |
| **GitHub & Dokumentation**   | 15%        | Regelmäßige Commits (5%), README (5%), saubere Projektstruktur (5%)                                             |

### Notenschlüssel (Alle Abgaben/ Sprints bzw. Meilensteine sind kurz zu präsentieren [Sprint - Review])

- **Sehr Gut:** Alle Diagramme korrekt und vollständig; Erweiterung voll funktionsfähig; Jira professionell gepflegt; sauberer Code
- **Gut:** Kleinere Mängel in Diagrammen oder Code; Erweiterung größtenteils funktionsfähig
- **Befriedigend:** Basisfunktionalität vorhanden; Diagramme mit Fehlern; Jira grundlegend genutzt
- **Genügend:** Minimale Funktionalität; unvollständige Dokumentation; wenige Commits
- **Nicht Genügend:** Abgabe fehlt oder wesentliche Teile nicht vorhanden

---

## 7. Abgabe & Meilensteine

| Meilenstein                      | Fälligkeit    | Abzugeben                                                                            |
| -------------------------------- | ------------- | ------------------------------------------------------------------------------------ |
| **M1: Setup & Erweiterungswahl** | Ende Sprint 0 | Jira-Projekt angelegt; Erweiterung gewählt und mitgeteilt; GitHub Repo akzeptiert    |
| **M2: Requirements Engineering** | Ende Sprint 1 | Alle 4 UML-Diagramme (Use-Case, Aktivität, Sequenz, ERD) im `docs/`-Ordner           |
| **M3: Implementierung**          | Ende Sprint 2 | Lauffähiges Basissystem; Erweiterung begonnen; Jira aktuell                          |
| **M4: Finale Abgabe**            | Ende Sprint 3 | Vollständiges Projekt; Erweiterung umgesetzt; Jira abgeschlossen; README vollständig |

### Abgabeformat

- Code: Im GitHub Classroom Repository (letzter Commit vor Deadline zählt)
- UML-Diagramme: Als `.puml` (Quellcode) **und** exportierte `.png`-Dateien im `docs/`-Ordner
- Jira: Link zum Jira-Board mit Lesezugriff für die Lehrperson (oder Screenshots)
- Präsentation: Kurze Live-Demo (ca. 5–10 Minuten) im Rahmen der Sprint Reviews

---

## 8. Empfohlene Tools & Ressourcen

| Bereich           | Tool                                          | Hinweis                                           |
| ----------------- | --------------------------------------------- | ------------------------------------------------- |
| UML-Diagramme     | **PlantUML** (VS Code Extension)              | Textbasiert, versionierbar in Git[^29]            |
| UML-Diagramme     | **draw.io / diagrams.net**                    | Browserbasiert, kostenlos                         |
| UML-Diagramme     | **StarUML** oder **Lucidchart**               | Alternative grafische Tools                       |
| Projektmanagement | **Jira** (Free Tier)                          | SCRUM-Template verwenden[^34]                     |
| Projektmanagement | **GitHub Projects**                           | Alternative direkt in GitHub integriert           |
| IDE               | **VS Code**                                   | Mit Python, Flask, PlantUML Extensions            |
| Datenbank         | **DB Browser for SQLite**                     | Zur Visualisierung/Debugging der DB               |
| API-Testing       | **Postman** oder **Thunder Client** (VS Code) | Für Erweiterung 3 (REST-API)                      |
| Versionierung     | **Git / GitHub**                              | Regelmäßige Commits mit aussagekräftigen Messages |

---

## 9. Hinweise & Tipps

- **Frühzeitig beginnen:** Die Requirements-Phase ist nicht optional – sie bildet die Grundlage für die Implementierung.
- **Iterativ arbeiten:** Die Diagramme dürfen (und sollen) sich im Laufe des Projekts weiterentwickeln. Erste Versionen müssen nicht perfekt sein.
- **Jira aktiv nutzen:** Das Board ist kein Dokumentationspflichterfüller, sondern soll euch bei der Organisation helfen. Tägliche Updates sind ideal.
- **Git-Workflow einhalten:** Nicht alles in einem großen Commit am Schluss abgeben. Die Commit-History zeigt den Arbeitsprozess.
- **Fragen stellen:** Unklarheiten bei der Erweiterungswahl oder der UML-Notation frühzeitig mit der Lehrperson klären.
- **PlantUML lernen:** Textbasierte Diagramme lassen sich hervorragend in Git versionieren und sind leichter zu pflegen als grafische Dateien[^21].

---

## References

1. [001_hands_on_CRM_Guide.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/18583364/588e18a2-7d21-4fc8-8e59-44d51dcc1346/001_hands_on_CRM_Guide.md?AWSAccessKeyId=ASIA2F3EMEYE4USWBBKR&Signature=7vux0ZSuRC6JCL61Cy7VXKay3XE%3D&x-amz-security-token=IQoJb3JpZ2luX2VjELX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIQC8r96ydnG42x31d4swlBFg49I8tLu92M7WXr7M%2B8Bh%2FgIfFWDO2aa9IHqkjLt9S3tfn98Rzz4NGpnLfhYAeOQv4irzBAh%2BEAEaDDY5OTc1MzMwOTcwNSIMRcZ3FWt77PqVrJusKtAEy8EBgV%2BspAfe%2FLWyRR7ZkjVBufmZ0IdFwxfU24rtsdDMD13plTEtbz%2FRGYfPdrnvBinliod2Ps8iPAEJyq36DNGoxJ3MXVb916Td%2FVQL7IRn2EjbUAf09urqxI12LhV8DBFoPmgViEY139%2BzeVSd8uDhxUCxu6IHoE5sS6sx5DU12RM%2FE7PsGBX8n%2FrTKLtDAsEPsb3V9kFi2HB4jA%2FaURtJMGd5Gaz1C%2B9emr2Vx%2Fu5bPu4jEnRv%2BXDjqHWSNjQx2I5Lnjcu3L5WGSEth4E0S3tpZ%2B9R4oVUGyFnaPhZkrZRfmQt78ty1fXuIg1BP905PRmdLh02jvgaLJRvQF1j0Kp3TL3Eej4Vd%2FmARqKgQTENR4SXKdtZmD1yq2vdcAgasYEHsBrKwUt8T0p8gfh3wEuzITJiy21Tvvhvt%2Bqly%2BqboQ5HNXOKi1NnyrJtMAgrNBSa5v%2B46jn8aEh6iChvxWFyTdaeyhS5B9Z7GKv9AWd6BTXYZ6htGmWyRaXpNi%2B%2Bid38%2B189aGG3jyp2N7p%2BgAoHGTd3jA9lycb7EJiyb3YlhAyOXdy5ZntIhNU%2FaGw%2BVX7iN%2FUJOkVm94N%2Fsa2LRkddzkNuzRWfvi0jhPGabGAfkVzgCN8DW%2BPq9fhKrZSOOTTQ2P%2BElSKDNbQIabeQXEOwVHdDWWwdMEFhChTc10pl3pdyHa8PICv7%2FARjY5HRMeSfvMd8EFybUigwzD1CSb8eUsz8hUFKfivPeUbgKXKn6nlui74c2Rscn7YaDC2qLV%2BPABR5k1zJnrMdM3oXjD96KPMBjqZAUMgQKDrRF7ZB2BBwKO4OCDrVJU%2FU1grmgb9Z%2BchYyLAXVB%2FNqvZOP2l8LL7KxA4FJwe7nEe7cEQgBUg1WBDBMYjeRMqU5RNJIcDGX2gdDt93EmJJqdN71qjpS8NtUKJC9Arlphl1UwZL6IXWJFNhC0xriJdYpzzsyU2ihvU8%2F9AgTYKF%2BinmwETZBP6c4DJnBiOMunhiIH3Mg%3D%3D&Expires=1770588102) - # Comprehensive Flask Framework Guide: Building a Customer Relationship Management (CRM) System

## ...

13. [How to Create a Jira SCRUM project (Short Course) - Coursera](https://www.coursera.org/projects/how-to-create-a-jira-scrum-project) - Learn How to Create a Jira SCRUM project in this 2-hour, Guided Project. Practice with real-world ta...

14. [[PDF] Requirements Modeling and Use Case Diagrams](https://community.wvu.edu/~hhammar/rts/adv%20rts/adv%20rts%20slides/07/advrts%20slides%203%20req%20use%20cases.pdf)

15. [UML sequence diagrams overview of graphical notation](https://www.uml-diagrams.org/sequence-diagrams.html) - UML sequence diagrams overview of UML graphical notation: Lifeline, Message, Execution Specification...

16. [Learn scrum with Jira Tutorial | Agile](https://www.atlassian.com/agile/tutorials/how-to-do-scrum-with-jira) - A step-by-step guide on how to drive a scrum project, prioritize and organize your backlog into spri...

17. [How do you choose between use case diagram and activity diagram for requirements engineering?](https://www.linkedin.com/advice/1/how-do-you-choose-between-use-case-diagram) - Learn the differences, advantages, and disadvantages of use case diagram and activity diagram for re...

18. [Creating PlantUML diagrams in VS Insiders from Python Flask Example Book app with Copilot AI](https://www.youtube.com/watch?v=MmpW906xtWg) - A RESTful API service built with Flask for managing a book collection. This application demonstrates...

19. [Sequence Diagrams - Unified Modeling Language (UML)](https://www.geeksforgeeks.org/system-design/unified-modeling-language-uml-sequence-diagrams/) - A sequence diagram is a key component of Unified Modeling Language (UML) used to visualize the inter...

20. [Use Case Diagram - Unified Modeling Language (UML)](https://www.geeksforgeeks.org/system-design/use-case-diagram/) - A Use Case Diagram is a visual way to show how users (actors) interact with a system and what functi...

21. [Add Authentication to Flask Apps with Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login) - Learn how to add secure authentication to your Flask app using Flask-Login. Implement user sessions,...

22. [Sprint backlog template | Jira](https://www.atlassian.com/software/jira/templates/sprint-backlog) - Streamline sprint planning and execution with a sprint backlog template, your tool for effective tas...

23. [UML Sequence Diagram¶](https://plantuml-documentation.readthedocs.io/en/latest/diagrams/sequence.html)

24. [Jira for Scrum: Sprint Planning & Backlog Management (Full Demo)](https://www.youtube.com/watch?v=CXCxnTiwUnA) - Complete End-to-End Demo of a Scrum Project
    00:00  Intro
    01:12  Overview of a Scrum Project (Theory)...

25. [Scrum template | Jira - Atlassian](https://www.atlassian.com/software/jira/templates/scrum) - Easily plan, track, and manage ֵwork across sprints.

26. [Scrum Template to Plan Backlogs, Sprints, and Retrospectives [2026]](https://asana.com/templates/scrum) - Plan sprints, refine backlogs, and run stand-ups with a Scrum template. Track user stories and monit...

27. [1. Jira Software Board...](https://www.easyagile.com/blog/your-guide-to-using-scrum-and-kanban-jira-boards) - What Jira boards are, how to create, configure, and navigate the boards, and how to approach reporti...
