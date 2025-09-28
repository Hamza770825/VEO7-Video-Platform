# دليل إضافة نماذج الذكاء الاصطناعي الجديدة
# AI Models Integration Guide

## 📋 نظرة عامة / Overview

هذا الدليل يوضح كيفية إضافة نماذج ذكاء اصطناعي جديدة إلى منصة VEO7. يتضمن الدليل الخطوات التقنية والمعمارية المطلوبة لدمج النماذج بشكل صحيح.

This guide explains how to add new AI models to the VEO7 platform, including technical and architectural steps for proper integration.

---

## 🏗️ البنية المعمارية / Architecture

### هيكل المجلدات / Folder Structure
```
backend/
├── ai_models/
│   ├── __init__.py
│   ├── base_model.py          # الفئة الأساسية للنماذج
│   ├── sadtalker_model.py     # نموذج SadTalker
│   ├── wav2lip_model.py       # نموذج Wav2Lip
│   ├── realesrgan_model.py    # نموذج Real-ESRGAN
│   └── your_new_model.py      # النموذج الجديد
├── models/                    # أوزان النماذج
│   ├── sadtalker/
│   ├── wav2lip/
│   ├── realesrgan/
│   └── your_model/
└── services/
    └── ai_service.py          # خدمة إدارة النماذج
```

---

## 🔧 إضافة نموذج جديد / Adding a New Model

### 1. إنشاء فئة النموذج / Create Model Class

```python
# backend/ai_models/your_new_model.py

import torch
import numpy as np
from typing import Dict, Any, Optional
from .base_model import BaseAIModel

class YourNewModel(BaseAIModel):
    """
    نموذج جديد للذكاء الاصطناعي
    New AI model implementation
    """
    
    def __init__(self, model_path: str, device: str = "cuda"):
        super().__init__(model_path, device)
        self.model_name = "your_new_model"
        self.model_version = "1.0.0"
        
    def load_model(self) -> bool:
        """
        تحميل النموذج وأوزانه
        Load the model and its weights
        """
        try:
            # تحميل النموذج هنا
            # Load your model here
            self.model = torch.load(
                self.model_path, 
                map_location=self.device
            )
            self.model.eval()
            self.is_loaded = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def preprocess_input(self, input_data: Dict[str, Any]) -> Any:
        """
        معالجة البيانات المدخلة
        Preprocess input data
        """
        # معالجة البيانات حسب متطلبات النموذج
        # Process data according to model requirements
        processed_data = input_data
        return processed_data
    
    def inference(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تشغيل النموذج والحصول على النتائج
        Run model inference
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            # معالجة البيانات المدخلة
            processed_input = self.preprocess_input(input_data)
            
            # تشغيل النموذج
            with torch.no_grad():
                output = self.model(processed_input)
            
            # معالجة النتائج
            result = self.postprocess_output(output)
            
            return {
                "success": True,
                "result": result,
                "model_info": {
                    "name": self.model_name,
                    "version": self.model_version
                }
            }
            
        except Exception as e:
            self.logger.error(f"Inference failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def postprocess_output(self, output: Any) -> Any:
        """
        معالجة نتائج النموذج
        Postprocess model output
        """
        # معالجة النتائج حسب الحاجة
        # Process output as needed
        return output
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        معلومات النموذج
        Get model information
        """
        return {
            "name": self.model_name,
            "version": self.model_version,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "memory_usage": self.get_memory_usage(),
            "supported_formats": ["jpg", "png", "mp4"],  # حسب النموذج
            "description": "وصف النموذج الجديد"
        }
```

### 2. تحديث خدمة الذكاء الاصطناعي / Update AI Service

```python
# backend/services/ai_service.py

from ai_models.your_new_model import YourNewModel

class AIService:
    def __init__(self):
        # ... الكود الموجود
        self.your_new_model = None
    
    def initialize_your_new_model(self) -> bool:
        """تهيئة النموذج الجديد"""
        try:
            model_path = os.getenv("YOUR_MODEL_PATH", "./models/your_model")
            device = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
            
            self.your_new_model = YourNewModel(model_path, device)
            success = self.your_new_model.load_model()
            
            if success:
                logger.info("Your new model initialized successfully")
            else:
                logger.error("Failed to initialize your new model")
            
            return success
        except Exception as e:
            logger.error(f"Error initializing your new model: {e}")
            return False
    
    def process_with_your_model(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة البيانات باستخدام النموذج الجديد"""
        if not self.your_new_model or not self.your_new_model.is_loaded:
            return {
                "success": False,
                "error": "Your new model not available"
            }
        
        return self.your_new_model.inference(input_data)
```

