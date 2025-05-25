#!/bin/bash

# سكريبت تثبيت وتشغيل نظام Maintenance Guide

echo "بدء تثبيت نظام Maintenance Guide..."

# التأكد من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "يرجى تثبيت Python 3 أولاً"
    exit 1
fi

# إنشاء بيئة افتراضية
echo "إنشاء بيئة افتراضية..."
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
echo "تثبيت المتطلبات البرمجية..."
pip install -r requirements.txt

# إنشاء قاعدة البيانات
echo "إنشاء قاعدة البيانات وإعداد المستخدم الافتراضي..."
python setup_db.py

# تشغيل التطبيق
echo "تشغيل التطبيق..."
echo "يمكنك الوصول إلى التطبيق عبر الرابط: http://localhost:5000"
echo "بيانات تسجيل الدخول الافتراضية:"
echo "اسم المستخدم: admin"
echo "كلمة المرور: admin123"
python run.py
