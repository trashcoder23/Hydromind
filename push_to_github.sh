#!/bin/bash
# push_to_github.sh - Script to push HydroMind to GitHub

echo "🚀 HydroMind - GitHub Push Script"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Add remote if not exists
if ! git remote | grep -q "origin"; then
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/trashcoder23/Hydromind.git
    echo "✅ Remote added"
else
    echo "✅ Remote already exists"
    git remote set-url origin https://github.com/trashcoder23/Hydromind.git
fi

# Stage all files
echo ""
echo "📝 Staging files..."
git add .

# Show status
echo ""
echo "📊 Git Status:"
git status --short

# Commit
echo ""
read -p "Enter commit message (default: 'Initial commit - HydroMind IoT System'): " commit_msg
commit_msg=${commit_msg:-"Initial commit - HydroMind IoT System"}

echo "💾 Committing changes..."
git commit -m "$commit_msg"

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main --force

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🔗 Repository: https://github.com/trashcoder23/Hydromind"
echo ""
echo "⚠️  IMPORTANT: Make sure you've removed any sensitive data:"
echo "   - Firebase credentials"
echo "   - Service account keys"
echo "   - API keys"
echo ""
