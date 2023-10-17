import { NextRequest, NextResponse } from "next/server";
import {
  SupportedLanguage,
  defaultLanguage,
  isSupportedLanguage,
  supportedLanguages,
} from "./translations";

function detectLanguage(request: NextRequest): SupportedLanguage {
  const cookie = request.cookies.get("NEXT_LOCALE");
  if (cookie && isSupportedLanguage(cookie.value)) {
    return cookie.value;
  }

  const acceptLanguage = request.headers.get("accept-language");
  if (acceptLanguage) {
    const languages = acceptLanguage
      .split(",")
      .map((s) => s.split(";")[0].split("-")[0]);
    for (const language of languages) {
      if (isSupportedLanguage(language)) {
        return language;
      }
    }
  }

  return defaultLanguage;
}

export function middleware(request: NextRequest) {
  const detectedLanguage = detectLanguage(request);

  // strip /en, /fi etc. from URL, setting the language cookie
  for (const requestedLanguage of supportedLanguages) {
    if (
      request.nextUrl.pathname === `/${requestedLanguage}` ||
      request.nextUrl.pathname.startsWith(`/${requestedLanguage}/`)
    ) {
      const response = NextResponse.redirect(
        new URL(
          request.nextUrl.pathname.slice(requestedLanguage.length + 1),
          request.url
        )
      );
      response.cookies.set("NEXT_LOCALE", requestedLanguage, { path: "/" });
      return response;
    }
  }

  // inject detected language into URL seen by next.js
  return NextResponse.rewrite(
    new URL(`/${detectedLanguage}${request.nextUrl.pathname}`, request.url)
  );
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
