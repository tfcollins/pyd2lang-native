#!/usr/bin/env bash
# Release script for pyd2lang-native
#
# Usage:
#   ./scripts/release.sh [major|minor|patch]
#
# Default bump type is "patch".
#
# What it does:
#   1. Reads the current version from d2/__init__.py
#   2. Computes the next version based on bump type
#   3. Shows changelog (commits since last tag)
#   4. Updates __version__ in d2/__init__.py
#   5. Commits the version bump
#   6. Creates a signed git tag (vX.Y.Z)
#   7. Pushes commit and tag to origin
#
# The tag push triggers the CI workflow which builds wheels and publishes to PyPI.

set -euo pipefail

BUMP_TYPE="${1:-patch}"
INIT_FILE="d2/__init__.py"

# Ensure we're in the repo root
if [[ ! -f "$INIT_FILE" ]]; then
    echo "Error: must be run from the repository root (could not find $INIT_FILE)"
    exit 1
fi

# Ensure working tree is clean
if [[ -n "$(git status --porcelain)" ]]; then
    echo "Error: working tree is not clean. Commit or stash changes first."
    exit 1
fi

# Ensure we're on main
BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "main" ]]; then
    echo "Warning: you are on branch '$BRANCH', not 'main'."
    read -rp "Continue anyway? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
fi

# Read current version
CURRENT_VERSION="$(grep -oP '(?<=__version__ = ")[^"]+' "$INIT_FILE")"
if [[ -z "$CURRENT_VERSION" ]]; then
    echo "Error: could not read __version__ from $INIT_FILE"
    exit 1
fi

# Parse semver components
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Compute next version
case "$BUMP_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Error: bump type must be 'major', 'minor', or 'patch' (got '$BUMP_TYPE')"
        exit 1
        ;;
esac

NEXT_VERSION="${MAJOR}.${MINOR}.${PATCH}"
TAG="v${NEXT_VERSION}"

# Check tag doesn't already exist
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "Error: tag $TAG already exists"
    exit 1
fi

# Show what's about to happen
echo "============================================"
echo "  Release: $CURRENT_VERSION → $NEXT_VERSION"
echo "  Tag:     $TAG"
echo "  Bump:    $BUMP_TYPE"
echo "============================================"
echo ""

# Show changelog since last tag
LAST_TAG="$(git describe --tags --abbrev=0 2>/dev/null || echo "")"
if [[ -n "$LAST_TAG" ]]; then
    echo "Changelog since $LAST_TAG:"
    echo "-------------------------------------------"
    git log --oneline "${LAST_TAG}..HEAD"
    echo "-------------------------------------------"
else
    echo "No previous tags found. This will be the first release."
fi
echo ""

# Confirm
read -rp "Proceed with release? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }

# Update version in __init__.py
sed -i "s/__version__ = \"${CURRENT_VERSION}\"/__version__ = \"${NEXT_VERSION}\"/" "$INIT_FILE"

# Verify the change
NEW_VERSION="$(grep -oP '(?<=__version__ = ")[^"]+' "$INIT_FILE")"
if [[ "$NEW_VERSION" != "$NEXT_VERSION" ]]; then
    echo "Error: version update failed (expected $NEXT_VERSION, got $NEW_VERSION)"
    git checkout -- "$INIT_FILE"
    exit 1
fi

# Commit version bump
git add "$INIT_FILE"
git commit -m "Release $TAG"

# Create tag
git tag -a "$TAG" -m "Release $NEXT_VERSION"

# Push commit and tag
git push origin "$BRANCH"
git push origin "$TAG"

echo ""
echo "============================================"
echo "  Released $TAG"
echo "  PyPI publish will be triggered by CI"
echo "============================================"
