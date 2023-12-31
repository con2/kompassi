import { HttpLink, DefaultContext } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import {
  NextSSRInMemoryCache,
  NextSSRApolloClient,
} from "@apollo/experimental-nextjs-app-support/ssr";
import { registerApolloClient } from "@apollo/experimental-nextjs-app-support/rsc";
import { kompassiBaseUrl } from "./config";
import { auth } from "./auth";

const authLink = setContext(async (_, context) => {
  const session = await auth();

  if (session?.accessToken) {
    const headers = context.headers ?? {};
    return {
      headers: { ...headers, authorization: `Bearer ${session.accessToken}` },
    };
  }

  return {};
});

const httpLink = new HttpLink({
  uri: `${kompassiBaseUrl}/graphql`,
});

export const { getClient } = registerApolloClient(() => {
  return new NextSSRApolloClient({
    cache: new NextSSRInMemoryCache(),
    link: authLink.concat(httpLink),
  });
});
