# CRM-Vertriebssystem - Projektberichterstattung (M4)

## Projektbeschreibung
Dieses CRM-System dient der digitalen Verwaltung von Kunden und Verkaufsinteressenten (Leads). Die Entwicklung erfolgte in vier Phasen (Sprint 0 bis Sprint 3) und deckt den gesamten Prozess von der Anforderungsanalyse bis hin zum Deployment und der API-Dokumentation ab.

## Projektverlauf und Meilensteine

| Sprint | Zeitraum | Fokus | Deliverables |
| :--- | :--- | :--- | :--- |
| **Sprint 0** | Woche 1 | Setup & Planning | Jira-Projekt eingerichtet, Erweiterung gewählt, GitHub Repo geklont |
| **Sprint 1** | Woche 2 | Requirements & Design | Use-Case-Diagramm, Aktivitätsdiagramm, ERD, Sequenzdiagramm |
| **Sprint 2** | Woche 3 | Implementierung Kern | Basisfunktionen lauffähig, Erweiterung begonnen, Authentifizierung |
| **Sprint 3** | Woche 4 | Erweiterung & Finalisierung | Erweiterung fertig (RBAC, Dashboard), Testing, Dokumentation, Deployment |

## Funktionsumfang
- **Kundenverwaltung**: Vollständige CRUD-Operationen (Erstellen, Lesen, Aktualisieren, Löschen).
- **Lead-Management**: Erfassung von Interessenten und automatisierte Konvertierung in Kunden.
- **Dashboard**: Grafische Darstellung der Kundenstatus-Verteilung.
- **Sicherheit (RBAC)**: Rollenbasierte Zugriffskontrolle zwischen Administratoren und Standard-Nutzern.
- **API-Dokumentation**: Automatisierte Schnittstellenbeschreibung via Swagger/Flasgger.

## Benutzerrollen für den Testbetrieb
| Rolle | Benutzername | Passwort | Berechtigungen |
| :--- | :--- | :--- | :--- |
| **Administrator** | admin | password123 | Voller Zugriff auf alle administrativen Funktionen |
| **Standard-User** | user1 | user123 | Eingeschränkter Lesezugriff, Suche und Filterung |

## Installation und Betrieb
1. Installation der Abhängigkeiten: `pip install -r requirements.txt`
2. Starten der Anwendung: `python app.py`
3. Zugriff auf die API-Dokumentation: `http://127.0.0.1:5000/apidocs`

## Dokumentation
Alle technischen Diagramme (Use-Case, ERD etc.) sind als `.puml` und `.png` Dateien im Ordner `docs/` hinterlegt. Der aktuelle Status der Tasks ist im Jira-Board dokumentiert.

---

##  Benutzerrollen & Test-Accounts
| Rolle | Benutzername | Passwort | Beschreibung |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Darf alles: CRUD, Löschen, Konvertieren. |
| **User** | `user1` | `user123` | Eingeschränkt: Nur Lesezugriff und Filterung. |

---

##  Technische Installation
1. **Requirements**: `pip install -r requirements.txt`
2. **Datenbank**: Wird beim ersten Start automatisch initialisiert.
3. **Start**: `python app.py`
4. **API-Docs**: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

##  UML-Dokumentation
Sämtliche Diagramme befinden sich im Ordner `/docs`:
- **Use Case Diagramm**: `docs/use_case.png` (Zeigt Rollen und Kernprozesse).
- **Jira-Dokumentation**: Der Projektfortschritt wurde vollständig in Jira dokumentiert (Status: Alle Tickets erledigt).

---
*Status: Finaler Release (M4) - März 2026*