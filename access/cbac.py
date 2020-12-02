

def get_default_claims(request):
    claims = {}

    # from CoreMiddleware
    if event := getattr(request, 'event'):
        claims['event'] = event.slug
    if organization := getattr(request, 'organization'):
        claims['organization'] = organization.slug

    # from Django router
    claims['method'] = request.method
    claims['path'] = request.path

    if url_name := request.resolver_match.url_name:
        claims['view'] = url_name
    if namespace := request.resolver_match.namespace:
        claims['app'] = namespace

    print(request.resolver_match)

    return claims
