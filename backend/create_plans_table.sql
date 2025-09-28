-- Create plans table
CREATE TABLE IF NOT EXISTS plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    duration_days INTEGER NOT NULL DEFAULT 30,
    features JSONB DEFAULT '[]'::jsonb,
    max_projects INTEGER DEFAULT 10,
    max_videos_per_month INTEGER DEFAULT 50,
    max_storage_gb INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default plans
INSERT INTO plans (name, description, price, duration_days, features, max_projects, max_videos_per_month, max_storage_gb, is_active) VALUES
('Free', 'خطة مجانية للمبتدئين', 0.00, 30, '["إنشاء 5 فيديوهات شهرياً", "جودة HD", "دعم أساسي"]'::jsonb, 3, 5, 1, true),
('Basic', 'خطة أساسية للاستخدام الشخصي', 9.99, 30, '["إنشاء 25 فيديو شهرياً", "جودة Full HD", "دعم عبر البريد الإلكتروني", "إزالة العلامة المائية"]'::jsonb, 10, 25, 5, true),
('Pro', 'خطة احترافية للمبدعين', 29.99, 30, '["إنشاء 100 فيديو شهرياً", "جودة 4K", "دعم أولوية", "تحليلات متقدمة", "تصدير بصيغ متعددة"]'::jsonb, 50, 100, 20, true),
('Enterprise', 'خطة للشركات والمؤسسات', 99.99, 30, '["فيديوهات غير محدودة", "جودة 4K+", "دعم مخصص 24/7", "API مخصص", "تكامل مع الأنظمة", "تدريب فريق العمل"]'::jsonb, -1, -1, 100, true);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_plans_active ON plans(is_active);
CREATE INDEX IF NOT EXISTS idx_plans_price ON plans(price);