from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    """
    Basierend auf dem Lehrer-Code, aber erweitert auf SQLAlchemy (Kap. 3.4)
    """
    __tablename__ = 'customers'
    
    # SQLAlchemy übernimmt die ID-Verwaltung (kein next_id nötig)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default="prospect")

    @classmethod
    def add_customer(cls, name, email, company, phone, status="prospect"):
        # Ersetzt cls.customers.append()
        new_customer = cls(name=name, email=email, company=company, phone=phone, status=status)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @classmethod
    def get_all_customers(cls):
        # Ersetzt return cls.customers
        return cls.query.all()

    @classmethod
    def get_customer_by_id(cls, customer_id):
        return cls.query.get(customer_id)

    @classmethod
    def delete_customer(cls, customer_id):
        customer = cls.get_customer_by_id(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()

class Lead(db.Model):
    """
    Basierend auf dem Lehrer-Code, erweitert für Persistenz (Sprint 2)
    """
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    company = db.Column(db.String(100))
    value = db.Column(db.Float)
    source = db.Column(db.String(50))
    status = db.Column(db.String(20), default="new")

    
    @classmethod
    def get_all_leads(cls):
        """Gibt alle Leads aus der Datenbank zurück"""
        return cls.query.all()

    @classmethod
    def add_lead(cls, name, email, company, value, source):
        """Speichert einen neuen Lead in der Datenbank"""
        new_lead = cls(name=name, email=email, company=company, value=value, source=source)
        db.session.add(new_lead)
        db.session.commit()
        return new_lead
    
    @classmethod
    def get_lead_by_id(cls, lead_id):
        return cls.query.get(lead_id)

    @classmethod
    def delete_lead(cls, lead_id):
        lead = cls.get_lead_by_id(lead_id)
        if lead:
            db.session.delete(lead)
            db.session.commit()

    @classmethod
    def add_lead(cls, name, email, company, value, source):
        new_lead = cls(name=name, email=email, company=company, value=value, source=source)
        db.session.add(new_lead)
        db.session.commit()
        return new_lead

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        password = db.Column(db.String(120))
        role = db.Column(db.String(20), default='user') # 'admin', 'user', 'guest'