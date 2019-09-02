from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter


class OptionalTrailingSlashMixin:
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.trailing_slash = '/?'


class OptionalTrailingSlashRouter(OptionalTrailingSlashMixin, SimpleRouter):
    pass


class OptionalTrailingSlashNestedRouter(OptionalTrailingSlashMixin, NestedSimpleRouter):
    pass
