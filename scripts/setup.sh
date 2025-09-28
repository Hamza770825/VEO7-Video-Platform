#!/bin/bash

# ===========================================
# VEO7 Video Platform - Setup Script
# ===========================================

set -e

echo "🚀 بدء إعداد منصة VEO7..."

# ألوان للنصوص
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة لطباعة الرسائل الملونة
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# التحقق من المتطلبات الأساسية
check_requirements() {
    print_step "التحقق من المتطلبات الأساسية..."
    
    # التحقق من Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js غير مثبت. يرجى تثبيت Node.js 18 أو أحدث."
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "يتطلب Node.js الإصدار 18 أو أحدث. الإصدار الحالي: $(node -v)"
        exit 1
    fi
    
    # التحقق من Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت. يرجى تثبيت Python 3.11 أو أحدث."
        exit 1
    fi
    
    # التحقق من Docker (اختياري)
    if command -v docker &> /dev/null; then
        print_message "Docker متوفر ✓"
    else
        print_warning "Docker غير مثبت. ستحتاج إليه للنشر."
    fi
    
    print_message "جميع المتطلبات متوفرة ✓"
}

# إنشاء ملفات البيئة
setup_environment() {
    print_step "إعداد ملفات البيئة..."
    
    # نسخ ملف البيئة الرئيسي
    if [ ! -f .env ]; then
        cp .env.example .env
        print_message "تم إنشاء ملف .env"
    else
        print_warning "ملف .env موجود بالفعل"
    fi
    
    # نسخ ملف البيئة للـ Frontend
    if [ ! -f frontend/.env.local ]; then
        cp .env.example frontend/.env.local
        print_message "تم إنشاء ملف frontend/.env.local"
    else
        print_warning "ملف frontend/.env.local موجود بالفعل"
    fi
    
    # نسخ ملف البيئة للـ Backend
    if [ ! -f backend/.env ]; then
        cp .env.example backend/.env
        print_message "تم إنشاء ملف backend/.env"
    else
        print_warning "ملف backend/.env موجود بالفعل"
    fi
}

# إعداد Frontend
setup_frontend() {
    print_step "إعداد Frontend..."
    
    cd frontend
    
    print_message "تثبيت تبعيات Frontend..."
    npm install
    
    print_message "بناء Frontend..."
    npm run build
    
    cd ..
    print_message "تم إعداد Frontend بنجاح ✓"
}

# إعداد Backend
setup_backend() {
    print_step "إعداد Backend..."
    
    cd backend
    
    # إنشاء البيئة الافتراضية
    if [ ! -d "venv" ]; then
        print_message "إنشاء البيئة الافتراضية..."
        python3 -m venv venv
    fi
    
    # تفعيل البيئة الافتراضية
    source venv/bin/activate
    
    # تثبيت المتطلبات
    print_message "تثبيت تبعيات Backend..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # إنشاء المجلدات المطلوبة
    mkdir -p uploads outputs temp
    
    cd ..
    print_message "تم إعداد Backend بنجاح ✓"
}

# إعداد قاعدة البيانات
setup_database() {
    print_step "إعداد قاعدة البيانات..."
    
    print_warning "يرجى التأكد من إعداد Supabase وتشغيل ملفات SQL التالية:"
    echo "  - backend/database/schema.sql"
    echo "  - backend/database/seed.sql"
    
    print_message "يمكنك تشغيلها في Supabase SQL Editor"
}

# إنشاء شهادات SSL للتطوير
setup_ssl() {
    print_step "إنشاء شهادات SSL للتطوير..."
    
    mkdir -p nginx/ssl
    
    if [ ! -f nginx/ssl/cert.pem ]; then
        print_message "إنشاء شهادة SSL ذاتية التوقيع..."
        openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=SA/ST=Riyadh/L=Riyadh/O=VEO7/CN=localhost"
        print_message "تم إنشاء شهادات SSL ✓"
    else
        print_warning "شهادات SSL موجودة بالفعل"
    fi
}

# إنشاء سكريبتات التشغيل
create_scripts() {
    print_step "إنشاء سكريبتات التشغيل..."
    
    # سكريبت تشغيل التطوير
    cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 بدء تشغيل VEO7 في وضع التطوير..."

# تشغيل Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# تشغيل Frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ تم تشغيل التطبيق:"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# انتظار إيقاف العمليات
wait $BACKEND_PID $FRONTEND_PID
EOF

    chmod +x start-dev.sh
    
    # سكريبت تشغيل الإنتاج
    cat > start-prod.sh << 'EOF'
#!/bin/bash
echo "🚀 بدء تشغيل VEO7 في وضع الإنتاج..."

# التحقق من Docker
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose غير مثبت"
    exit 1
fi

# تشغيل الخدمات
docker-compose up -d

echo "✅ تم تشغيل التطبيق:"
echo "   Application: https://localhost"
echo "   HTTP: http://localhost:8080"
EOF

    chmod +x start-prod.sh
    
    print_message "تم إنشاء سكريبتات التشغيل ✓"
}

# الدالة الرئيسية
main() {
    echo "================================================"
    echo "🎬 VEO7 Video Platform - Setup Script"
    echo "================================================"
    echo ""
    
    check_requirements
    setup_environment
    setup_frontend
    setup_backend
    setup_database
    setup_ssl
    create_scripts
    
    echo ""
    echo "================================================"
    echo "✅ تم إعداد المشروع بنجاح!"
    echo "================================================"
    echo ""
    echo "الخطوات التالية:"
    echo "1. قم بتحديث ملفات .env بالقيم الصحيحة"
    echo "2. أعد إعداد قاعدة البيانات في Supabase"
    echo "3. شغل التطبيق:"
    echo "   - للتطوير: ./start-dev.sh"
    echo "   - للإنتاج: ./start-prod.sh"
    echo ""
    echo "📚 للمزيد من المعلومات، راجع README.md"
    echo ""
}

# تشغيل الدالة الرئيسية
main "$@"