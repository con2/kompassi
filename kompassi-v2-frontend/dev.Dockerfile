FROM node:24 AS deps
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:24 AS dev
WORKDIR /usr/src/app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /usr/src/app/node_modules ./node_modules
COPY scripts/ scripts/
COPY codegen.ts package.json package-lock.json next.config.ts tsconfig.json .eslintrc.json ./
# COPY public public
COPY src src

ENTRYPOINT [ "scripts/wait-for-it.sh", "-s", "-t", "120", "router:8000", "--" ]
CMD [ "npm", "run", "dev" ]
