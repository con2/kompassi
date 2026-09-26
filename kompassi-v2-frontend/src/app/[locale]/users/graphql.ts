import { graphql } from "@/__generated__";

graphql(`
  fragment AdminPerson on AdminPersonType {
    id
    firstName
    lastName
    nick
    displayName
    email
    phoneNumber
    discordHandle
    username
    isSuperuser
    isActive
    emailVerifiedAt
    dateJoined
    lastLogin
    notes
    groups
  }
`);
