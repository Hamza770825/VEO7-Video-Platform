# دليل النشر الشامل لمنصة VEO7 مع ميزات الذكاء الاصطناعي
# VEO7 Platform Comprehensive Deployment Guide with AI Features

## 📋 جدول المحتويات / Table of Contents

1. [متطلبات النظام / System Requirements](#متطلبات-النظام--system-requirements)
2. [إعداد البيئة / Environment Setup](#إعداد-البيئة--environment-setup)
3. [تثبيت التبعيات / Dependencies Installation](#تثبيت-التبعيات--dependencies-installation)
4. [إعداد قاعدة البيانات / Database Setup](#إعداد-قاعدة-البيانات--database-setup)
5. [إعداد نماذج الذكاء الاصطناعي / AI Models Setup](#إعداد-نماذج-الذكاء-الاصطناعي--ai-models-setup)
6. [النشر المحلي / Local Deployment](#النشر-المحلي--local-deployment)
7. [النشر على الإنتاج / Production Deployment](#النشر-على-الإنتاج--production-deployment)
8. [المراقبة والصيانة / Monitoring and Maintenance](#المراقبة-والصيانة--monitoring-and-maintenance)
9. [استكشاف الأخطاء / Troubleshooting](#استكشاف-الأخطاء--troubleshooting)

---

## متطلبات النظام / System Requirements

### الحد الأدنى / Minimum Requirements
- **المعالج / CPU**: Intel i5 أو AMD Ryzen 5 (4 cores)
- **الذاكرة / RAM**: 8 GB
- **التخزين / Storage**: 50 GB مساحة فارغة
- **نظام التشغيل / OS**: Windows 10/11, Ubuntu 20.04+, macOS 12+

### الموصى به / Recommended Requirements
- **المعالج / CPU**: Intel i7 أو AMD Ryzen 7 (8+ cores)
- **الذاكرة / RAM**: 16 GB أو أكثر
- **كرت الرسوميات / GPU**: NVIDIA GTX 1060 أو أفضل (للذكاء الاصطناعي)
- **التخزين / Storage**: 100 GB SSD
- **الشبكة / Network**: اتصال إنترنت مستقر

### متطلبات الذكاء الاصطناعي / AI Requirements
- **CUDA**: إصدار 11.8 أو أحدث (للمعالجة بـ GPU)
- **cuDNN**: إصدار 8.6 أو أحدث
- **Python**: 3.9 - 3.11
- **VRAM**: 6 GB أو أكثر (للنماذج المتقدمة)

---

## إعداد البيئة / Environment Setup

### 1. تثبيت Python
```bash
# Windows
# تحميل Python من python.org

# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# macOS
brew install python@3.10
```

### 2. تثبيت Node.js
```bash
# Windows
# تحميل Node.js من nodejs.org

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node@18
```

### 3. تثبيت Git
```bash
# Windows
# تحميل Git من git-scm.com

# Ubuntu/Debian
sudo apt install git

# macOS
brew install git
```

### 4. تثبيت Docker (اختياري)
```bash
# Windows
# تحميل Docker Desktop من docker.com

# Ubuntu
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose
```

---

## تثبيت التبعيات / Dependencies Installation

### 1. استنساخ المشروع / Clone Project
```bash
git clone https://github.com/your-username/VEO7-Video-Platform.git
cd VEO7-Video-Platform
```

### 2. إعداد البيئة الافتراضية / Virtual Environment
```bash
# إنشاء البيئة الافتراضية
python -m venv .venv

# تفعيل البيئة الافتراضية
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. تثبيت تبعيات Python
```bash
# التبعيات الأساسية
pip install -r backend/requirements.txt

# تبعيات الذكاء الاصطناعي (اختياري)
pip install -r backend/requirements_ai_models.txt
```

### 4. تثبيت تبعيات Node.js
```bash
cd frontend
npm install
cd ..
```

---

## إعداد قاعدة البيانات / Database Setup

### 1. تثبيت PostgreSQL
```bash
# Windows
# تحميل PostgreSQL من postgresql.org

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

### 2. إنشاء قاعدة البيانات
```sql
-- الاتصال بـ PostgreSQL
psql -U postgres

-- إنشاء قاعدة البيانات
CREATE DATABASE veo7_platform;
CREATE USER veo7_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE veo7_platform TO veo7_user;
```

### 3. إعداد متغيرات البيئة
```bash
# إنشاء ملف .env في مجلد backend
cp backend/.env.example backend/.env

# تحرير الملف وإضافة:
DATABASE_URL=postgresql://veo7_user:your_secure_password@localhost:5432/veo7_platform
SECRET_KEY=your_very_secure_secret_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4. تشغيل الهجرات
```bash
cd backend
python setup_database.py
```

---

## إعداد نماذج الذكاء الاصطناعي / AI Models Setup

### 1. تثبيت CUDA (للمعالجة بـ GPU)
```bash
# Windows
# تحميل CUDA Toolkit من developer.nvidia.com

# Ubuntu
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt install cuda
```

### 2. تحميل أوزان النماذج
```bash
# إنشاء مجلد النماذج
mkdir -p backend/models

# تحميل نماذج SadTalker
cd backend/models
wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00109-model.pth.tar
wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar

# تحميل نماذج Wav2Lip
wget https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp2pgHDvJA

# تحميل نماذج Real-ESRGAN
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
```

### 3. إعداد متغيرات البيئة للذكاء الاصطناعي
```bash
# إضافة إلى ملف .env
AI_MODELS_ENABLED=true
SADTALKER_MODEL_PATH=./models/sadtalker
WAV2LIP_MODEL_PATH=./models/wav2lip
REALESRGAN_MODEL_PATH=./models/realesrgan
DEVICE=cuda  # أو cpu للمعالجة بـ CPU
```

### 4. اختبار النماذج
```bash
python test_ai_features.py
```

---

## النشر المحلي / Local Deployment

### 1. تشغيل الخادم الخلفي
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. تشغيل الواجهة الأمامية
```bash
cd frontend
npm run dev
```

### 3. الوصول إلى التطبيق
- **الواجهة الأمامية**: http://localhost:3000
- **API التوثيق**: http://localhost:8000/docs
- **AI Studio**: http://localhost:3000/ai-studio

---

## النشر على الإنتاج / Production Deployment

### 1. إعداد Docker
```dockerfile
# Dockerfile للخادم الخلفي
FROM python:3.10-slim

WORKDIR /app
COPY backend/requirements*.txt ./
RUN pip install -r requirements.txt

COPY backend/ ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile للواجهة الأمامية
FROM node:18-alpine

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### 2. Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: 
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend/models:/app/models
      - ./backend/uploads:/app/uploads
    depends_on:
      - postgres

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=veo7_platform
      - POSTGRES_USER=veo7_user
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

### 3. تشغيل الإنتاج
```bash
# بناء وتشغيل الحاويات
docker-compose up -d --build

# مراقبة السجلات
docker-compose logs -f
```

---

## المراقبة والصيانة / Monitoring and Maintenance

### 1. مراقبة الأداء
```bash
# مراقبة استخدام الموارد
docker stats

# مراقبة السجلات
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 2. النسخ الاحتياطي
```bash
# نسخ احتياطي لقاعدة البيانات
docker exec -t postgres pg_dump -U veo7_user veo7_platform > backup_$(date +%Y%m%d_%H%M%S).sql

# نسخ احتياطي للملفات المرفوعة
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend/uploads/
```

### 3. التحديثات
```bash
# سحب أحدث التغييرات
git pull origin main

# إعادة بناء الحاويات
docker-compose down
docker-compose up -d --build
```

---

## استكشاف الأخطاء / Troubleshooting

### مشاكل شائعة / Common Issues

#### 1. خطأ في الاتصال بقاعدة البيانات
```bash
# التحقق من حالة PostgreSQL
sudo systemctl status postgresql

# إعادة تشغيل PostgreSQL
sudo systemctl restart postgresql
```

#### 2. مشاكل في نماذج الذكاء الاصطناعي
```bash
# التحقق من CUDA
nvidia-smi

# التحقق من PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

#### 3. مشاكل في الذاكرة
```bash
# مراقبة استخدام الذاكرة
free -h

# تنظيف ذاكرة التخزين المؤقت
sudo sync && sudo sysctl vm.drop_caches=3
```

#### 4. مشاكل في الشبكة
```bash
# التحقق من المنافذ
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000
```

### سجلات الأخطاء / Error Logs

#### مواقع السجلات
- **Backend**: `backend/logs/`
- **Frontend**: Browser Developer Console
- **Docker**: `docker-compose logs`
- **Nginx**: `/var/log/nginx/`

#### تحليل السجلات
```bash
# عرض آخر 100 سطر من السجلات
tail -n 100 backend/logs/app.log

# البحث عن أخطاء محددة
grep "ERROR" backend/logs/app.log

# مراقبة السجلات في الوقت الفعلي
tail -f backend/logs/app.log
```

---

## الأمان / Security

### 1. إعدادات الأمان الأساسية
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade

# إعداد جدار الحماية
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 2. شهادات SSL
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot --nginx -d yourdomain.com
```

### 3. النسخ الاحتياطي المجدول
```bash
# إضافة مهمة cron للنسخ الاحتياطي اليومي
crontab -e

# إضافة السطر التالي:
0 2 * * * /path/to/backup_script.sh
```

---

## الأداء / Performance

### 1. تحسين قاعدة البيانات
```sql
-- إنشاء فهارس للاستعلامات السريعة
CREATE INDEX idx_videos_user_id ON videos(user_id);
CREATE INDEX idx_videos_created_at ON videos(created_at);
```

### 2. تحسين الذكاء الاصطناعي
```python
# إعدادات تحسين الأداء في .env
AI_BATCH_SIZE=4
AI_MAX_WORKERS=2
AI_MEMORY_LIMIT=8GB
```

### 3. CDN وتخزين مؤقت
```nginx
# إعداد Nginx للتخزين المؤقت
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## الدعم / Support

### موارد المساعدة
- **التوثيق**: [docs.veo7.com](https://docs.veo7.com)
- **GitHub Issues**: [github.com/veo7/issues](https://github.com/veo7/issues)
- **Discord**: [discord.gg/veo7](https://discord.gg/veo7)
- **البريد الإلكتروني**: support@veo7.com

### المساهمة
نرحب بمساهماتكم! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) للمزيد من المعلومات.

---

## الترخيص / License

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للمزيد من التفاصيل.

---

**تم إنشاء هذا الدليل بواسطة فريق VEO7 💜**