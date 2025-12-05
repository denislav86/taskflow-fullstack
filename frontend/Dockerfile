# =============================================================================
# TaskFlow Frontend - Development Dockerfile
# =============================================================================
# This Dockerfile is optimized for local development with:
# - pnpm for fast, efficient dependency management
# - Proper layer caching for quick rebuilds
# - Hot module replacement (HMR) support via Vite
# =============================================================================

FROM node:20-alpine

# Install pnpm globally
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy dependency files first for better layer caching
# This layer is only rebuilt when package.json or pnpm-lock.yaml changes
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
# Using --frozen-lockfile ensures reproducible builds when lockfile exists
# Falls back to regular install if no lockfile (first run)
RUN pnpm install --frozen-lockfile 2>/dev/null || pnpm install

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy source code
# This layer changes frequently but doesn't affect dependency installation
COPY . .

# Expose Vite dev server port
EXPOSE 3000

# Use entrypoint script to handle dependency synchronization
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command - start Vite dev server
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
