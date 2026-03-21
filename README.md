# 🚀 CRM-Vertriebssystem (Full Project Release)

## 📋 Projektübersicht
Dieses CRM-System wurde über drei Sprints hinweg entwickelt, um den Vertriebsprozess von der ersten Lead-Erfassung bis zur aktiven Kundenverwaltung zu digitalisieren. Es bietet eine sichere, rollenbasierte Umgebung mit Datenvisualisierung und API-Unterstützung.

---

## 🏗️ Projektentwicklung (Sprint-Historie)

### 🔹 Sprint 1: Fundament & Basis-Funktionen
- **Setup**: Flask-App mit SQLite-Datenbank-Anbindung.
- **Basis-CRUD**: Erstellen, Lesen, Aktualisieren und Löschen von Kunden (Customers).
- **Navigation**: Implementierung eines konsistenten Layouts mittels Jinja2-Templates (`base.html`).

### 🔹 Sprint 2: Lead-Management & Business Logic
- **Leads-Verwaltung**: Einführung einer separaten Tabelle für Verkaufsinteressenten.
- **Benutzer-Authentifizierung**: Erstes Login-System für den Zugriffsschutz.
- **Frontend-Styling**: Integration von Bootstrap 5 für ein responsives Design.

### 🔹 Sprint 3: Analyse, Suche & Berechtigung (Aktuell)
- **CIY-21 (Dashboard)**: Grafische Auswertung der Kundenstatus-Verteilung (Chart.js).
- **CIY-22 (Suche/Filter)**: Dynamische Echtzeit-Suche für die Kundenliste.
- **CIY-23 (Lead-Konvertierung)**: Komplexer Workflow zur Umwandlung von Leads in Kunden.
- **CIY-24 (RBAC)**: Rollenbasierte Zugriffskontrolle (Admin vs. User).
- **CIY-25 (API-Dokumentation)**: Automatisierte Swagger-UI Integration.

---

## 🔐 Benutzerrollen & Test-Accounts
| Rolle | Benutzername | Passwort | Beschreibung |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Darf alles: CRUD, Löschen, Konvertieren. |
| **User** | `user1` | `user123` | Eingeschränkt: Nur Lesezugriff und Filterung. |

---

## 🛠️ Technische Installation
1. **Requirements**: `pip install -r requirements.txt`
2. **Datenbank**: Wird beim ersten Start automatisch initialisiert.
3. **Start**: `python app.py`
4. **API-Docs**: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## 📊 UML-Dokumentation
Sämtliche Diagramme befinden sich im Ordner `/docs`:
- **Use Case Diagramm**: `docs/usecase.png` (Zeigt Rollen und Kernprozesse).
- **Jira-Dokumentation**: Der Projektfortschritt wurde vollständig in Jira dokumentiert (Status: Alle Tickets erledigt).

---
*Status: Finaler Release (M4) - März 2026*