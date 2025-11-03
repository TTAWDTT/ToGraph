#!/bin/bash
# Test script to verify ToGraph installation

echo "ToGraph Installation Test"
echo "========================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
echo ""

# Check if tograph is installed
run_test "tograph command availability" "which tograph"

# Check if Python module can be imported
run_test "Python module import" "python3 -c 'import tograph'"

# Check dependencies
run_test "pdfplumber installed" "python3 -c 'import pdfplumber'"
run_test "markdown installed" "python3 -c 'import markdown'"
run_test "networkx installed" "python3 -c 'import networkx'"
run_test "pyvis installed" "python3 -c 'import pyvis'"
run_test "matplotlib installed" "python3 -c 'import matplotlib'"
run_test "reportlab installed" "python3 -c 'import reportlab'"

# Check if example files exist
run_test "Example markdown file exists" "test -f examples/sample.md"
run_test "Example PDF generator exists" "test -f examples/create_sample_pdf.py"

# Test basic functionality
echo ""
echo "Running functional tests..."
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"
echo ""

# Test 1: Markdown to HTML
run_test "Convert Markdown to HTML" \
    "tograph examples/sample.md -o $TEMP_DIR/test1.html -t light --title 'Test'"

# Test 2: Markdown to PNG
run_test "Convert Markdown to PNG" \
    "tograph examples/sample.md -o $TEMP_DIR/test2.png -f png"

# Test 3: Check help
run_test "Help command works" \
    "tograph --help"

# Test 4: Error handling (non-existent file)
if tograph nonexistent.md -o $TEMP_DIR/test.html 2>&1 | grep -q "not found"; then
    echo -n "Testing: Error handling for missing file... "
    echo -e "${GREEN}PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -n "Testing: Error handling for missing file... "
    echo -e "${RED}FAILED${NC}"
    ((TESTS_FAILED++))
fi

# Cleanup
rm -rf "$TEMP_DIR"

# Summary
echo ""
echo "========================="
echo "Test Summary"
echo "========================="
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! ToGraph is properly installed.${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check the installation.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Make sure all dependencies are installed: pip install -r requirements.txt"
    echo "2. Install the package: pip install -e ."
    echo "3. Check Python version (3.8+ required)"
    exit 1
fi
