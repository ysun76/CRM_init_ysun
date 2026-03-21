from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Customer, Lead 
from functools import wraps
from flasgger import Swagger
    
app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihr-geheimschlüssel-hier'

# Initialize Database and Swagger
db.init_app(app)
swagger = Swagger(app)

# --- RBAC Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Bitte loggen Sie sich ein.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Zugriff verweigert: Admin-Rechte erforderlich!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['logged_in'] = True
            session['username'] = user.username
            session['role'] = user.role
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ungültige Zugangsdaten!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Erfolgreich abgemeldet.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Basis-Statistiken abrufen
    total_customers = Customer.query.count()
    total_leads = Lead.query.count()
    
    # --- Sprint 3: Statistiken für das Dashboard-Diagramm ---
    # Anzahl der aktiven Kunden ermitteln 
    active_count = Customer.query.filter_by(status='active').count()
    # Anzahl der Interessenten (Prospects) ermitteln 
    prospect_count = Customer.query.filter_by(status='prospect').count()
    
    # Daten an das Frontend-Template übergeben
    return render_template('index.html', 
                           total_customers=total_customers, 
                           total_leads=total_leads,
                           active_count=active_count,
                           prospect_count=prospect_count)

# --- Customer Management Routes ---
@app.route('/customers')
@login_required
def customers():
    return render_template('customers.html', customers=Customer.get_all_customers())

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        phone = request.form.get('phone')
        status = request.form.get('status', 'prospect')
        
        if not all([name, email, company, phone]):
            flash('Alle Felder sind Pflichtfelder!', 'error')
            return redirect(url_for('add_customer'))
            
        Customer.add_customer(name, email, company, phone, status)
        flash(f'Kunde {name} wurde hinzugefügt!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html')

@app.route('/customers/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Kunde nicht gefunden!', 'error')
        return redirect(url_for('customers'))
    return render_template('customer_detail.html', customer=customer)

@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_customer(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Kunde nicht gefunden!', 'error')
        return redirect(url_for('customers'))
        
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.company = request.form.get('company')
        customer.phone = request.form.get('phone')
        customer.status = request.form.get('status')
        db.session.commit()
        flash('Kundendaten aktualisiert!', 'success')
        return redirect(url_for('customer_detail', customer_id=customer.id))
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_customer(customer_id):
    Customer.delete_customer(customer_id)
    flash('Kunde gelöscht!', 'success')
    return redirect(url_for('customers'))

# --- API Routes ---
@app.route('/api/stats', methods=['GET'])
def api_stats():
    """
    Abrufen der Systemstatistiken
    ---
    responses:
      200:
        description: Gibt die Anzahl der Kunden und Leads zurück
    """
    c_count = Customer.query.count()
    l_count = Lead.query.count()
    return jsonify({
        "project": "USME_CRM_SYSTEM",
        "data": {
            "total_customers": c_count,
            "total_leads": l_count
        }
    })

@app.route('/api/customers', methods=['GET'])
@login_required
def get_customers_api():
    """
    Liste aller Kunden im JSON-Format
    ---
    responses:
      200:
        description: Eine Liste aller Kunden
    """
    customers_list = Customer.get_all_customers()
    return jsonify([{
        'id': c.id, 
        'name': c.name, 
        'email': c.email,
        'company': c.company,
        'status': c.status
    } for c in customers_list])

# --- Leads Routes ---
@app.route('/leads')
@login_required
def leads():
    return render_template('leads.html', leads=Lead.get_all_leads())

@app.route('/leads/<int:lead_id>')
@login_required
def lead_detail(lead_id):
    lead = Lead.get_lead_by_id(lead_id)
    if not lead:
        flash('Lead nicht gefunden!', 'error')
        return redirect(url_for('leads'))
    return render_template('lead_detail.html', lead=lead)

@app.route('/leads/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lead():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        value = request.form.get('value')
        source = request.form.get('source')
        
        try:
            Lead.add_lead(name, email, company, float(value), source)
            flash(f'Lead {name} erfolgreich erstellt!', 'success')
        except (ValueError, TypeError):
            flash('Der Wert muss eine Zahl sein!', 'error')
        return redirect(url_for('leads'))
    return render_template('add_lead.html')

@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_lead(lead_id):
    Lead.delete_lead(lead_id)
    flash('Lead gelöscht!', 'success')
    return redirect(url_for('leads'))

@app.route('/convert_lead/<int:lead_id>', methods=['POST'])
@login_required
def convert_lead(lead_id):
    # Den zu konvertierenden Lead aus der Datenbank abrufen (德语注释)
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        # Einen neuen Kunden auf Basis der Lead-Daten erstellen (德语注释)
        # Wir nutzen getattr, falls das 'phone'-Attribut im Lead-Model fehlt
        new_customer = Customer(
            name=lead.name,
            email=lead.email,
            company=lead.company,
            phone=getattr(lead, 'phone', 'Keine Angabe'), # Sicherer Zugriff 
            status='active'  # Standardmäßig als aktiver Kunde anlegen
        )
        
        # Den neuen Kunden hinzufügen und den alten Lead löschen 
        db.session.add(new_customer)
        db.session.delete(lead)
        
        # Änderungen in der Datenbank speichern 
        db.session.commit()
        
        flash(f'Erfolg: {lead.name} wurde erfolgreich in einen Kunden umgewandelt!', 'success')
    except Exception as e:
        # Bei Fehlern die Transaktion zurückrollen 
        db.session.rollback()
        flash(f'Fehler bei der Konvertierung: {str(e)}', 'error')
        
    return redirect(url_for('customers'))

# --- Error Handling ---
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# --- Main Entry Point ---
if __name__ == '__main__':
    with app.app_context():
        # 1. Create tables
        db.create_all()
        
        # 2. Create Admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('password123')
            db.session.add(admin)
            print("Admin account created: admin / password123")

        if not User.query.filter_by(username='user1').first():
            standard_user = User(username='user1', role='user') # Rolle ist 'user'
            standard_user.set_password('user123')
            db.session.add(standard_user)
            
        # 3. Load demo data if database is empty
        if not Customer.query.first():
            customer_data = [
                ('John Doe', 'john@example.com', 'Acme Corp', '555-0001', 'active'),
                ('Jane Smith', 'jane@example.com', 'Tech Solutions', '555-0002', 'prospect'),
                ('Max Mustermann', 'max@test.de', 'Berlin Tech', '030-12345', 'active'),
                ('Erika Muster', 'erika@web.de', 'Muster AG', '089-98765', 'prospect'),
                ('BMW Group', 'contact@bmw.de', 'Automotive', '089-11111', 'active'),
                ('Siemens', 'info@siemens.com', 'Energy', '0911-2222', 'active')
            ]
            for n, e, c, p, s in customer_data:
                Customer.add_customer(n, e, c, p, s)
            
            Lead.add_lead('Alice Brown', 'alice@example.com', 'StartUp Inc', 50000.0, 'Website')
            Lead.add_lead('Portfolio Project', 'invest@finance.com', 'Global Invest', 250000.0, 'Referral')
            print("Demo data loaded successfully.")
            
        db.session.commit()
        print("CRM System is ready.")

        
       

    # Start Server
    app.run(debug=True, host='127.0.0.1', port=5000)