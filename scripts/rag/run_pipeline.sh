#!/bin/bash
#
# This script orchestrates the execution of the RAG data pipeline.
# It runs a sequence of Python scripts to clean, prepare, and
# create a vector store from the raw ServiceNow data.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Raw data file exported from ServiceNow.
# Note: This file is in .rooignore and should be provided by the user.
INPUT_FILE="docs/servicenow/task.json"

# Directory to store the processed data.
OUTPUT_DIR="docs/servicenow/"

# Intermediate and final file paths.
CLEANED_FILE="${OUTPUT_DIR}task_cleaned.json"
PREPARED_FILE="${OUTPUT_DIR}task_prepared.jsonl"

# Directory to save the FAISS vector store.
VECTOR_STORE_DIR="vector_index/faiss_amarel"


# --- Pipeline Execution ---

# Step 1: Clean the raw data
# This script anonymizes PII, removes redundant text, and normalizes whitespace.
echo "--- Step 1: Cleaning data ---"
python3 scripts/rag/clean_data.py \
    --input-path "$INPUT_FILE" \
    --output-path "$CLEANED_FILE"
echo "--- Cleaning complete ---"
echo

# Step 2: Prepare the data for embedding
# This script combines text fields into a format suitable for the embedding model
# and saves the output as a JSONL file.
echo "--- Step 2: Preparing data ---"
python3 scripts/rag/prepare_data.py \
    --input-path "$CLEANED_FILE" \
    --output-path "$PREPARED_FILE"
echo "--- Preparation complete ---"
echo

# Step 3: Create the vector store
# This script loads the prepared data, generates embeddings, and saves them
# into a FAISS vector store for efficient similarity search.
echo "--- Step 3: Creating vector store ---"
python3 scripts/rag/create_vector_store.py \
    --vector-store faiss \
    --persist-dir "$VECTOR_STORE_DIR" \
    --servicenow-path "$PREPARED_FILE"
echo "--- Vector store creation complete ---"
echo

echo "RAG data pipeline executed successfully!"
echo "Vector store created at: $VECTOR_STORE_DIR"