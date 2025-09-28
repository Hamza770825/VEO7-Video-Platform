# استخدام Node.js 18 Alpine كصورة أساسية
FROM node:18-alpine AS base

# تثبيت المتطلبات الأساسية
RUN apk add --no-cache libc6-compat

# مرحلة تثبيت التبعيات
FROM base AS deps
WORKDIR /app

# نسخ ملفات package
COPY package.json package-lock.json* ./

# تثبيت التبعيات
RUN npm ci --only=production

# مرحلة البناء
FROM base AS builder
WORKDIR /app

# نسخ التبعيات من المرحلة السابقة
COPY --from=deps /app/node_modules ./node_modules

# نسخ الكود المصدري
COPY . .

# تعطيل telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# بناء التطبيق
RUN npm run build

# مرحلة الإنتاج
FROM base AS runner
WORKDIR /app

# تعيين متغيرات البيئة
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# إنشاء مستخدم غير root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# نسخ الملفات المطلوبة
COPY --from=builder /app/public ./public

# نسخ ملفات البناء
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# التبديل للمستخدم غير root
USER nextjs

# تعريض المنفذ
EXPOSE 3000

# تعيين متغيرات البيئة
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# فحص صحة التطبيق
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# تشغيل التطبيق
CMD ["node", "server.js"]