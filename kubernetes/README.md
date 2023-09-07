# Kubernetes deployment for kompassi2

Uses the [`node-app` default template]() of Emskaffolden. Examples:

    # test locally (eg. Docker Desktop)
    emsk -T node-app dev

    # deploy to a cluster
    emsk -T node-app -E staging -- build --file-output build.json
    emsk -T node-app -E staging -- deploy -n kompassi2-staging -a build.json
