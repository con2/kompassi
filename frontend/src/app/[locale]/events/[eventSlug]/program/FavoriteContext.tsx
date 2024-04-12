"use client";

import { createContext, useCallback, useState } from "react";
import type { Translations } from "@/translations/en";

interface FavoriteContextValue {
  markAsFavorite(programSlug: string): Promise<void>;
  unmarkAsFavorite(programSlug: string): Promise<void>;
  isFavorite(programSlug: string): boolean;
  messages: Translations["Program"]["favorites"];
}

const nullFavoriteContextValue: FavoriteContextValue = {
  async markAsFavorite() {},
  async unmarkAsFavorite() {},
  isFavorite() {
    return false;
  },
  messages: {
    markAsFavorite: "",
    unmarkAsFavorite: "",
    signInToAddFavorites: "",
  },
};

export const FavoriteContext = createContext<FavoriteContextValue>(
  nullFavoriteContextValue,
);

interface Props {
  markAsFavorite(programSlug: string): Promise<void>;
  unmarkAsFavorite(programSlug: string): Promise<void>;
  slugs: string[];
  messages: Translations["Program"]["favorites"];
  children: React.ReactNode;
}

/// This context provider avoids having to supply these props
/// hundreds of times over the server–client component boundary.
export function FavoriteContextProvider(props: Props) {
  const {
    slugs,
    messages,
    children,
    markAsFavorite: upstreamMarkAsFavorite,
    unmarkAsFavorite: upstreamUnmarkAsFavorite,
  } = props;
  const [favorites, setFavorites] = useState(new Set(slugs));

  const markAsFavorite = useCallback(
    async (programSlug: string) => {
      setFavorites((prev) => new Set([...prev, programSlug]));
      return upstreamMarkAsFavorite(programSlug);
    },
    [upstreamMarkAsFavorite],
  );

  const unmarkAsFavorite = useCallback(
    async (programSlug: string) => {
      setFavorites((prev) => {
        const next = new Set(prev);
        next.delete(programSlug);
        return next;
      });
      return upstreamUnmarkAsFavorite(programSlug);
    },
    [upstreamUnmarkAsFavorite],
  );

  const isFavorite = useCallback(
    (programSlug: string) => {
      return favorites.has(programSlug);
    },
    [favorites],
  );

  return (
    <FavoriteContext.Provider
      value={{ markAsFavorite, unmarkAsFavorite, isFavorite, messages }}
    >
      {children}
    </FavoriteContext.Provider>
  );
}
