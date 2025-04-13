FROM node:20-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build
RUN npm install -g serve

CMD ["serve", "www", "-s", "-l", "5000"]
