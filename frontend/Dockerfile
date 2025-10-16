# Build stage
FROM node:lts-slim AS builder 
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY --from=builder /app/static /usr/share/nginx/html
COPY --from=builder /app/src /usr/share/nginx/html/src
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]