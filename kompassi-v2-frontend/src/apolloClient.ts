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
import { headers } from "next/headers";
import { forbidden, notFound, redirect } from "next/navigation";
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

/// Machine-readable codes a GraphQLError may carry in extensions.code (see
/// kompassi/access/constants.py and kompassi/graphql_api/errors.py on the backend).
const NOT_FOUND = "NOT_FOUND";
const CBAC_PERMISSION_DENIED = "CBAC_PERMISSION_DENIED";

/// The claim keys a CBAC denial may expose to a superuser (see CBAC_SUDO_CLAIMS in
/// kompassi/access/constants.py). Sudo can never grant more than these.
export const CBAC_SUDO_CLAIM_KEYS = ["organization", "event", "app"] as const;

/// Returns the extensions.code of the first GraphQL error, if any. Callers branch on
/// this instead of matching an error's English message.
export function graphqlErrorCode(error: unknown): string | undefined {
  if (CombinedGraphQLErrors.is(error)) {
    for (const { extensions } of error.errors) {
      const code = extensions?.code;
      if (typeof code === "string") {
        return code;
      }
    }
  }

  return undefined;
}

/// Returns the denied claims a CBAC_PERMISSION_DENIED error exposes, if any. Only ever
/// present for a superuser (see expose_claims in kompassi/access/cbac.py); a normal
/// user's denial carries no claims, so this returns undefined for them.
function cbacDeniedClaims(error: unknown): Record<string, string> | undefined {
  if (CombinedGraphQLErrors.is(error)) {
    for (const { extensions } of error.errors) {
      if (extensions?.code === CBAC_PERMISSION_DENIED && extensions.claims) {
        return extensions.claims as Record<string, string>;
      }
    }
  }

  return undefined;
}

async function sudoUrl(claims: Record<string, string>): Promise<string> {
  const headerList = await headers();
  const pathname = headerList.get("x-pathname") ?? "/";

  const params = new URLSearchParams({ next: pathname });
  for (const key of CBAC_SUDO_CLAIM_KEYS) {
    const value = claims[key];
    if (value) {
      params.set(key, value);
    }
  }

  return `/sudo?${params.toString()}`;
}

async function handleGraphQLError(error: unknown): Promise<never> {
  const code = graphqlErrorCode(error);

  if (code === NOT_FOUND) {
    notFound();
  }

  if (code === CBAC_PERMISSION_DENIED) {
    const claims = cbacDeniedClaims(error);
    if (claims) {
      // superuser: offer the sudo override instead of a flat 403
      redirect(await sudoUrl(claims));
    }
    forbidden();
  }

  throw error;
}

/**
 * `errorPolicy` defaults to "none" at runtime (GraphQL errors reject the
 * promise), but Apollo Client 4's types only narrow `data` to non-undefined
 * when `errorPolicy: "none"` is passed explicitly. This wrapper does that so
 * call sites don't all need `data!` or null checks for a case that can't happen.
 *
 * It also catches CBAC_PERMISSION_DENIED / NOT_FOUND errors and turns them into the
 * appropriate Next.js interrupt (forbidden()/notFound()/a redirect to /sudo) so callers
 * get a real error page instead of falling through to the generic error boundary.
 */
export function getClient() {
  const client = getRawClient();
  return {
    async query<TData, TVariables extends OperationVariables>(
      options: Omit<
        ApolloClientNamespace.QueryOptions<TData, TVariables>,
        "errorPolicy"
      >,
    ): Promise<{ data: TData }> {
      try {
        return (await client.query({
          ...options,
          errorPolicy: "none",
        } as any)) as { data: TData };
      } catch (error) {
        return handleGraphQLError(error);
      }
    },
    async mutate<TData, TVariables extends OperationVariables>(
      options: Omit<
        ApolloClientNamespace.MutateOptions<TData, TVariables>,
        "errorPolicy"
      >,
    ): Promise<{ data: TData }> {
      try {
        return (await client.mutate({
          ...options,
          errorPolicy: "none",
        } as any)) as { data: TData };
      } catch (error) {
        return handleGraphQLError(error);
      }
    },
  };
}
