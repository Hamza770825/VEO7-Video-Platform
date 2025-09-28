import type { Metadata } from 'next'
import { Inter, Noto_Sans_Arabic } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter'
})

const notoSansArabic = Noto_Sans_Arabic({ 
  subsets: ['arabic'],
  display: 'swap',
  variable: '--font-noto-arabic'
})

export const metadata: Metadata = {
  title: 'VEO7 - Professional Video Generation Platform',
  description: 'Create stunning AI-powered videos with image animation and voice synthesis. Professional video generation made simple.',
  keywords: ['video generation', 'AI', 'image animation', 'text to speech', 'video creation'],
  authors: [{ name: 'VEO7 Team' }],
  creator: 'VEO7',
  publisher: 'VEO7',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  openGraph: {
    title: 'VEO7 - Professional Video Generation Platform',
    description: 'Create stunning AI-powered videos with image animation and voice synthesis.',
    url: '/',
    siteName: 'VEO7',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'VEO7 Video Platform',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'VEO7 - Professional Video Generation Platform',
    description: 'Create stunning AI-powered videos with image animation and voice synthesis.',
    images: ['/og-image.png'],
    creator: '@veo7platform',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.svg" />
        <link rel="icon" type="image/svg+xml" sizes="32x32" href="/favicon-32x32.svg" />
        <link rel="icon" type="image/svg+xml" sizes="16x16" href="/favicon-16x16.svg" />
        <link rel="manifest" href="/site.webmanifest" />
        <meta name="theme-color" content="#3b82f6" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
      </head>
      <body className={`${inter.variable} ${notoSansArabic.variable} font-sans antialiased`}>
        <Providers>
          <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900">
            {children}
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}