import React from 'react';

export default function BlogPage() {
  const blogPosts = [
    {
      id: 1,
      title: "مستقبل إنتاج المحتوى بالذكاء الاصطناعي",
      excerpt: "كيف تغير تقنيات الذكاء الاصطناعي طريقة إنتاج المحتوى المرئي والصوتي",
      author: "فريق VEO7",
      date: "15 يناير 2024",
      readTime: "5 دقائق",
      image: "/api/placeholder/400/250",
      category: "تقنية"
    },
    {
      id: 2,
      title: "دليل شامل لإنشاء فيديوهات تعليمية فعالة",
      excerpt: "نصائح وإرشادات لإنتاج محتوى تعليمي جذاب ومؤثر باستخدام منصة VEO7",
      author: "سارة أحمد",
      date: "12 يناير 2024",
      readTime: "8 دقائق",
      image: "/api/placeholder/400/250",
      category: "تعليم"
    },
    {
      id: 3,
      title: "أفضل الممارسات في التسويق بالفيديو",
      excerpt: "استراتيجيات مجربة لاستخدام الفيديوهات في حملاتك التسويقية",
      author: "محمد علي",
      date: "10 يناير 2024",
      readTime: "6 دقائق",
      image: "/api/placeholder/400/250",
      category: "تسويق"
    },
    {
      id: 4,
      title: "كيفية اختيار الصوت المناسب لفيديوهاتك",
      excerpt: "دليل شامل لاختيار نبرة الصوت والسرعة المناسبة لجمهورك المستهدف",
      author: "ليلى حسن",
      date: "8 يناير 2024",
      readTime: "4 دقائق",
      image: "/api/placeholder/400/250",
      category: "إنتاج"
    },
    {
      id: 5,
      title: "الترجمة الآلية: التحديات والحلول",
      excerpt: "نظرة عميقة على تقنيات الترجمة الآلية وكيفية تحسين دقتها",
      author: "أحمد محمود",
      date: "5 يناير 2024",
      readTime: "7 دقائق",
      image: "/api/placeholder/400/250",
      category: "تقنية"
    },
    {
      id: 6,
      title: "قصص نجاح: كيف غيرت VEO7 أعمال عملائنا",
      excerpt: "تعرف على تجارب حقيقية لعملاء استخدموا منصتنا لتطوير أعمالهم",
      author: "فريق VEO7",
      date: "3 يناير 2024",
      readTime: "10 دقائق",
      image: "/api/placeholder/400/250",
      category: "قصص نجاح"
    }
  ];

  const categories = ["الكل", "تقنية", "تعليم", "تسويق", "إنتاج", "قصص نجاح"];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            مدونة VEO7
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            اكتشف أحدث الاتجاهات والنصائح في عالم إنتاج المحتوى بالذكاء الاصطناعي
          </p>
        </div>

        {/* Categories Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map((category, index) => (
            <button
              key={index}
              className={`px-6 py-2 rounded-full transition duration-200 ${
                index === 0
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-blue-50 border border-gray-300'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Featured Post */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-12">
          <div className="md:flex">
            <div className="md:w-1/2">
              <div className="h-64 md:h-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                <svg className="w-24 h-24 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div className="md:w-1/2 p-8">
              <div className="flex items-center mb-4">
                <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">مميز</span>
                <span className="text-gray-500 text-sm ml-4">{blogPosts[0].category}</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">{blogPosts[0].title}</h2>
              <p className="text-gray-600 mb-6">{blogPosts[0].excerpt}</p>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
                  <div>
                    <div className="text-sm font-semibold text-gray-900">{blogPosts[0].author}</div>
                    <div className="text-xs text-gray-500">{blogPosts[0].date}</div>
                  </div>
                </div>
                <span className="text-sm text-gray-500">{blogPosts[0].readTime}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Blog Posts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {blogPosts.slice(1).map((post) => (
            <article key={post.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-200">
              <div className="h-48 bg-gradient-to-r from-purple-400 to-pink-400 flex items-center justify-center">
                <svg className="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                </svg>
              </div>
              <div className="p-6">
                <div className="flex items-center mb-3">
                  <span className="bg-gray-100 text-gray-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {post.category}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{post.title}</h3>
                <p className="text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-gray-300 rounded-full mr-2"></div>
                    <div>
                      <div className="text-sm font-semibold text-gray-900">{post.author}</div>
                      <div className="text-xs text-gray-500">{post.date}</div>
                    </div>
                  </div>
                  <span className="text-sm text-gray-500">{post.readTime}</span>
                </div>
              </div>
            </article>
          ))}
        </div>

        {/* Load More Button */}
        <div className="text-center mt-12">
          <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition duration-200 font-semibold">
            تحميل المزيد من المقالات
          </button>
        </div>

        {/* Newsletter Subscription */}
        <div className="bg-white rounded-lg shadow-lg p-8 mt-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">اشترك في نشرتنا الإخبارية</h2>
          <p className="text-gray-600 mb-6">احصل على أحدث المقالات والنصائح مباشرة في بريدك الإلكتروني</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <input
              type="email"
              placeholder="بريدك الإلكتروني"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-200 font-semibold">
              اشترك
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}