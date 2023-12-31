"use client";

import { signIn } from "next-auth/react";

import type { Translations } from "@/translations/en";

interface SignInRequiredProps {
  translations: Translations["SignInRequired"];
}

export function SignInRequired({ translations }: SignInRequiredProps) {
  return (
    <div className="container mt-4">
      <h1>{translations.title}</h1>
      <p>{translations.message}</p>
      <button onClick={() => signIn("kompassi")} className="btn btn-primary">
        {translations.signIn}…
      </button>
    </div>
  );
}
