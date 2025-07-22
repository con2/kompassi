import { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    serverActions: {
      bodySizeLimit: "100mb",
    },
  },
  sassOptions: {
    silenceDeprecations: ["legacy-js-api"],
  },
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
