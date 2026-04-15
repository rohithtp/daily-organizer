#!/bin/bash

echo "--- Git Identity Setup (Local Repo) ---"

# Prompt user for input
read -p "Enter your Full Name: " gitname
read -p "Enter your Email: " gitemail

# Check if we are inside a git repository
if [ -d .git ] || git rev-parse --git-dir > /dev/null 2>&1; then

    # Validate email format before setting
    if ! [[ "$gitemail" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        echo -e "\n\033[31m❌ Error: Invalid email format. Please use format: user@example.com\033[0m"
        exit 1
    fi

    # Set local configuration
    git config user.name "$gitname" && \
    git config user.email "$gitemail"

    echo -e "\n\033[32m✅ Success! Local repo settings updated:\033[0m"
    echo -e "  Name: $gitname"
    echo -e "  Email: \033[34m$gitemail\033[0m"
else
    echo "❌ Error: This directory is not a Git repository."
    echo "Please run this script inside a project folder."
    exit 1
fi
