FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3006
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3006/health || exit 1
CMD ["node", "app.js"]
