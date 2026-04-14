from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Customer, Lead
from functools import wraps
from flasgger import Swagger
import os

app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ihr-geheimschlüssel-hier')

# Initialize Database and Swagger
db.init_app(app)
swagger = Swagger(app)

# --- RBAC Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Access denied: Admin rights required!', 'danger')
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
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    total_customers = Customer.query.count()
    total_leads = Lead.query.count()
    active_count = Customer.query.filter_by(status='active').count()
    prospect_count = Customer.query.filter_by(status='prospect').count()
    
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
            flash('All fields are required!', 'error')
            return redirect(url_for('add_customer'))
            
        Customer.add_customer(name, email, company, phone, status)
        flash(f'Customer {name} has been added!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html')


@app.route('/customers/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Customer not found!', 'error')
        return redirect(url_for('customers'))
    return render_template('customer_detail.html', customer=customer)


@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_customer(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Customer not found!', 'error')
        return redirect(url_for('customers'))
        
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.company = request.form.get('company')
        customer.phone = request.form.get('phone')
        customer.status = request.form.get('status')
        db.session.commit()
        flash('Customer data updated!', 'success')
        return redirect(url_for('customer_detail', customer_id=customer.id))
    return render_template('edit_customer.html', customer=customer)


@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_customer(customer_id):
    Customer.delete_customer(customer_id)
    flash('Customer deleted!', 'success')
    return redirect(url_for('customers'))


# --- API Routes ---
@app.route('/api/stats', methods=['GET'])
def api_stats():
    """
    Get system statistics
    ---
    tags:
      - API-Management
    responses:
      200:
        description: Statistics retrieved successfully
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



@app.route('/api/customers', methods=['POST'])
def add_customer_api():
    """
    Einen neuen Kunden über API anlegen (Finaler Fix)
    ---
    tags:
      - API-Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                name:
                    type: string
                email:
                    type: string
                company:
                    type: string
                phone:
                    type: string
    responses:
      201:
        description: Kunde erfolgreich erstellt
      400:
        description: Name oder Email fehlt
    """
    # 强制读取 JSON 请求体（你就是这么提交的！）
    data = request.get_json(silent=True) or {}
    
    name = data.get('name')
    email = data.get('email')
    company = data.get('company', 'N/A')
    phone = data.get('phone', '000000')

    if not name or not email:
        return jsonify({
            "status": "error",
            "message": "Name und Email sind erforderlich.",
            "debug": f"Empfangen: name={name}, email={email}"
        }), 400

    try:
        Customer.add_customer(
            name=name,
            email=email,
            company=company,
            phone=phone,
            status='prospect'
        )
        return jsonify({
            "status": "success",
            "message": f"Kunde {name} wurde über die API angelegt."
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_api(customer_id):
    """
    Delete a customer via API
    ---
    tags:
      - API-Management
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Customer deleted
      404:
        description: Not found
    """
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"status": "error", "message": "Customer not found"}), 404
        
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"status": "success", "message": f"Customer {customer_id} deleted"}), 200


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
        flash('Lead not found!', 'error')
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
            flash(f'Lead {name} created successfully!', 'success')
        except (ValueError, TypeError):
            flash('Value must be a number!', 'error')
        return redirect(url_for('leads'))
    return render_template('add_lead.html')


@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_lead(lead_id):
    Lead.delete_lead(lead_id)
    flash('Lead deleted!', 'success')
    return redirect(url_for('leads'))


@app.route('/convert_lead/<int:lead_id>', methods=['POST'])
@login_required
def convert_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        new_customer = Customer(
            name=lead.name,
            email=lead.email,
            company=lead.company,
            phone=getattr(lead, 'phone', 'No information'),
            status='active'
        )
        
        db.session.add(new_customer)
        db.session.delete(lead)
        db.session.commit()
        
        flash(f'Success: {lead.name} has been converted to a customer!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Conversion error: {str(e)}', 'error')
        
    return redirect(url_for('customers'))


# --- Error Handling ---
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# --- Main Entry Point ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('password123')
            db.session.add(admin)
            print("Admin account created: admin / password123")

        if not User.query.filter_by(username='user1').first():
            standard_user = User(username='user1', role='user')
            standard_user.set_password('user123')
            db.session.add(standard_user)
            
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

    app.run(debug=True, host='127.0.0.1', port=5000)