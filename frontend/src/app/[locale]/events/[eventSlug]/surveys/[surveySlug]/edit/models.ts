export interface Survey {
  slug: string;
  title?: string | null;
  languages: {
    language: string;
  }[];
}
