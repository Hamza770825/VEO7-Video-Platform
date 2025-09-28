#!/bin/bash

# ===========================================
# VEO7 Video Platform - Deployment Script
# ===========================================

set -e

# ألوان للنصوص
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# متغيرات التكوين
ENVIRONMENT=${1:-production}
BUILD_FRONTEND=${BUILD_FRONTEND:-true}
BUILD_BACKEND=${BUILD_BACKEND:-true}
PUSH_IMAGES=${PUSH_IMAGES:-false}
REGISTRY=${REGISTRY:-""}

# عرض المساعدة
show_help() {
    echo "استخدام: $0 [ENVIRONMENT] [OPTIONS]"
    echo ""
    echo "ENVIRONMENT:"
    echo "  development  - نشر للتطوير"
    echo "  staging      - نشر للاختبار"
    echo "  production   - نشر للإنتاج (افتراضي)"
    echo ""
    echo "OPTIONS:"
    echo "  --no-frontend     تخطي بناء Frontend"
    echo "  --no-backend      تخطي بناء Backend"
    echo "  --push-images     رفع الصور إلى Registry"
    echo "  --registry=URL    عنوان Docker Registry"
    echo "  --help           عرض هذه المساعدة"
    echo ""
    echo "أمثلة:"
    echo "  $0 production"
    echo "  $0 staging --push-images --registry=myregistry.com"
    echo "  $0 development --no-backend"
}

# معالجة المعاملات
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-frontend)
                BUILD_FRONTEND=false
                shift
                ;;
            --no-backend)
                BUILD_BACKEND=false
                shift
                ;;
            --push-images)
                PUSH_IMAGES=true
                shift
                ;;
            --registry=*)
                REGISTRY="${1#*=}"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                if [[ -z "$ENVIRONMENT" ]]; then
                    ENVIRONMENT="$1"
                fi
                shift
                ;;
        esac
    done
}

# التحقق من المتطلبات
check_requirements() {
    print_step "التحقق من المتطلبات..."
    
    # التحقق من Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker غير مثبت"
        exit 1
    fi
    
    # التحقق من Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose غير مثبت"
        exit 1
    fi
    
    # التحقق من ملفات البيئة
    if [ ! -f ".env" ]; then
        print_error "ملف .env غير موجود"
        exit 1
    fi
    
    print_message "جميع المتطلبات متوفرة ✓"
}

# تحضير البيئة
prepare_environment() {
    print_step "تحضير بيئة $ENVIRONMENT..."
    
    # نسخ ملف البيئة المناسب
    case $ENVIRONMENT in
        development)
            ENV_FILE=".env.development"
            ;;
        staging)
            ENV_FILE=".env.staging"
            ;;
        production)
            ENV_FILE=".env.production"
            ;;
        *)
            ENV_FILE=".env"
            ;;
    esac
    
    if [ -f "$ENV_FILE" ]; then
        cp "$ENV_FILE" .env
        print_message "تم استخدام ملف البيئة: $ENV_FILE"
    else
        print_warning "ملف البيئة $ENV_FILE غير موجود، سيتم استخدام .env الافتراضي"
    fi
}

# بناء Frontend
build_frontend() {
    if [ "$BUILD_FRONTEND" = true ]; then
        print_step "بناء Frontend..."
        
        cd frontend
        
        # تثبيت التبعيات
        print_message "تثبيت تبعيات Frontend..."
        npm ci --only=production
        
        # بناء التطبيق
        print_message "بناء Frontend..."
        npm run build
        
        cd ..
        print_message "تم بناء Frontend بنجاح ✓"
    else
        print_warning "تم تخطي بناء Frontend"
    fi
}

# بناء Backend
build_backend() {
    if [ "$BUILD_BACKEND" = true ]; then
        print_step "بناء Backend..."
        
        cd backend
        
        # التحقق من ملف المتطلبات
        if [ ! -f "requirements.txt" ]; then
            print_error "ملف requirements.txt غير موجود"
            exit 1
        fi
        
        cd ..
        print_message "تم التحقق من Backend بنجاح ✓"
    else
        print_warning "تم تخطي بناء Backend"
    fi
}

# بناء صور Docker
build_docker_images() {
    print_step "بناء صور Docker..."
    
    # تحديد العلامات
    if [ -n "$REGISTRY" ]; then
        FRONTEND_TAG="$REGISTRY/veo7-frontend:$ENVIRONMENT"
        BACKEND_TAG="$REGISTRY/veo7-backend:$ENVIRONMENT"
    else
        FRONTEND_TAG="veo7-frontend:$ENVIRONMENT"
        BACKEND_TAG="veo7-backend:$ENVIRONMENT"
    fi
    
    # بناء Frontend
    if [ "$BUILD_FRONTEND" = true ]; then
        print_message "بناء صورة Frontend..."
        docker build -t "$FRONTEND_TAG" ./frontend
    fi
    
    # بناء Backend
    if [ "$BUILD_BACKEND" = true ]; then
        print_message "بناء صورة Backend..."
        docker build -t "$BACKEND_TAG" ./backend
    fi
    
    print_message "تم بناء صور Docker بنجاح ✓"
}

