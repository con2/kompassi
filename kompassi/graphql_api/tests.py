def test_graphql_api_is_at_wellknown_url(client):
    assert client.get("/graphql").status_code != 404
