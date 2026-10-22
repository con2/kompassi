import type { Values } from "./models";

export interface FormDraft {
  savedAt: string;
  values: Values;
}

const storagePrefix = "kompassi.draft.v1:";
const maxAgeMs = 30 * 24 * 60 * 60 * 1000;

function storageKey(draftKey: string): string {
  return `${storagePrefix}${draftKey}`;
}

// localStorage is unavailable during SSR and may throw in private browsing or
// when the quota is exhausted. Drafts are a convenience, so every failure is
// swallowed and the form behaves as if no draft existed.
function getStorage(): Storage | null {
  try {
    return typeof window === "undefined" ? null : window.localStorage;
  } catch {
    return null;
  }
}

function isExpired(draft: FormDraft, now: number): boolean {
  const savedAt = Date.parse(draft.savedAt);
  return Number.isNaN(savedAt) || now - savedAt > maxAgeMs;
}

export function loadDraft(draftKey: string): FormDraft | null {
  const storage = getStorage();
  if (!storage) return null;
  try {
    const raw = storage.getItem(storageKey(draftKey));
    if (!raw) return null;
    const draft = JSON.parse(raw) as FormDraft;
    if (
      typeof draft?.savedAt !== "string" ||
      typeof draft?.values !== "object" ||
      draft.values === null ||
      isExpired(draft, Date.now())
    ) {
      return null;
    }
    return draft;
  } catch {
    return null;
  }
}

export function saveDraft(draftKey: string, values: Values): void {
  const storage = getStorage();
  if (!storage) return;
  const draft: FormDraft = { savedAt: new Date().toISOString(), values };
  try {
    storage.setItem(storageKey(draftKey), JSON.stringify(draft));
  } catch {
    // quota exceeded or storage disabled
  }
}

export function clearDraft(draftKey: string): void {
  const storage = getStorage();
  if (!storage) return;
  try {
    storage.removeItem(storageKey(draftKey));
  } catch {
    // storage disabled
  }
}

export function pruneExpiredDrafts(): void {
  const storage = getStorage();
  if (!storage) return;
  try {
    const now = Date.now();
    const expiredKeys: string[] = [];
    for (let i = 0; i < storage.length; i++) {
      const key = storage.key(i);
      if (!key?.startsWith(storagePrefix)) continue;
      try {
        const draft = JSON.parse(storage.getItem(key) ?? "") as FormDraft;
        if (isExpired(draft, now)) expiredKeys.push(key);
      } catch {
        expiredKeys.push(key);
      }
    }
    for (const key of expiredKeys) storage.removeItem(key);
  } catch {
    // storage disabled
  }
}
