# Next generation UI for the Kompassi Event Management System

## Getting Started

```bash
npm install
npm run dev
open http://localhost:3000
```

By default, the development environment will connect to the Kompassi development instance at `dev.kompassi.eu`. To connect to a local instance instead (ie. one you have started with `docker compose up` in `kompassi`):

```bash
export NEXT_PUBLIC_KOMPASSI_BASE_URL=http://localhost:8000
```

To connect to the production instance instead:

```bash
export NEXT_PUBLIC_KOMPASSI_BASE_URL=https://kompassi.eu
```