### 3. إضافة API Endpoints / Add API Endpoints

```python
# backend/main.py

@app.post("/api/ai-models/your-new-model")
async def process_with_your_model(
    request: YourModelRequest,
    current_user: User = Depends(get_current_user)
):
    """
    معالجة البيانات باستخدام النموذج الجديد
    Process data with your new model
    """
    try:
        # التحقق من صحة البيانات
        input_data = {
            "param1": request.param1,
            "param2": request.param2,
            # ... باقي المعاملات
        }
        
        # معالجة البيانات
        result = ai_service.process_with_your_model(input_data)
        
        if result["success"]:
            return {
                "success": True,
                "result": result["result"],
                "processing_time": result.get("processing_time", 0)
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error in your new model endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# نموذج البيانات المطلوبة
class YourModelRequest(BaseModel):
    param1: str
    param2: Optional[int] = None
    settings: Optional[Dict[str, Any]] = {}
```

### 4. إضافة واجهة المستخدم / Add Frontend Interface

```typescript
// frontend/components/ai-studio/YourNewModelPanel.tsx

import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';

interface YourModelPanelProps {
  onProcessingStart: () => void;
  onProcessingComplete: (result: any) => void;
  onError: (error: string) => void;
}

export const YourNewModelPanel: React.FC<YourModelPanelProps> = ({
  onProcessingStart,
  onProcessingComplete,
  onError
}) => {
  const { user } = useAuth();
  const { language, t } = useLanguage();
  const [isProcessing, setIsProcessing] = useState(false);
  const [settings, setSettings] = useState({
    param1: '',
    param2: 1,
  });

  const handleProcess = async () => {
    if (!user) {
      onError(t('auth.loginRequired'));
      return;
    }

    setIsProcessing(true);
    onProcessingStart();

    try {
      const response = await fetch('/api/ai-models/your-new-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify(settings)
      });

      const result = await response.json();

      if (result.success) {
        onProcessingComplete(result.result);
      } else {
        onError(result.error || t('errors.processingFailed'));
      }
    } catch (error) {
      onError(t('errors.networkError'));
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
      <h3 className="text-xl font-bold mb-4">
        {t('aiStudio.yourNewModel.title')}
      </h3>
      
      {/* واجهة إعدادات النموذج */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('aiStudio.yourNewModel.param1')}
          </label>
          <input
            type="text"
            value={settings.param1}
            onChange={(e) => setSettings({...settings, param1: e.target.value})}
            className="w-full p-3 border rounded-lg"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('aiStudio.yourNewModel.param2')}
          </label>
          <input
            type="number"
            value={settings.param2}
            onChange={(e) => setSettings({...settings, param2: parseInt(e.target.value)})}
            className="w-full p-3 border rounded-lg"
          />
        </div>
        
        <button
          onClick={handleProcess}
          disabled={isProcessing}
          className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50"
        >
          {isProcessing ? t('common.processing') : t('aiStudio.yourNewModel.process')}
        </button>
      </div>
    </div>
  );
};
```

### 5. إضافة الترجمات / Add Translations

```json
// frontend/locales/ar.json
{
  "aiStudio": {
    "yourNewModel": {
      "title": "النموذج الجديد",
      "param1": "المعامل الأول",
      "param2": "المعامل الثاني",
      "process": "معالجة",
      "description": "وصف النموذج الجديد"
    }
  }
}

// frontend/locales/en.json
{
  "aiStudio": {
    "yourNewModel": {
      "title": "Your New Model",
      "param1": "Parameter 1",
      "param2": "Parameter 2",
      "process": "Process",
      "description": "Description of your new model"
    }
  }
}
```

---

## 🧪 الاختبار / Testing

### 1. اختبار النموذج / Model Testing

