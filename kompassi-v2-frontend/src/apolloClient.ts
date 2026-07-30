import { HttpLink, CombinedGraphQLErrors } from "@apollo/client";
import type { ApolloClient as ApolloClientNamespace } from "@apollo/client";
import type { OperationVariables } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { ErrorLink } from "@apollo/client/link/error";
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
      headers: {
        ...headers,
        authorization: `Bearer ${session.accessToken}`,
      },
    };
  }

  return {};
});

const errorLink = new ErrorLink(({ error }) => {
  if (CombinedGraphQLErrors.is(error)) {
    error.errors.forEach(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );
  } else {
    console.error(`[Network error]: ${error}`);
  }
});

const httpLink = new HttpLink({
  uri: `${kompassiBaseUrl}/graphql`,
});

const {
  getClient: getRawClient,
  query,
  PreloadQuery,
} = registerApolloClient(() => {
  return new ApolloClient({
    cache: new InMemoryCache(),
    link: authLink.concat(errorLink).concat(httpLink),
  });
});

export { query, PreloadQuery };

/**
 * `errorPolicy` defaults to "none" at runtime (GraphQL errors reject the
 * promise), but Apollo Client 4's types only narrow `data` to non-undefined
 * when `errorPolicy: "none"` is passed explicitly. This wrapper does that so
 * call sites don't all need `data!` or null checks for a case that can't happen.
 */
export function getClient() {
  const client = getRawClient();
  return {
    query<TData, TVariables extends OperationVariables>(
      options: Omit<
        ApolloClientNamespace.QueryOptions<TData, TVariables>,
        "errorPolicy"
      >,
    ): Promise<{ data: TData }> {
      return client.query({
        ...options,
        errorPolicy: "none",
      } as any) as Promise<{ data: TData }>;
    },
    mutate<TData, TVariables extends OperationVariables>(
      options: Omit<
        ApolloClientNamespace.MutateOptions<TData, TVariables>,
        "errorPolicy"
      >,
    ): Promise<{ data: TData }> {
      return client.mutate({
        ...options,
        errorPolicy: "none",
      } as any) as Promise<{ data: TData }>;
    },
  };
}
