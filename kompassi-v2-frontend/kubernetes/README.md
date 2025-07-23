# Kubernetes deployment for kompassi2

Generate Kubernetes manifests using

    npm run k8s:generate

This runs the `kubernetes/manifest.ts` that is intended to be a brutally simple Node.js program with no other dependencies than `fs`. It accepts one environment variable, `ENV`, with the values `dev` (the default), `staging` and `production`, and outputs Kubernetes manifests as JSON files in the directory it was run.

Test with Skaffold (with Docker Desktop or similar local Kubernetes cluster):

    npm run k8s:dev

Assuming you have an [ingress controller set up](https://outline.con2.fi/doc/ingress-controller-XfVUOHtp2t#h-installing-an-ingress-controller-for-local-development), you should now be able to view the UI at http://kompassi2.localhost.

For staging and production, deployment is done in two steps using Skaffold:

    cd kubernetes && ENV=staging npx tsx manifest.ts && cd -
    skaffold build --file-output build.json
    skaffold deploy -n kompassi2-staging -a build.json

See `skaffold.yaml` in the repository root.

You should, for the most part, not deploy manually. GitHub Actions CI/CD is set up to deploy all commits to `main` into the staging environment at https://v2.dev.kompassi.eu, and after a manual gate into production at https://v2.kompassi.eu. See `.github/workflows/cicd.yaml`.