```python
# tests/test_your_new_model.py

import pytest
from ai_models.your_new_model import YourNewModel

class TestYourNewModel:
    def setup_method(self):
        self.model = YourNewModel("./models/your_model", "cpu")
    
    def test_model_loading(self):
        """اختبار تحميل النموذج"""
        success = self.model.load_model()
        assert success == True
        assert self.model.is_loaded == True
    
    def test_inference(self):
        """اختبار تشغيل النموذج"""
        self.model.load_model()
        
        input_data = {
            "param1": "test_value",
            "param2": 1
        }
        
        result = self.model.inference(input_data)
        assert result["success"] == True
        assert "result" in result
    
    def test_model_info(self):
        """اختبار معلومات النموذج"""
        info = self.model.get_model_info()
        assert "name" in info
        assert "version" in info
        assert info["name"] == "your_new_model"
```

### 2. اختبار API / API Testing

```python
# tests/test_api_your_model.py

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_your_model_endpoint():
    """اختبار endpoint النموذج الجديد"""
    response = client.post(
        "/api/ai-models/your-new-model",
        json={
            "param1": "test",
            "param2": 1
        },
        headers={"Authorization": "Bearer test_token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

---

## 📦 التبعيات / Dependencies

### إضافة التبعيات المطلوبة / Add Required Dependencies

```txt
# backend/requirements_your_model.txt
your-model-library==1.0.0
additional-dependency==2.0.0
```

```bash
# تثبيت التبعيات
pip install -r backend/requirements_your_model.txt
```

---

## 🔧 الإعدادات / Configuration

### متغيرات البيئة / Environment Variables

```bash
# .env
YOUR_MODEL_PATH=./models/your_model
YOUR_MODEL_ENABLED=true
YOUR_MODEL_BATCH_SIZE=4
YOUR_MODEL_MAX_MEMORY=8GB
```

### إعدادات النموذج / Model Configuration

```python
# backend/config/your_model_config.py

YOUR_MODEL_CONFIG = {
    "model_path": "./models/your_model",
    "device": "cuda",
    "batch_size": 4,
    "max_memory": "8GB",
    "preprocessing": {
        "resize": (512, 512),
        "normalize": True
    },
    "postprocessing": {
        "format": "mp4",
        "quality": "high"
    }
}
```

---

## 📚 أفضل الممارسات / Best Practices

### 1. إدارة الذاكرة / Memory Management
```python
def cleanup_memory(self):
    """تنظيف الذاكرة بعد المعالجة"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # تنظيف المتغيرات المؤقتة
    del self.temp_variables
```

### 2. معالجة الأخطاء / Error Handling
```python
try:
    result = self.model.inference(input_data)
except torch.cuda.OutOfMemoryError:
    self.logger.error("GPU memory exhausted")
    # تبديل إلى CPU
    self.device = "cpu"
    self.model.to(self.device)
except Exception as e:
    self.logger.error(f"Unexpected error: {e}")
    raise
```

### 3. التحقق من صحة البيانات / Input Validation
```python
def validate_input(self, input_data: Dict[str, Any]) -> bool:
    """التحقق من صحة البيانات المدخلة"""
    required_fields = ["param1", "param2"]
    
    for field in required_fields:
        if field not in input_data:
            raise ValueError(f"Missing required field: {field}")
    
    return True
```

### 4. المراقبة والسجلات / Monitoring and Logging
```python
import time
from functools import wraps

def monitor_performance(func):
    """مراقبة أداء النموذج"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        processing_time = end_time - start_time
        logger.info(f"Model processing time: {processing_time:.2f}s")
        
        return result
    return wrapper
```

---

## 🚀 النشر / Deployment

### 1. إعداد Docker / Docker Setup
```dockerfile
# إضافة إلى Dockerfile
COPY models/your_model /app/models/your_model
RUN pip install -r requirements_your_model.txt
```

### 2. اختبار الإنتاج / Production Testing
```bash
# اختبار النموذج في بيئة الإنتاج
python -m pytest tests/test_your_new_model.py -v
```

---

## 📞 الدعم / Support

للحصول على المساعدة في إضافة نماذج جديدة:
- **التوثيق**: راجع الأمثلة الموجودة في `ai_models/`
- **GitHub Issues**: أنشئ issue جديد مع تفاصيل النموذج
- **Discord**: انضم إلى قناة المطورين

For help with adding new models:
- **Documentation**: Check existing examples in `ai_models/`
- **GitHub Issues**: Create a new issue with model details
- **Discord**: Join the developers channel

---

**تم إنشاء هذا الدليل بواسطة فريق VEO7 💜**