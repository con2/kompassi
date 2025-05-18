export interface Profile {
  firstName: string;
  lastName: string;
  nick: string; // may be empty
  email: string;
  phoneNumber: string;
  discordHandle: string; // may be empty
  [key: string]: string; // for other fields
}

/// NOTE: Must match ProfileFieldSelector in backend
export interface ProfileFieldSelector {
  firstName?: boolean;
  lastName?: boolean;
  nick?: boolean;
  email?: boolean;
  phoneNumber?: boolean;
  discordHandle?: boolean;
}

export type ProfileField = keyof ProfileFieldSelector;
export const profileFields: ProfileField[] = [
  "firstName",
  "lastName",
  "nick",
  "email",
  "phoneNumber",
  "discordHandle",
];

export const allProfileFields: ProfileFieldSelector = {
  firstName: true,
  lastName: true,
  nick: true,
  email: true,
  phoneNumber: true,
  discordHandle: true,
};

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
