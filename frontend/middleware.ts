import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  
  // Handle Vite client requests that shouldn't exist in Next.js
  if (req.nextUrl.pathname.startsWith('/@vite/')) {
    return new NextResponse(null, { status: 404 });
  }

  // Handle other development-related requests
  if (req.nextUrl.pathname.startsWith('/__next')) {
    return NextResponse.next();
  }

  const supabase = createMiddlewareClient({ req, res })

  // تحديث الجلسة
  const {
    data: { session },
  } = await supabase.auth.getSession()

  // الصفحات المحمية التي تتطلب تسجيل دخول
  const protectedRoutes = [
    '/dashboard',
    '/profile',
    '/settings',
    '/create-video',
    '/my-videos'
  ]

  // الصفحات التي يجب إعادة توجيه المستخدم المسجل منها
  const authRoutes = [
    '/auth/login',
    '/auth/register',
    '/auth/forgot-password'
  ]

  const { pathname } = req.nextUrl

  // التحقق من الصفحات المحمية
  if (protectedRoutes.some(route => pathname.startsWith(route))) {
    if (!session) {
      // إعادة توجيه إلى صفحة تسجيل الدخول مع الاحتفاظ بالصفحة المطلوبة
      const redirectUrl = new URL('/auth/login', req.url)
      redirectUrl.searchParams.set('redirectTo', pathname)
      return NextResponse.redirect(redirectUrl)
    }
  }

  // إعادة توجيه المستخدمين المسجلين من صفحات المصادقة
  if (authRoutes.some(route => pathname.startsWith(route))) {
    if (session) {
      // التحقق من وجود redirectTo في query parameters
      const redirectTo = req.nextUrl.searchParams.get('redirectTo')
      const redirectUrl = new URL(redirectTo || '/dashboard', req.url)
      return NextResponse.redirect(redirectUrl)
    }
  }

  // التحقق من تأكيد البريد الإلكتروني
  if (pathname.startsWith('/auth/verify-email')) {
    if (session && session.user.email_confirmed_at) {
      return NextResponse.redirect(new URL('/dashboard', req.url))
    }
  }

  // السماح بالوصول للصفحات العامة
  return res
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}