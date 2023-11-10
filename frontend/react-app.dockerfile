FROM node:alpine

WORKDIR /app

COPY package.json .

RUN npm install 

COPY . .

ARG REACT_APP_SECRET_KEY
ENV REACT_APP_SECRET_KEY $REACT_APP_SECRET_KEY


CMD ["npm","start"]