# إعداد PayPal للإنتاج - VEO7 Video Platform

## الوضع الحالي
النظام يعمل حالياً في وضع المحاكاة (Mock Mode) لأغراض التطوير والاختبار.

## التبديل إلى PayPal الحقيقي

### 1. الحصول على بيانات اعتماد PayPal Live

1. قم بتسجيل الدخول إلى [PayPal Developer Dashboard](https://developer.paypal.com/)
2. أنشئ تطبيق جديد للإنتاج (Live)
3. احصل على:
   - Client ID
   - Client Secret
   - Merchant Email

### 2. تحديث ملف .env

في ملف `backend/.env`، قم بإلغاء التعليق عن البيانات الحقيقية وتعليق بيانات Sandbox:

```env
# PayPal Configuration - Sandbox for Testing (Comment out for production)
# PAYPAL_CLIENT_ID=AYsqtnDtSJ8mFYmTPN9D6BELWu5pLRl7RwNHphcs2xWVsoOaVdx8GqNp_siqVfaVXOEBHUot_MrG9WfA
# PAYPAL_CLIENT_SECRET=EGnHDxD_qRPdaLdHCKiZ0NaF2B6PlVK5TBHHmNJ6_NjgiQABzVKRjrQBxKqEEBNKJQBHUot_MrG9WfA
# PAYPAL_ENVIRONMENT=sandbox

# PayPal Live Production Settings (Uncomment for production)
PAYPAL_CLIENT_ID=YOUR_LIVE_CLIENT_ID_HERE
PAYPAL_CLIENT_SECRET=YOUR_LIVE_CLIENT_SECRET_HERE
PAYPAL_ENVIRONMENT=live
PAYPAL_MERCHANT_EMAIL=hmhhmhhmh55@gmail.com
PAYPAL_WEBHOOK_ID=YOUR_LIVE_WEBHOOK_ID_HERE
```

### 3. إعداد Webhooks

1. في PayPal Developer Dashboard، انتقل إلى تطبيقك
2. أضف webhook URL: `https://yourdomain.com/api/payments/webhook`
3. اختر الأحداث التالية:
   - `BILLING.SUBSCRIPTION.CREATED`
   - `BILLING.SUBSCRIPTION.ACTIVATED`
   - `BILLING.SUBSCRIPTION.CANCELLED`
   - `BILLING.SUBSCRIPTION.SUSPENDED`
   - `PAYMENT.SALE.COMPLETED`

### 4. اختبار النظام

بعد تحديث البيانات، قم بإعادة تشغيل الخادم واختبر:

```bash
# إنشاء خطط PayPal الحقيقية
POST /api/payments/plans/create

# عرض الخطط المتاحة
GET /api/payments/plans

# عرض تفاصيل خطة محددة
GET /api/payments/plans/{plan_id}
```

### 5. نقاط API المتاحة

#### إدارة الخطط
- `GET /api/payments/plans` - عرض جميع الخطط
- `GET /api/payments/plans/{plan_id}` - تفاصيل خطة محددة
- `POST /api/payments/plans/create` - إنشاء خطط PayPal

#### الاشتراكات
- `POST /api/payments/subscribe/{plan_id}` - إنشاء اشتراك جديد

#### إحصائيات
- `GET /api/payments/paypal-stats` - حالة خدمة PayPal

### 6. الخطط المتاحة

#### Basic Plan - $9.99/شهر
- 10 فيديوهات شهرياً
- تخزين 1GB
- دعم أساسي
- نماذج AI أساسية

#### Pro Plan - $29.99/شهر
- 100 فيديو شهرياً
- تخزين 10GB
- دعم أولوية
- جميع نماذج AI
- تحليلات متقدمة

#### Enterprise Plan - $99.99/شهر
- فيديوهات غير محدودة
- تخزين 100GB
- دعم مخصص 24/7
- أولوية قصوى
- نماذج AI مخصصة
- وصول API
- تقارير تحليلية

### 7. الأمان

- جميع المعاملات مشفرة
- التحقق من Webhook signatures
- حماية من CSRF
- تسجيل جميع المعاملات

### 8. المراقبة

- سجلات مفصلة لجميع معاملات PayPal
- تنبيهات عند فشل المعاملات
- إحصائيات الاشتراكات والإيرادات

### 9. استكشاف الأخطاء

#### خطأ "invalid_client"
- تأكد من صحة Client ID و Client Secret
- تأكد من أن التطبيق مُفعل للإنتاج

#### خطأ "PERMISSION_DENIED"
- تأكد من أن التطبيق له صلاحيات الاشتراكات
- تحقق من إعدادات التطبيق في PayPal Dashboard

#### مشاكل Webhook
- تأكد من أن URL صحيح ومتاح
- تحقق من SSL certificate
- راجع سجلات PayPal Dashboard

### 10. الدعم

للحصول على المساعدة:
1. راجع [PayPal Developer Documentation](https://developer.paypal.com/docs/)
2. تحقق من سجلات التطبيق
3. استخدم PayPal Sandbox للاختبار أولاً

---

**ملاحظة مهمة**: لا تشارك بيانات اعتماد PayPal الحقيقية في أي مكان عام أو في نظام التحكم في الإصدارات.