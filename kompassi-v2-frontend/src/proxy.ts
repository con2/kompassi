import { NextRequest } from "next/server";
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

const handleI18nRouting = createMiddleware(routing);

// Next removed the built-in way for a server component to read the current request's
// pathname, so stash it in a header here - next-intl forwards mutated request headers
// through its own rewrite, so `await headers()` downstream can read it back.
export default function proxy(request: NextRequest) {
  request.headers.set(
    "x-pathname",
    request.nextUrl.pathname + request.nextUrl.search,
  );
  return handleI18nRouting(request);
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|healthz).*)"],
};
