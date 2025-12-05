#!/bin/sh
# =============================================================================
# Frontend Docker Entrypoint Script
# =============================================================================
# This script ensures dependencies are synchronized when the container starts.
# It compares checksums of package.json and pnpm-lock.yaml to detect changes.
# =============================================================================

set -e

DEPS_HASH_FILE="/app/.deps-hash"

# Calculate current hash of dependency files
calculate_deps_hash() {
    if [ -f "pnpm-lock.yaml" ]; then
        cat package.json pnpm-lock.yaml | sha256sum | cut -d' ' -f1
    else
        cat package.json | sha256sum | cut -d' ' -f1
    fi
}

CURRENT_HASH=$(calculate_deps_hash)

# Check if dependencies need to be reinstalled
if [ -f "$DEPS_HASH_FILE" ]; then
    STORED_HASH=$(cat "$DEPS_HASH_FILE")
    if [ "$CURRENT_HASH" != "$STORED_HASH" ]; then
        echo "📦 Dependencies changed, reinstalling..."
        pnpm install
        echo "$CURRENT_HASH" > "$DEPS_HASH_FILE"
        echo "✅ Dependencies updated!"
    else
        echo "✅ Dependencies up to date"
    fi
else
    # First run or node_modules missing
    if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
        echo "📦 Installing dependencies..."
        pnpm install
        echo "✅ Dependencies installed!"
    fi
    echo "$CURRENT_HASH" > "$DEPS_HASH_FILE"
fi

# Execute the main command
exec "$@"

