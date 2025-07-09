from event_log_v2 import registry

registry.register(
    name="directory.search.performed",
    message="User {actor} searched the {organization} directory for: {search_term}",
)


registry.register(
    name="directory.viewed",
    message="User {actor} browsed the {organization} directory without a search term.",
)
