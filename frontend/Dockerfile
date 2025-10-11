# Build stage
FROM node:lts-slim AS builder 
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Copy built files to volume
FROM alpine:latest
COPY --from=builder /app/build /build
CMD ["sh", "-c", "cp -r /build/* /usr/share/nginx/html/ && tail -f /dev/null"]