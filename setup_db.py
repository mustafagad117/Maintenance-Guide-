import os
import sys
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# إضافة مسار المشروع إلى مسارات النظام
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# إنشاء تطبيق Flask مؤقت لإعداد قاعدة البيانات
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_guide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# تعريف نماذج قاعدة البيانات
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='user')  # admin, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone1 = db.Column(db.String(20), nullable=False)
    phone2 = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقة مع الأوردرات
    orders = db.relationship('Order', backref='customer', lazy=True)

class Technician(db.Model):
    __tablename__ = 'technicians'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    specialization = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقة مع الأوردرات
    orders = db.relationship('Order', backref='technician', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)  # غسالة، ثلاجة، بوتاجاز، سخان، شاشة، تكييف، ديب فريزر، مجفف، أخرى
    brand = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)  # تحت المتابعة، تم الإصلاح، تأجيل، رفض، كشف
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقة مع الفاتورة
    invoice = db.relationship('Invoice', backref='order', lazy=True, uselist=False)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    service_description = db.Column(db.Text, nullable=False)
    parts_cost = db.Column(db.Float, default=0)
    service_cost = db.Column(db.Float, default=0)
    total_cost = db.Column(db.Float, nullable=False)
    warranty_months = db.Column(db.Integer, default=12)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def setup_database():
    with app.app_context():
        # إنشاء جميع الجداول
        db.create_all()
        
        # إنشاء مستخدم مسؤول افتراضي إذا لم يكن موجوداً
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                full_name='مدير النظام',
                email='admin@example.com',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('تم إنشاء مستخدم مسؤول افتراضي')
        else:
            print('المستخدم المسؤول موجود بالفعل')

if __name__ == '__main__':
    setup_database()
    print('تم إعداد قاعدة البيانات بنجاح')
