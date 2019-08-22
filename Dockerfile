FROM node:12

WORKDIR /usr/src/app
EXPOSE 3000

COPY package.json package-lock.json tsconfig.json tslint.json /usr/src/app/
RUN npm install
COPY public /usr/src/app/public
COPY src /usr/src/app/src

USER node

CMD ["node_modules/.bin/react-scripts", "start"]
