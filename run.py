from flask import Flask, render_template, redirect, url_for, session, flash, request
import os
import logging
import sys

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'maintenance_guide_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_guide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# استيراد نماذج قاعدة البيانات
from src.models.models import db, User, Customer, Technician, Order, Invoice
db.init_app(app)

# استيراد مسارات التطبيق
from src.routes.auth import auth_bp
from src.routes.orders import orders_bp
from src.routes.technicians import technicians_bp
from src.routes.invoices import invoices_bp
from src.routes.api import api_bp

# تسجيل مسارات التطبيق
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(technicians_bp, url_prefix='/technicians')
app.register_blueprint(invoices_bp, url_prefix='/invoices')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('يجب تسجيل الدخول أولاً', 'error')
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"404 خطأ: {str(e)}")
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 خطأ: {str(e)}")
    return render_template('errors/500.html'), 500

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

if __name__ == '__main__':
    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        db.create_all()
        
        # إنشاء مستخدم مسؤول افتراضي إذا لم يكن موجوداً
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                full_name='مدير النظام',
                email='admin@example.com',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            logger.info('تم إنشاء مستخدم مسؤول افتراضي')
    
    # تشغيل التطبيق
    app.run(host='0.0.0.0', port=5000, debug=True)
