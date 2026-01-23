#!/bin/bash

# Script để chạy admin tests
# Usage: bash run_tests.sh

echo "🧪 Running Admin Module Tests..."
echo "================================"
echo ""

# Set PYTHONPATH to include project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
python3 tests/test_admin.py

echo ""
echo "Tests completed!"
