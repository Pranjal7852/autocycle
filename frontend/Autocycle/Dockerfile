# Stage 1: Build the Next.js application
FROM node:22-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Create the production image
FROM node:22-slim AS production
WORKDIR /app
COPY --from=builder /app/.next .
COPY --from=builder /app/public ./public
COPY package*.json ./
RUN npm install --omit=dev # Install only production dependencies
EXPOSE 3000
CMD ["npm", "start"]
# Or, if you have a custom server:
# CMD ["node", "server.js"]