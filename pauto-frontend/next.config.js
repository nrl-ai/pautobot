/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => [
    {
      source: "/api/:path*",
      destination: "http://127.0.0.1:5678/api/:path*",
    },
  ],
};

module.exports = nextConfig;
