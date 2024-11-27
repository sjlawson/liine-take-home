/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://django:8000/api/:path*',
      },
    ]
  },
  skipTrailingSlashRedirect: true,
};

export default nextConfig;
