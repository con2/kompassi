"use client";

import Link from "next/link";
import { Session } from "next-auth";
import { signIn, signOut } from "next-auth/react";
import { useReducer } from "react";

import type { Translations } from "@/translations/en";

interface UserMenuProps {
  session: Session | null;
  messages: Translations["UserMenu"];
}

export default function UserMenu({ session, messages }: UserMenuProps) {
  const [isOpen, toggleOpen] = useReducer((isOpen) => !isOpen, false);

  if (!session?.user) {
    return (
      <button
        onClick={() => signIn("kompassi")}
        className="nav-link btn btn-link"
      >
        {messages.signIn}…
      </button>
    );
  }

  return (
    <div className="nav-item dropdown">
      <button
        className="nav-link btn btn-link dropdown-toggle"
        id="user-menu"
        role="button"
        aria-expanded={isOpen}
        onClick={toggleOpen}
      >
        {session.user.name}
      </button>
      <ul
        className={`dropdown-menu dropdown-menu-end ${isOpen ? "show" : ""}`}
        aria-labelledby="user-menu"
      >
        <li>
          <Link
            className="dropdown-item"
            href={`/profile/responses`}
            onClick={toggleOpen}
          >
            {messages.responses}
          </Link>
        </li>
        <li>
          <hr className="dropdown-divider" />
        </li>
        <li>
          <button className="dropdown-item" onClick={() => signOut()}>
            {messages.signOut}
          </button>
        </li>
      </ul>
    </div>
  );
}
