# =============================================================================
# Developer Dashboard Frontend - Dockerfile
# =============================================================================
# Multi-stage build:
# 1. Build stage: Install deps and build
# 2. Production stage: Serve with Nginx
#
# Railway injects PORT at runtime. We use envsubst to render
# nginx.conf.template with the correct port and backend URL.

# -----------------------------------------------------------------------------
# Stage 1: Build
# -----------------------------------------------------------------------------
FROM node:22-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
# This creates optimized production files in /app/dist
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 2: Production
# -----------------------------------------------------------------------------
FROM nginx:alpine as production

# Labels
LABEL maintainer="Developer Dashboard"
LABEL description="React frontend for Developer Dashboard"

# Copy nginx config template (substituted at startup)
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Default environment variables (Railway overrides PORT at runtime)
ENV PORT=3000
ENV BACKEND_URL=http://backend:8000

# Expose port
EXPOSE ${PORT}

# Health check using the dynamic port
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:${PORT} || exit 1

# nginx:alpine image auto-runs envsubst on /etc/nginx/templates/*.template
# and outputs to /etc/nginx/conf.d/ before starting nginx
CMD ["nginx", "-g", "daemon off;"]
