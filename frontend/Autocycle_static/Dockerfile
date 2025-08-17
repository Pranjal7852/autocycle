# Stage 1: Build the Next.js application
FROM node:22-slim AS builder
WORKDIR /app

# Copy package files first to leverage Docker cache for installations
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build the Next.js application
RUN npm run build

# Stage 2: Create the production image
FROM node:22-slim AS production
WORKDIR /app

# Copy package files for production dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Copy necessary files from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.mjs ./next.config.mjs
COPY --from=builder /app/.env ./.env

# Expose the port your app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]