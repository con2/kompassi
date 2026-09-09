export interface Survey {
  slug: string;
  title?: string | null;
  canRemove: boolean;
  canGrantAccess: boolean;
  languages: {
    language: string;
  }[];
  purpose: "DEFAULT" | "INVITE";
}
