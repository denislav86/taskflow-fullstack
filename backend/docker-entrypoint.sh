#!/bin/bash
# =============================================================================
# Backend Docker Entrypoint Script
# =============================================================================
# This script handles:
# - Waiting for the database to be ready
# - Running database migrations
# - Starting the application
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Wait for database to be ready
wait_for_db() {
    log_info "Waiting for database to be ready..."
    
    MAX_RETRIES=30
    RETRY_COUNT=0
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if python -c "
from sqlalchemy import create_engine
from app.core.config import settings
engine = create_engine(settings.DATABASE_URL)
engine.connect()
" 2>/dev/null; then
            log_info "Database is ready!"
            return 0
        fi
        
        RETRY_COUNT=$((RETRY_COUNT + 1))
        log_warn "Database not ready (attempt $RETRY_COUNT/$MAX_RETRIES). Retrying in 2s..."
        sleep 2
    done
    
    log_error "Database connection failed after $MAX_RETRIES attempts"
    exit 1
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    if alembic upgrade head; then
        log_info "Migrations completed successfully!"
    else
        log_warn "Migration failed or no migrations to run"
    fi
}

# Main entrypoint logic
main() {
    # Only wait for DB and run migrations if DATABASE_URL is set
    if [ -n "$DATABASE_URL" ]; then
        wait_for_db
        
        # Run migrations unless explicitly disabled
        if [ "$SKIP_MIGRATIONS" != "true" ]; then
            run_migrations
        fi
    fi
    
    log_info "Starting application..."
    exec "$@"
}

main "$@"

