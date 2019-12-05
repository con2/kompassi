from rest_framework.routers import SimpleRouter


class OptionalTrailingSlashRouter(SimpleRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = '/?'
