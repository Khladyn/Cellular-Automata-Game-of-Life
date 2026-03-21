#!/bin/bash

# Configuration
NOISE_LEVEL="1e-5"
OUTPUT_DIR="research_output"

echo "Generating Supplement Visualization Screenshots for Research Output..."
echo "Noise Level: $NOISE_LEVEL"
echo "Output Directory: $OUTPUT_DIR"
echo "----------------------------------------------------------------------"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Pattern Classes
PATTERNS=("block" "pulsar" "glider" "gosper_glider_gun")

for PATTERN in "${PATTERNS[@]}"; do
    FILENAME="${OUTPUT_DIR}/viz_screenshot_${PATTERN}.png"
    echo "Processing $PATTERN..."
    python3 main.py --viz --pattern "$PATTERN" --noise "$NOISE_LEVEL" --save "$FILENAME"
done

echo "----------------------------------------------------------------------"
echo "All screenshots generated successfully in $OUTPUT_DIR"
