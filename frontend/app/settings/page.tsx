'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import Link from 'next/link';

export default function SettingsPage() {
  const { language, setLanguage } = useLanguage();
  const isRTL = language === 'ar';
  const supabase = createClientComponentClient();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      marketing: false
    },
    privacy: {
      profilePublic: true,
      showEmail: false,
      showLocation: true
    },
    preferences: {
      theme: 'system',
      language: language,
      autoSave: true
    }
  });

  useEffect(() => {
    getUser();
  }, []);

  async function getUser() {
    try {
      setLoading(true);
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    } catch (error) {
      console.error('Error loading user:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    setSettings(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        language: newLanguage
      }
    }));
  };

  const handleNotificationChange = (key: string, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [key]: value
      }
    }));
  };

  const handlePrivacyChange = (key: string, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      privacy: {
        ...prev.privacy,
        [key]: value
      }
    }));
  };

  const handlePreferenceChange = (key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: value
      }
    }));
  };

  const saveSettings = async () => {
    try {
      // Here you would save settings to your backend
      console.log('Saving settings:', settings);
      // For now, just show a success message
      alert(language === 'ar' ? 'تم حفظ الإعدادات بنجاح' : 'Settings saved successfully');
    } catch (error) {
      console.error('Error saving settings:', error);
      alert(language === 'ar' ? 'خطأ في حفظ الإعدادات' : 'Error saving settings');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'يرجى تسجيل الدخول' : 'Please Login'}
          </h2>
          <Link href="/auth/login" className="btn-primary">
            {language === 'ar' ? 'تسجيل الدخول' : 'Login'}
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${isRTL ? 'rtl' : 'ltr'} bg-gray-50 dark:bg-gray-900`}>
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              {language === 'ar' ? 'الإعدادات' : 'Settings'}
            </h1>
            <Link
              href="/dashboard"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
            >
              {language === 'ar' ? 'العودة للوحة التحكم' : 'Back to Dashboard'}
            </Link>
          </div>
        </div>
      </div>

      {/* Settings Content */}
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="space-y-8">
          
          {/* Language & Preferences */}
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                {language === 'ar' ? 'التفضيلات العامة' : 'General Preferences'}
              </h2>
            </div>
            <div className="px-6 py-4 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {language === 'ar' ? 'اللغة' : 'Language'}
                </label>
                <select
                  value={settings.preferences.language}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option value="ar">العربية</option>
                  <option value="en">English</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {language === 'ar' ? 'المظهر' : 'Theme'}
                </label>
                <select
                  value={settings.preferences.theme}
                  onChange={(e) => handlePreferenceChange('theme', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option value="light">{language === 'ar' ? 'فاتح' : 'Light'}</option>
                  <option value="dark">{language === 'ar' ? 'داكن' : 'Dark'}</option>
                  <option value="system">{language === 'ar' ? 'تلقائي' : 'System'}</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'الحفظ التلقائي' : 'Auto Save'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'حفظ العمل تلقائياً أثناء التحرير' : 'Automatically save work while editing'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.preferences.autoSave}
                  onChange={(e) => handlePreferenceChange('autoSave', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                {language === 'ar' ? 'الإشعارات' : 'Notifications'}
              </h2>
            </div>
            <div className="px-6 py-4 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'إشعارات البريد الإلكتروني' : 'Email Notifications'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'تلقي إشعارات عبر البريد الإلكتروني' : 'Receive notifications via email'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.notifications.email}
                  onChange={(e) => handleNotificationChange('email', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'الإشعارات الفورية' : 'Push Notifications'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'تلقي إشعارات فورية في المتصفح' : 'Receive push notifications in browser'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.notifications.push}
                  onChange={(e) => handleNotificationChange('push', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'الإشعارات التسويقية' : 'Marketing Notifications'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'تلقي إشعارات حول العروض والميزات الجديدة' : 'Receive notifications about offers and new features'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.notifications.marketing}
                  onChange={(e) => handleNotificationChange('marketing', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>
            </div>
          </div>

          {/* Privacy */}
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                {language === 'ar' ? 'الخصوصية' : 'Privacy'}
              </h2>
            </div>
            <div className="px-6 py-4 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'الملف الشخصي العام' : 'Public Profile'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'جعل ملفك الشخصي مرئياً للآخرين' : 'Make your profile visible to others'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.privacy.profilePublic}
                  onChange={(e) => handlePrivacyChange('profilePublic', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'إظهار البريد الإلكتروني' : 'Show Email'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'إظهار بريدك الإلكتروني في الملف الشخصي' : 'Display your email in your profile'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.privacy.showEmail}
                  onChange={(e) => handlePrivacyChange('showEmail', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'إظهار الموقع' : 'Show Location'}
                  </label>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {language === 'ar' ? 'إظهار موقعك في الملف الشخصي' : 'Display your location in your profile'}
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.privacy.showLocation}
                  onChange={(e) => handlePrivacyChange('showLocation', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>
            </div>
          </div>

          {/* Account Actions */}
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                {language === 'ar' ? 'إجراءات الحساب' : 'Account Actions'}
              </h2>
            </div>
            <div className="px-6 py-4 space-y-4">
              <button
                onClick={() => supabase.auth.signOut()}
                className="w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                {language === 'ar' ? 'تسجيل الخروج' : 'Sign Out'}
              </button>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={saveSettings}
              className="btn-primary"
            >
              {language === 'ar' ? 'حفظ الإعدادات' : 'Save Settings'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}