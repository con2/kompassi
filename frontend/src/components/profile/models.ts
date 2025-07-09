import { graphql } from "@/__generated__";

graphql(`
  fragment FullOwnProfile on OwnProfileType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

graphql(`
  fragment FullSelectedProfile on SelectedProfileType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

graphql(`
  fragment FullLimitedProfile on LimitedProfileType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

graphql(`
  fragment FullProfileFieldSelector on ProfileFieldSelectorType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

export interface Profile {
  firstName: string;
  lastName: string;
  nick: string; // may be empty
  email: string;
  phoneNumber: string;
  discordHandle: string; // may be empty
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
