import { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const bodySizeLimit = "100mb";

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    middlewareClientMaxBodySize: bodySizeLimit,
    serverActions: {
      bodySizeLimit,
    },
  },
  sassOptions: {
    // bootstrap
    silenceDeprecations: [
      "legacy-js-api",
      "import",
      "global-builtin",
      "color-functions",
    ],
  },
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
