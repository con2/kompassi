"use client";

import { signIn } from "next-auth/react";

import type { Translations } from "@/translations/en";

interface SignInRequiredProps {
  messages: Translations["SignInRequired"];
}

export default function SignInRequired({ messages }: SignInRequiredProps) {
  return (
    <div className="container mt-4">
      <h1>{messages.title}</h1>
      <p>{messages.message}</p>
      <button onClick={() => signIn("kompassi")} className="btn btn-primary">
        {messages.signIn}…
      </button>
    </div>
  );
}
