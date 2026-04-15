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

    # Get existing configurations
    current_name=$(git config --get user.name)
    current_email=$(git config --get user.email)

    # Determine if changes are needed
    update_name=false
    update_email=false

    if [ "$current_name" != "$gitname" ]; then
        echo -e "\n⚠️  Name differs from current Git configuration."
        read -p "Do you want to override the name (y/n)? " choice
        case $choice in
            y|Y ) update_name=true ;;
            * ) update_name=false ;;
        esac
    fi

    if [ "$current_email" != "$gitemail" ]; then
        echo -e "\n⚠️  Email differs from current Git configuration."
        read -p "Do you want to override the email (y/n)? " choice
        case $choice in
            y|Y ) update_email=true ;;
            * ) update_email=false ;;
        esac
    fi

    # Update configurations if needed
    success_message=""

    if [ "$update_name" = true ]; then
        git config user.name "$gitname"
        success_message+=" Name: $gitname"
    else
        success_message+=" Name (unchanged): $current_name"
    fi

    if [ "$update_email" = true ]; then
        git config user.email "$gitemail"
        success_message+=" Email: $gitemail"
    fi

    # Output the results
    echo -e "\n\033[32m✅ Git configuration updated:\033[0m"
    echo -e "$success_message"
else
    echo "❌ Error: This directory is not a Git repository."
    echo "Please run this script inside a project folder."
    exit 1
fi
