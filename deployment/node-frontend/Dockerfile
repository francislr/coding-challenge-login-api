FROM node:11.9
RUN mkdir -p /srv
WORKDIR /code
COPY package.json /code/
RUN npm install
COPY . /code/

