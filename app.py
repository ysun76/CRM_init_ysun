from flask import Flask, render_template, request, redirect, url_for, flash, session 
# NEU (Sprint 2): Import der Datenbank-Instanz und der persistenten Modelle
from models import db, Customer, Lead 


app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# --- NEU (Sprint 2): Datenbank-Konfiguration für Persistenz ---
# Ersetzt die flüchtige In-Memory Speicherung durch eine SQLite-Datenbank
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisierung von SQLAlchemy
db.init_app(app)

# --- NEU (Sprint 2): Automatische Tabellenerstellung beim Anwendungsstart ---
with app.app_context():
    db.create_all()
    # Initialdaten werden nur erstellt, wenn die Datenbank leer ist
    if not Customer.query.first():
        Customer.add_customer('John Doe', 'john@example.com', 'Acme Corp', '555-0001', 'active')
        Customer.add_customer('Jane Smith', 'jane@example.com', 'Tech Solutions', '555-0002', 'prospect')
        Lead.add_lead('Alice Brown', 'alice@example.com', 'StartUp Inc', 50000, 'Website')


 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        

        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            session['username'] = 'Admin'
            session['role'] = 'admin'
            flash('Willkommen, Admin!', 'success')
            return redirect(url_for('index'))
            

        elif username == 'user' and password == 'user123':
            session['logged_in'] = True
            session['username'] = 'Test-User'
            session['role'] = 'user'
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('index'))
            

        else:
            flash('Ungültige Zugangsdaten!', 'danger')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sie wurden erfolgreich abgemeldet.', 'info')
    return redirect(url_for('login'))  

@app.route('/')
def index():
    # Abfrage der Gesamtzahl der Datensätze über das SQLAlchemy-Modell
    total_customers = len(Customer.get_all_customers())
    total_leads = len(Lead.get_all_leads())
    return render_template('index.html', total_customers=total_customers, total_leads=total_leads)

# --- CUSTOMER ROUTES ---
@app.route('/customers')
def customers():
    # Rückgabe der Kundenliste aus der Datenbank
    return render_template('customers.html', customers=Customer.get_all_customers())

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        phone = request.form.get('phone')
        status = request.form.get('status', 'prospect')

        if not all([name, email, company, phone]):
            flash('Alle Felder sind erforderlich!', 'error')
            return redirect(url_for('add_customer'))

        # Speichert den neuen Kunden permanent in der Datenbank
        Customer.add_customer(name, email, company, phone, status)
        flash(f'Kunde {name} wurde erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html')

@app.route('/customers/<int:customer_id>')
def customer_detail(customer_id):
    # Abrufen eines spezifischen Kunden anhand seiner ID
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Kunde nicht gefunden!', 'error')
        return redirect(url_for('customers'))
    return render_template('customer_detail.html', customer=customer)

# --- NEU (Sprint 2): Bearbeiten-Route mit Datenbank-Commit ---
@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    # Suche nach dem zu bearbeitenden Datensatz
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Kunde nicht gefunden!', 'error')
        return redirect(url_for('customers'))

    if request.method == 'POST':
        # Aktualisierung der Objektattribute durch Formular-Daten
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.company = request.form.get('company')
        customer.phone = request.form.get('phone')
        customer.status = request.form.get('status')

        # --- WICHTIG: Speichern der Änderungen dauerhaft in der Datenbank ---
        db.session.commit()
        
        flash('Kundendaten erfolgreich aktualisiert!', 'success')
        return redirect(url_for('customer_detail', customer_id=customer.id))

    return render_template('edit_customer.html', customer=customer)

# --- NEU (Sprint 2): Löschfunktion für Kunden ---
@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    # Entfernt den Datensatz über die Methode im Modell
    Customer.delete_customer(customer_id)
    flash('Kunde wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('customers'))

# --- NEU: LEADS ROUTES ---
@app.route('/leads')
def leads():
    """Zeigt die Liste aller Leads aus der Datenbank an"""
    return render_template('leads.html', leads=Lead.get_all_leads())

@app.route('/leads/<int:lead_id>')
def lead_detail(lead_id):
    """Zeigt detaillierte Informationen zu einem Lead"""
    lead = Lead.get_lead_by_id(lead_id)
    if not lead:
        flash('Lead nicht gefunden!', 'error')
        return redirect(url_for('leads'))
    return render_template('lead_detail.html', lead=lead)

@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
def delete_lead(lead_id):
    """Löscht einen spezifischen Lead permanent"""
    Lead.delete_lead(lead_id)
    flash('Lead erfolgreich gelöscht!', 'success')
    return redirect(url_for('leads'))

@app.route('/leads/add', methods=['GET', 'POST'])
def add_lead():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        value = request.form.get('value')
        source = request.form.get('source')

        if not all([name, email, company, value, source]):
            flash('Alle Felder sind erforderlich!', 'error')
            return redirect(url_for('add_lead'))

        try:
            # Konvertierung des Deal-Werts und Speicherung
            Lead.add_lead(name, email, company, float(value), source)
            flash(f'Lead {name} wurde erfolgreich hinzugefügt!', 'success')
        except ValueError:
            flash('Der Deal-Wert muss eine Zahl sein!', 'error')

        return redirect(url_for('leads'))
    return render_template('add_lead.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Startet den Server im Debug-Modus für die Entwicklung
    app.run(debug=True, host='127.0.0.1', port=5000)