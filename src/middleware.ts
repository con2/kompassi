import createMiddleware from "next-intl/middleware";

export default createMiddleware({
  locales: ["fi", "en"],
  defaultLocale: "en",
  localePrefix: "never",
});

export const config = {
  matcher: ["/", "/(fi|en)/:path*"],
};
