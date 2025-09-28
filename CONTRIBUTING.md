# 🤝 دليل المساهمة في VEO7

نرحب بمساهماتكم في تطوير منصة VEO7! هذا الدليل سيساعدكم على فهم كيفية المساهمة بفعالية في المشروع.

## 📋 جدول المحتويات

- [قواعد السلوك](#قواعد-السلوك)
- [كيفية المساهمة](#كيفية-المساهمة)
- [إعداد بيئة التطوير](#إعداد-بيئة-التطوير)
- [معايير الكود](#معايير-الكود)
- [عملية المراجعة](#عملية-المراجعة)
- [الإبلاغ عن الأخطاء](#الإبلاغ-عن-الأخطاء)
- [طلب الميزات](#طلب-الميزات)

## 🤝 قواعد السلوك

### التزامنا
نحن ملتزمون بتوفير بيئة ترحيبية وشاملة للجميع، بغض النظر عن:
- العمر أو الجنس أو الهوية الجنسية
- العرق أو الدين أو الجنسية
- مستوى الخبرة أو التعليم
- الإعاقة أو المظهر الشخصي

### السلوك المتوقع
- استخدام لغة ترحيبية وشاملة
- احترام وجهات النظر والتجارب المختلفة
- قبول النقد البناء بأدب
- التركيز على ما هو أفضل للمجتمع
- إظهار التعاطف مع أعضاء المجتمع الآخرين

### السلوك غير المقبول
- استخدام لغة أو صور جنسية
- التنمر أو التعليقات المهينة
- المضايقة العامة أو الخاصة
- نشر معلومات خاصة للآخرين دون إذن
- أي سلوك آخر يُعتبر غير مناسب مهنياً

## 🚀 كيفية المساهمة

### أنواع المساهمات المرحب بها

#### 🐛 إصلاح الأخطاء
- البحث عن الأخطاء وإصلاحها
- تحسين معالجة الأخطاء
- إصلاح مشاكل الأداء

#### ✨ الميزات الجديدة
- إضافة وظائف جديدة
- تحسين الواجهة
- دعم لغات جديدة

#### 📚 التوثيق
- تحسين README
- إضافة تعليقات للكود
- كتابة أدلة المستخدم

#### 🧪 الاختبارات
- كتابة اختبارات جديدة
- تحسين التغطية
- اختبارات الأداء

#### 🎨 التصميم
- تحسين UI/UX
- إضافة رسوم متحركة
- تحسين إمكانية الوصول

## 🛠️ إعداد بيئة التطوير

### المتطلبات الأساسية
```bash
# Node.js 18+
node --version

# Python 3.11+
python3 --version

# Git
git --version

# Docker (اختياري)
docker --version
```

### خطوات الإعداد

#### 1. استنساخ المشروع
```bash
git clone https://github.com/your-username/VEO7-Video-Platform.git
cd VEO7-Video-Platform
```

#### 2. إعداد البيئة
```bash
# تشغيل سكريبت الإعداد
chmod +x scripts/setup.sh
./scripts/setup.sh

# أو الإعداد اليدوي
npm run install:all
```

#### 3. تكوين متغيرات البيئة
```bash
# نسخ ملف البيئة
cp .env.example .env

# تحرير المتغيرات
nano .env
```

#### 4. تشغيل التطبيق
```bash
# تشغيل Frontend و Backend معاً
npm run dev

# أو تشغيل كل واحد منفصل
npm run dev:frontend
npm run dev:backend
```

## 📝 معايير الكود

### Frontend (Next.js/TypeScript)

#### هيكل الملفات
```
frontend/
├── app/                 # App Router
├── components/          # المكونات القابلة للإعادة
│   ├── ui/             # مكونات UI الأساسية
│   └── features/       # مكونات الميزات
├── utils/              # الأدوات المساعدة
├── types/              # تعريفات TypeScript
└── styles/             # ملفات التنسيق
```

#### قواعد التسمية
```typescript
// المكونات - PascalCase
const VideoPlayer = () => {}

// الدوال - camelCase
const handleVideoPlay = () => {}

// الثوابت - UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 100 * 1024 * 1024

// الواجهات - PascalCase مع I
interface IVideoProps {}

// الأنواع - PascalCase مع T
type TVideoStatus = 'pending' | 'processing' | 'completed'
```

#### أمثلة على الكود الجيد
```typescript
// ✅ جيد
interface VideoPlayerProps {
  src: string
  autoPlay?: boolean
  onPlay?: () => void
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ 
  src, 
  autoPlay = false, 
  onPlay 
}) => {
  const [isPlaying, setIsPlaying] = useState(false)
  
  const handlePlay = useCallback(() => {
    setIsPlaying(true)
    onPlay?.()
  }, [onPlay])
  
  return (
    <video 
      src={src} 
      autoPlay={autoPlay}
      onPlay={handlePlay}
      className="w-full h-auto rounded-lg"
    />
  )
}

// ❌ سيء
const videoplayer = (props: any) => {
  let playing = false
  return <video src={props.src} />
}
```

### Backend (FastAPI/Python)

#### هيكل الملفات
```
backend/
├── main.py              # نقطة الدخول
├── database.py          # تكوين قاعدة البيانات
├── models/              # نماذج البيانات
├── services/            # منطق العمل
├── routers/             # نقاط النهاية
└── utils/               # الأدوات المساعدة
```

#### قواعد التسمية
```python
# الفئات - PascalCase
class VideoService:
    pass

# الدوال والمتغيرات - snake_case
def process_video():
    pass

video_status = "processing"

# الثوابت - UPPER_SNAKE_CASE
MAX_VIDEO_DURATION = 300

# الملفات - snake_case
# video_service.py
# user_model.py
```

#### أمثلة على الكود الجيد
```python
# ✅ جيد
from typing import Optional
from pydantic import BaseModel

class VideoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    quality: str = "medium"
    
    class Config:
        schema_extra = {
            "example": {
                "title": "فيديو تجريبي",
                "description": "وصف الفيديو",
                "quality": "high"
            }
        }

async def create_video(
    request: VideoCreateRequest,
    user_id: str
) -> VideoResponse:
    """إنشاء فيديو جديد"""
    try:
        video = await video_service.create(
            title=request.title,
            description=request.description,
            quality=request.quality,
            user_id=user_id
        )
        return VideoResponse.from_orm(video)
    except Exception as e:
        logger.error(f"خطأ في إنشاء الفيديو: {e}")
        raise HTTPException(
            status_code=500,
            detail="فشل في إنشاء الفيديو"
        )

# ❌ سيء
def createvideo(data):
    video = Video()
    video.title = data["title"]
    return video
```

### قواعد عامة

#### التعليقات
```typescript
// ✅ جيد - تعليقات مفيدة
/**
 * يحسب مدة الفيديو بناءً على النص المدخل
 * @param text النص المراد تحويله لصوت
 * @param wordsPerMinute عدد الكلمات في الدقيقة
 * @returns مدة الفيديو بالثواني
 */
const calculateVideoDuration = (text: string, wordsPerMinute: number = 150): number => {
  const wordCount = text.split(' ').length
  return Math.ceil((wordCount / wordsPerMinute) * 60)
}

// ❌ سيء - تعليقات غير مفيدة
// هذه الدالة تحسب شيء ما
const calc = (t: string) => {
  // عد الكلمات
  const c = t.split(' ').length
  // اقسم على 150
  return c / 150
}
```

#### معالجة الأخطاء
```typescript
// ✅ جيد
try {
  const result = await apiCall()
  return result
} catch (error) {
  logger.error('فشل في استدعاء API:', error)
  throw new ApiError('فشل في العملية', error)
}

// ❌ سيء
try {
  const result = await apiCall()
  return result
} catch (error) {
  console.log(error)
  return null
}
```

## 🔄 عملية المراجعة

### قبل إرسال Pull Request

#### 1. التحقق من الكود
```bash
# تشغيل الاختبارات
npm test

# فحص الكود
npm run lint

# تنسيق الكود
npm run format
```

#### 2. التحقق من الوظائف
- تأكد من عمل جميع الميزات
- اختبر على متصفحات مختلفة
- تحقق من الاستجابة على الأجهزة المختلفة

#### 3. التوثيق
- حدث README إذا لزم الأمر
- أضف تعليقات للكود الجديد
- وثق أي تغييرات في API

### إرسال Pull Request

#### 1. إنشاء Branch
```bash
# إنشاء branch جديد
git checkout -b feature/amazing-feature

# أو لإصلاح خطأ
git checkout -b fix/bug-description
```

#### 2. Commit Messages
```bash
# ✅ جيد
git commit -m "feat: إضافة مشغل فيديو متقدم مع تحكم في السرعة"
git commit -m "fix: إصلاح مشكلة تحميل الملفات الكبيرة"
git commit -m "docs: تحديث دليل التثبيت"

# ❌ سيء
git commit -m "تحديث"
git commit -m "إصلاح"
git commit -m "WIP"
```

#### 3. قالب Pull Request
```markdown
## 📝 الوصف
وصف مختصر للتغييرات المقترحة

## 🎯 نوع التغيير
- [ ] إصلاح خطأ
- [ ] ميزة جديدة
- [ ] تحسين الأداء
- [ ] تحديث التوثيق

## 🧪 الاختبار
- [ ] تم اختبار الكود محلياً
- [ ] تم إضافة اختبارات جديدة
- [ ] جميع الاختبارات تمر بنجاح

## 📸 لقطات الشاشة
(إذا كانت التغييرات تؤثر على الواجهة)

## ✅ قائمة المراجعة
- [ ] الكود يتبع معايير المشروع
- [ ] التعليقات واضحة ومفيدة
- [ ] التوثيق محدث
- [ ] لا توجد تحذيرات في وحدة التحكم
```

### مراجعة الكود

#### ما نبحث عنه
- **الوظائف**: هل الكود يعمل كما هو متوقع؟
- **الأداء**: هل هناك تحسينات ممكنة؟
- **الأمان**: هل هناك ثغرات أمنية؟
- **القابلية للقراءة**: هل الكود واضح ومفهوم؟
- **الاختبارات**: هل التغييرات مغطاة بالاختبارات؟

#### عملية المراجعة
1. **المراجعة الأولية** - فحص سريع للتأكد من اتباع المعايير
2. **المراجعة التفصيلية** - فحص منطق الكود والأداء
3. **الاختبار** - تجربة التغييرات محلياً
4. **الموافقة** - الموافقة على الدمج أو طلب تعديلات

## 🐛 الإبلاغ عن الأخطاء

### قبل الإبلاغ
- ابحث في Issues الموجودة
- تأكد من أن المشكلة قابلة للتكرار
- جرب على متصفحات مختلفة

### قالب الإبلاغ
```markdown
## 🐛 وصف الخطأ
وصف واضح ومختصر للخطأ

## 🔄 خطوات التكرار
1. اذهب إلى '...'
2. اضغط على '...'
3. مرر إلى '...'
4. شاهد الخطأ

## ✅ السلوك المتوقع
وصف ما كان يجب أن يحدث

## 📸 لقطات الشاشة
إذا أمكن، أضف لقطات شاشة للمساعدة في شرح المشكلة

## 🖥️ معلومات البيئة
- نظام التشغيل: [مثل iOS]
- المتصفح: [مثل Chrome, Safari]
- الإصدار: [مثل 22]

## 📝 معلومات إضافية
أي معلومات أخرى حول المشكلة
```

## ✨ طلب الميزات

### قالب طلب الميزة
```markdown
## 🚀 وصف الميزة
وصف واضح ومختصر للميزة المطلوبة

## 🎯 المشكلة المحلولة
ما هي المشكلة التي تحلها هذه الميزة؟

## 💡 الحل المقترح
وصف الحل الذي تريده

## 🔄 البدائل المدروسة
وصف أي حلول أو ميزات بديلة فكرت فيها

## 📝 معلومات إضافية
أي معلومات أخرى حول طلب الميزة
```

## 🏷️ التسميات (Labels)

### أنواع التسميات

#### الأولوية
- `priority: high` - أولوية عالية
- `priority: medium` - أولوية متوسطة  
- `priority: low` - أولوية منخفضة

#### النوع
- `type: bug` - خطأ
- `type: feature` - ميزة جديدة
- `type: enhancement` - تحسين
- `type: documentation` - توثيق

#### المجال
- `area: frontend` - Frontend
- `area: backend` - Backend
- `area: database` - قاعدة البيانات
- `area: ui/ux` - واجهة المستخدم

#### الحالة
- `status: needs-review` - يحتاج مراجعة
- `status: in-progress` - قيد التطوير
- `status: blocked` - محجوب

## 🎉 الاعتراف بالمساهمين

نحن نقدر جميع المساهمات ونعترف بها:

### Hall of Fame
- **المساهمون الأساسيون** - يظهرون في README
- **المساهمون النشطون** - يحصلون على شارات خاصة
- **المساهمون الجدد** - نرحب بهم في المجتمع

### طرق الاعتراف
- ذكر في Release Notes
- إضافة إلى قائمة المساهمين
- شارات GitHub خاصة
- دعوة لأحداث المجتمع

## 📞 التواصل

### قنوات التواصل
- **GitHub Issues** - للأخطاء وطلبات الميزات
- **GitHub Discussions** - للنقاشات العامة
- **Discord** - للدردشة المباشرة
- **Email** - للاستفسارات الخاصة

### أوقات الاستجابة
- **Issues** - خلال 48 ساعة
- **Pull Requests** - خلال 72 ساعة
- **Discord** - فوري (حسب التوفر)

---

## 🙏 شكراً لكم

شكراً لاهتمامكم بالمساهمة في VEO7! مساهماتكم تجعل هذا المشروع أفضل للجميع.

**معاً نبني مستقبل إنشاء الفيديوهات بالذكاء الاصطناعي! 🚀**