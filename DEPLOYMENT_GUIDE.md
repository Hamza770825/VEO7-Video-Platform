# 🚀 دليل النشر - VEO7 مع التحسينات الاحترافية

## 📋 متطلبات النشر

### البيئة المطلوبة
- **Node.js**: 18.0.0 أو أحدث
- **Python**: 3.9 أو أحدث
- **Docker**: 20.10 أو أحدث
- **RAM**: 4GB كحد أدنى (8GB موصى به)
- **Storage**: 10GB مساحة فارغة

### متطلبات الأداء للتحسينات الجديدة
- **GPU**: دعم WebGL 2.0 (للتأثيرات المتقدمة)
- **CPU**: معالج متعدد النوى (للرسوم المتحركة السلسة)
- **Network**: اتصال مستقر (للتحميل التدريجي)

## 🔧 إعداد بيئة الإنتاج

### 1. تحسين Frontend

```bash
# تثبيت التبعيات
cd frontend
npm ci --production

# بناء الإنتاج مع التحسينات
npm run build

# تحليل حجم الحزمة
npm run analyze
```

### 2. تكوين Next.js للإنتاج

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // تحسينات الأداء
  experimental: {
    optimizeCss: true,
    optimizeImages: true,
    optimizePackageImports: ['framer-motion', 'react-icons'],
  },
  
  // ضغط الملفات
  compress: true,
  
  // تحسين الصور
  images: {
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60,
    dangerouslyAllowSVG: true,
  },
  
  // تحسين الخطوط
  optimizeFonts: true,
  
  // إزالة console.log في الإنتاج
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  // تحسين CSS
  swcMinify: true,
  
  // Headers للأمان والأداء
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

### 3. تحسين Backend

```python
# requirements-prod.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-decouple==3.8
supabase==2.0.2
redis==5.0.1
celery==5.3.4
```

## 🐳 نشر Docker

### 1. Dockerfile للـ Frontend

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine AS base

# تثبيت التبعيات
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# بناء التطبيق
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# إنتاج
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### 2. Docker Compose للإنتاج

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    restart: unless-stopped
    networks:
      - veo7-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
    networks:
      - veo7-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
    networks:
      - veo7-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - veo7-network

networks:
  veo7-network:
    driver: bridge
```

## 🌐 إعداد Nginx

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    # ضغط الملفات
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # تحسين الأداء
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    
    server {
        listen 80;
        server_name your-domain.com;
        
        # إعادة توجيه إلى HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name your-domain.com;
        
        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        
        # Headers للأمان
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
        
        # Backend API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # تحسين ملفات الوسائط
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## ☁️ نشر على الخدمات السحابية

### 1. Vercel (Frontend)

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase-url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase-anon-key"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

### 2. Railway (Backend)

```dockerfile
# railway.dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. AWS ECS

```yaml
# ecs-task-definition.json
{
  "family": "veo7-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "veo7-frontend",
      "image": "your-registry/veo7-frontend:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/veo7",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

## 📊 مراقبة الأداء

### 1. إعداد مراقبة Core Web Vitals

```javascript
// lib/analytics.js
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  // إرسال إلى خدمة التحليلات
  console.log(metric);
}

export function initWebVitals() {
  getCLS(sendToAnalytics);
  getFID(sendToAnalytics);
  getFCP(sendToAnalytics);
  getLCP(sendToAnalytics);
  getTTFB(sendToAnalytics);
}
```

### 2. مراقبة الأخطاء

```javascript
// lib/error-tracking.js
export function setupErrorTracking() {
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // إرسال إلى خدمة تتبع الأخطاء
  });
  
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // إرسال إلى خدمة تتبع الأخطاء
  });
}
```

## 🔒 الأمان في الإنتاج

### 1. متغيرات البيئة

```bash
# .env.production
NODE_ENV=production
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
REDIS_URL=your-redis-url
```

### 2. إعدادات الأمان

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const response = NextResponse.next();
  
  // Headers الأمان
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'origin-when-cross-origin');
  
  return response;
}
```

## 📈 تحسين الأداء

### 1. تحميل تدريجي للتأثيرات

```javascript
// lib/lazy-effects.js
export const loadEffects = async () => {
  const { default: effects } = await import('./heavy-effects');
  return effects;
};
```

### 2. تحسين الصور

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['your-domain.com'],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60,
  },
};
```

## 🚀 سكريبت النشر التلقائي

```bash
#!/bin/bash
# deploy.sh

echo "🚀 بدء عملية النشر..."

# تحديث الكود
git pull origin main

# بناء Frontend
echo "📦 بناء Frontend..."
cd frontend
npm ci
npm run build
cd ..

# بناء Backend
echo "🐍 إعداد Backend..."
cd backend
pip install -r requirements.txt
cd ..

# بناء Docker images
echo "🐳 بناء Docker images..."
docker-compose -f docker-compose.prod.yml build

# إيقاف الخدمات القديمة
echo "⏹️ إيقاف الخدمات القديمة..."
docker-compose -f docker-compose.prod.yml down

# تشغيل الخدمات الجديدة
echo "▶️ تشغيل الخدمات الجديدة..."
docker-compose -f docker-compose.prod.yml up -d

# فحص الصحة
echo "🔍 فحص صحة الخدمات..."
sleep 30
curl -f http://localhost:3000 || exit 1
curl -f http://localhost:8000/health || exit 1

echo "✅ تم النشر بنجاح!"
```

## 📋 قائمة فحص ما قبل النشر

- [ ] اختبار جميع التأثيرات البصرية
- [ ] فحص الأداء على أجهزة مختلفة
- [ ] اختبار التوافق مع المتصفحات
- [ ] فحص الأمان والثغرات
- [ ] اختبار التحميل والاستجابة
- [ ] تحديث الوثائق
- [ ] إعداد النسخ الاحتياطية
- [ ] تكوين المراقبة والتنبيهات

---

**ملاحظة**: تأكد من اختبار جميع التحسينات في بيئة مشابهة للإنتاج قبل النشر النهائي.