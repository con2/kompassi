import { AuthOptions } from "next-auth";

import { kompassiOidc } from "@/config";

export const authOptions: AuthOptions = {
  providers: [
    {
      id: "kompassi",
      name: "Kompassi",
      type: "oauth",
      profile: (profile) => {
        return {
          image: null,
          id: profile.sub,
          name: profile.name,
          email: profile.email,
        };
      },
      idToken: true,
      ...kompassiOidc,
    },
  ],
};
