# Kubernetes deployment for kompassi2

Generate Kubernetes manifests using

    cd kubernetes
    npx ts-node manifest.ts

Test with Skaffold:

    skaffold dev

Generate config for staging or production:

    ENV=staging npx ts-node manifest.ts
    ENV=production npx ts-node manifest.ts
