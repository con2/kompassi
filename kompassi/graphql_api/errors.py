# Machine-readable code the frontend branches on (via extensions.code) when a resolver's
# ObjectDoesNotExist is translated into a GraphQLError. Kept import-light (no Django models)
# to avoid import cycles, same rationale as kompassi/tickets_v2/graphql/errors.py.
NOT_FOUND = "NOT_FOUND"
