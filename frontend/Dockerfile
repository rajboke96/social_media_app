FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
ARG VITE_GRAPHQL_URL
ENV VITE_GRAPHQL_URL=${VITE_GRAPHQL_URL:-http://127.0.0.1:8000/graphql}

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
