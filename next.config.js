const withNextIntl = require("next-intl/plugin")();

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
};

module.exports = withNextIntl(nextConfig);
