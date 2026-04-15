#!/bin/bash

# Define the Ollama API base URL
export OLLAMA_API_BASE=http://localhost:11434

# Check if Ollama service is running
echo "Checking Ollama service status..."
if ! curl --silent http://localhost:11434; then
    echo -e "\n❌ Error: Ollama service not found. Please ensure Ollama is running."
    exit 1
fi

# Ensure the best models for the job are ready
echo "Ensuring optimal models are available..."
ollama pull deepseek-r1:32b || { echo "Failed to pull DeepSeek-R1 model"; exit 1; }
ollama pull qwen2.5-coder:32b || { echo "Failed to pull Qwen2.5-Coder model"; exit 1; }

# Architect Mode Configuration:
# - Architect: DeepSeek-R1 (32B) for high-level reasoning and logic.
# - Editor: Qwen2.5-Coder (32B) for precise code implementation.

aider \
  --model ollama_chat/deepseek-r1:32b \
  --editor-model ollama_chat/qwen2.5-coder:32b \
  --architect \
  --map-tokens 2048 \
  --cache-prompts \
  --no-stream \
  --dark-mode \
  --suggest-shell-commands
