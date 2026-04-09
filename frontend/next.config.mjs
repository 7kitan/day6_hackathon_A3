/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  rewrites: async () => {
    return [
      {
        source: '/api/python-chat/:path*',
        destination: 'http://localhost:8000/:path*',
      },
      {
        source: '/api/attractions',
        destination: 'http://localhost:8000/attractions',
      },
    ]
  },
}

export default nextConfig
