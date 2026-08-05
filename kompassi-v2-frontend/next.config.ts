import { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const bodySizeLimit = "100mb";

const nextConfig: NextConfig = {
  output: "standalone",
  transpilePackages: ["@con2/components"],
  logging: {
    incomingRequests: false,
  },
  experimental: {
    proxyClientMaxBodySize: bodySizeLimit,
    serverActions: {
      bodySizeLimit,
    },
  },
  sassOptions: {
    // bootstrap
    silenceDeprecations: [
      "import",
      "if-function",
      "legacy-js-api",
      "global-builtin",
      "color-functions",
    ],
    // Turbopack mishandles Sass's `@charset "UTF-8";` output: it gets turned
    // into a raw BOM that lands after Turbopack's own leading comment instead
    // of at byte 0, which invalidates the CSS rule it's glued to (Bootstrap's
    // `:root` variable declarations). We don't rely on non-ASCII output, so
    // just stop Sass from emitting a charset marker at all.
    charset: false,
  },
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
