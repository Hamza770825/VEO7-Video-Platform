# دليل إعداد نماذج الذكاء الاصطناعي - VEO7 Video Platform

## نظرة عامة
يدعم VEO7 نماذج ذكاء اصطناعي متقدمة لتوليد الفيديو وتحسين جودة المحتوى:

### النماذج المدعومة:
1. **SadTalker** - توليد فيديو من صورة وملف صوتي
2. **Wav2Lip** - مزامنة حركة الشفاه مع الصوت
3. **Real-ESRGAN** - تحسين جودة الصور والفيديو

## متطلبات النظام

### الحد الأدنى:
- Python 3.8+
- CUDA 11.0+ (للمعالجة بـ GPU)
- RAM: 8GB
- VRAM: 4GB (للنماذج الأساسية)

### الموصى به:
- Python 3.9+
- CUDA 11.8+
- RAM: 16GB+
- VRAM: 8GB+
- SSD للتخزين السريع

## التثبيت

### 1. تثبيت المتطلبات الأساسية
```bash
cd backend
pip install -r requirements_ai_models.txt
```

### 2. تثبيت PyTorch مع دعم CUDA
```bash
# للـ CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# للـ CPU فقط (أبطأ)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 3. تحميل أوزان النماذج

#### SadTalker:
```bash
# إنشاء مجلد النماذج
mkdir -p models/sadtalker/checkpoints

# تحميل الأوزان (سيتم تحميلها تلقائياً عند أول استخدام)
# أو يمكن تحميلها يدوياً من:
# https://github.com/OpenTalker/SadTalker
```

#### Wav2Lip:
```bash
# إنشاء مجلد النماذج
mkdir -p models/wav2lip

# تحميل نموذج Wav2Lip
# سيتم تحميله تلقائياً عند أول استخدام
```

## الإعداد

### 1. متغيرات البيئة
أضف إلى ملف `.env`:

```env
# AI Models Configuration
AI_MODELS_ENABLED=true
AI_MODELS_DEVICE=cuda  # أو cpu
AI_MODELS_CACHE_DIR=./models
AI_MODELS_MAX_MEMORY=8GB

# SadTalker Settings
SADTALKER_ENABLED=true
SADTALKER_QUALITY=high  # low, medium, high
SADTALKER_FPS=25

# Wav2Lip Settings
WAV2LIP_ENABLED=true
WAV2LIP_QUALITY=high
WAV2LIP_BATCH_SIZE=16

# Real-ESRGAN Settings
REALESRGAN_ENABLED=true
REALESRGAN_SCALE=2  # 2x, 4x upscaling
```

### 2. اختبار التثبيت
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

## الاستخدام

### 1. SadTalker - توليد فيديو من صورة وصوت
```python
from services.ai_models_service import AIModelsService

ai_service = AIModelsService()

# توليد فيديو
result = await ai_service.generate_sadtalker_video(
    image_path="path/to/image.jpg",
    audio_path="path/to/audio.wav",
    output_path="path/to/output.mp4"
)
```

### 2. Wav2Lip - مزامنة الشفاه
```python
# مزامنة حركة الشفاه
result = await ai_service.generate_wav2lip_video(
    video_path="path/to/video.mp4",
    audio_path="path/to/audio.wav",
    output_path="path/to/synced.mp4"
)
```

### 3. Real-ESRGAN - تحسين الجودة
```python
# تحسين جودة الصورة
result = await ai_service.enhance_image(
    image_path="path/to/image.jpg",
    output_path="path/to/enhanced.jpg",
    scale=2
)
```

## استكشاف الأخطاء

### مشاكل شائعة:

#### 1. خطأ CUDA Out of Memory
```bash
# تقليل batch_size في الإعدادات
WAV2LIP_BATCH_SIZE=8
SADTALKER_QUALITY=medium
```

#### 2. بطء في المعالجة
```bash
# التأكد من استخدام GPU
AI_MODELS_DEVICE=cuda

# تحسين إعدادات الذاكرة
AI_MODELS_MAX_MEMORY=6GB
```

#### 3. خطأ في تحميل النماذج
```bash
# حذف الكاش وإعادة التحميل
rm -rf models/cache
python -c "from services.ai_models_service import AIModelsService; AIModelsService().download_models()"
```

## الأداء والتحسين

### نصائح للأداء الأمثل:

1. **استخدم GPU**: تأكد من تثبيت CUDA وتفعيله
2. **إدارة الذاكرة**: راقب استخدام VRAM
3. **معالجة متوازية**: استخدم batch processing للملفات المتعددة
4. **تخزين مؤقت**: احتفظ بالنماذج في الذاكرة بين الطلبات

### مراقبة الأداء:
```python
# مراقبة استخدام GPU
nvidia-smi

# مراقبة استخدام الذاكرة
htop
```

## الأمان

### احتياطات مهمة:
1. **تحقق من المدخلات**: تأكد من صحة ملفات الصور والصوت
2. **حدود الحجم**: ضع حدود لحجم الملفات المرفوعة
3. **مهلة زمنية**: ضع timeout للعمليات الطويلة
4. **تنظيف الملفات**: احذف الملفات المؤقتة بانتظام

## الدعم

للحصول على المساعدة:
1. راجع سجلات الأخطاء في `logs/ai_models.log`
2. تحقق من إعدادات النظام والذاكرة
3. راجع وثائق النماذج الرسمية

## المراجع

- [SadTalker GitHub](https://github.com/OpenTalker/SadTalker)
- [Wav2Lip GitHub](https://github.com/Rudrabha/Wav2Lip)
- [Real-ESRGAN GitHub](https://github.com/xinntao/Real-ESRGAN)
- [PyTorch Documentation](https://pytorch.org/docs/)