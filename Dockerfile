FROM node:18 as deps
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:18 as builder
WORKDIR /usr/src/app
ENV NEXT_TELEMETRY_DISABLED 1
COPY --from=deps /usr/src/app/node_modules ./node_modules
COPY package.json package-lock.json next.config.js tsconfig.json .eslintrc.json ./
# COPY public public
COPY src src
RUN npm run build

FROM node:18 as runner
WORKDIR /usr/src/app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
ENV PORT 3000
COPY --from=builder /usr/src/app/.next/standalone ./
# COPY --from=builder /usr/src/app/public public
COPY --from=builder /usr/src/app/.next/static .next/static
CMD ["node", "server.js"]