# رفع الصور
push_images() {
    if [ "$PUSH_IMAGES" = true ] && [ -n "$REGISTRY" ]; then
        print_step "رفع الصور إلى Registry..."
        
        if [ "$BUILD_FRONTEND" = true ]; then
            print_message "رفع صورة Frontend..."
            docker push "$REGISTRY/veo7-frontend:$ENVIRONMENT"
        fi
        
        if [ "$BUILD_BACKEND" = true ]; then
            print_message "رفع صورة Backend..."
            docker push "$REGISTRY/veo7-backend:$ENVIRONMENT"
        fi
        
        print_message "تم رفع الصور بنجاح ✓"
    else
        print_warning "تم تخطي رفع الصور"
    fi
}

# نشر التطبيق
deploy_application() {
    print_step "نشر التطبيق..."
    
    # إيقاف الخدمات الحالية
    print_message "إيقاف الخدمات الحالية..."
    docker-compose down || true
    
    # تنظيف الصور القديمة
    print_message "تنظيف الصور القديمة..."
    docker system prune -f || true
    
    # تشغيل الخدمات الجديدة
    print_message "تشغيل الخدمات الجديدة..."
    docker-compose up -d
    
    # انتظار تشغيل الخدمات
    print_message "انتظار تشغيل الخدمات..."
    sleep 30
    
    # التحقق من حالة الخدمات
    print_message "التحقق من حالة الخدمات..."
    docker-compose ps
    
    print_message "تم نشر التطبيق بنجاح ✓"
}

# اختبار النشر
test_deployment() {
    print_step "اختبار النشر..."
    
    # اختبار Backend
    print_message "اختبار Backend..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_message "Backend يعمل بشكل صحيح ✓"
    else
        print_error "Backend لا يعمل بشكل صحيح"
        return 1
    fi
    
    # اختبار Frontend
    print_message "اختبار Frontend..."
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_message "Frontend يعمل بشكل صحيح ✓"
    else
        print_error "Frontend لا يعمل بشكل صحيح"
        return 1
    fi
    
    print_message "جميع الاختبارات نجحت ✓"
}

# إنشاء نسخة احتياطية
create_backup() {
    print_step "إنشاء نسخة احتياطية..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # نسخ احتياطية من قاعدة البيانات (إذا كانت محلية)
    if docker-compose ps | grep -q database; then
        print_message "إنشاء نسخة احتياطية من قاعدة البيانات..."
        docker-compose exec -T database pg_dump -U veo7_user veo7 > "$BACKUP_DIR/database.sql"
    fi
    
    # نسخ احتياطية من الملفات المرفوعة
    if [ -d "backend/uploads" ]; then
        print_message "إنشاء نسخة احتياطية من الملفات..."
        cp -r backend/uploads "$BACKUP_DIR/"
    fi
    
    print_message "تم إنشاء النسخة الاحتياطية في: $BACKUP_DIR ✓"
}

# تنظيف النسخ الاحتياطية القديمة
cleanup_old_backups() {
    print_step "تنظيف النسخ الاحتياطية القديمة..."
    
    # الاحتفاظ بآخر 5 نسخ احتياطية فقط
    if [ -d "backups" ]; then
        cd backups
        ls -t | tail -n +6 | xargs -r rm -rf
        cd ..
        print_message "تم تنظيف النسخ الاحتياطية القديمة ✓"
    fi
}

# الدالة الرئيسية
main() {
    echo "================================================"
    echo "🚀 VEO7 Video Platform - Deployment Script"
    echo "================================================"
    echo ""
    
    parse_args "$@"
    
    print_message "بدء النشر للبيئة: $ENVIRONMENT"
    print_message "بناء Frontend: $BUILD_FRONTEND"
    print_message "بناء Backend: $BUILD_BACKEND"
    print_message "رفع الصور: $PUSH_IMAGES"
    
    if [ -n "$REGISTRY" ]; then
        print_message "Registry: $REGISTRY"
    fi
    
    echo ""
    
    check_requirements
    create_backup
    prepare_environment
    build_frontend
    build_backend
    build_docker_images
    push_images
    deploy_application
    test_deployment
    cleanup_old_backups
    
    echo ""
    echo "================================================"
    echo "✅ تم النشر بنجاح!"
    echo "================================================"
    echo ""
    echo "معلومات النشر:"
    echo "  البيئة: $ENVIRONMENT"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo ""
    echo "للمراقبة:"
    echo "  docker-compose logs -f"
    echo "  docker-compose ps"
    echo ""
}

# تشغيل الدالة الرئيسية
main "$@"