export interface Organization {
  slug: string;
  name: string;
}

export interface Registry {
  organization: Organization;
  slug: string;
  title: string;
  policyUrl: string;
}
