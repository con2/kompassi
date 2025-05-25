export interface Survey {
  slug: string;
  title?: string | null;
  canRemove: boolean;
  languages: {
    language: string;
  }[];
  purpose: "DEFAULT" | "INVITE";
}
