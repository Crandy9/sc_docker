FROM node:18-alpine

WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm install

COPY . ./