import { HttpLink, DefaultContext } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import {
  registerApolloClient,
  ApolloClient,
  InMemoryCache,
} from "@apollo/client-integration-nextjs";
import { auth } from "./auth";
import { kompassiBaseUrl } from "./config";

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

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );

  if (networkError) console.error(`[Network error]: ${networkError}`);
});

const httpLink = new HttpLink({
  uri: `${kompassiBaseUrl}/graphql`,
});

export const { getClient } = registerApolloClient(() => {
  return new ApolloClient({
    cache: new InMemoryCache(),
    link: authLink.concat(errorLink).concat(httpLink),
  });
});
