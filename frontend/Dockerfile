FROM node:22-alpine AS builder
WORKDIR /app
RUN npm init -y && npm pkg set type=module && npm install --save-exact react@19.2.6 react-dom@19.2.6 lucide-react@1.31.0 vite@8.0.13 @vitejs/plugin-react@6.0.2 typescript@5.9.3
COPY frontend ./frontend
COPY app/globals.css ./app/globals.css
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ARG VITE_APP_TOKEN
ENV VITE_APP_TOKEN=$VITE_APP_TOKEN
RUN npx vite build --config frontend/vite.config.ts
FROM nginx:alpine
COPY --from=builder /app/dist-local /usr/share/nginx/html
EXPOSE 80
