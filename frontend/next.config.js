/** @type {import('next').NextConfig} */
let nextConfig = {
  distDir: "dist",
};

if (process.env.NODE_ENV === "development") {
  nextConfig.rewrites = async () => {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:5678/api/:path*",
      },
    ];
  };
} else {
  nextConfig.output = "export";
}

module.exports = nextConfig;
