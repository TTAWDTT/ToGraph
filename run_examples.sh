#!/bin/bash
# Script to run all examples and generate sample outputs

set -e  # Exit on error

echo "ToGraph - Example Runner"
echo "========================"
echo ""

# Create output directory
mkdir -p examples_output

echo "Example 1: Markdown to HTML (Light Theme)"
echo "-----------------------------------------"
python3 -m tograph.main examples/sample.md -o examples_output/markdown_light.html -t light --title "Machine Learning Overview"
echo "✓ Created: examples_output/markdown_light.html"
echo ""

echo "Example 2: Markdown to HTML (Dark Theme)"
echo "----------------------------------------"
python3 -m tograph.main examples/sample.md -o examples_output/markdown_dark.html -t dark --title "Machine Learning Overview"
echo "✓ Created: examples_output/markdown_dark.html"
echo ""

echo "Example 3: Markdown to PNG"
echo "--------------------------"
python3 -m tograph.main examples/sample.md -o examples_output/markdown_graph.png -f png -t light
echo "✓ Created: examples_output/markdown_graph.png"
echo ""

echo "Example 4: Markdown to PDF"
echo "--------------------------"
python3 -m tograph.main examples/sample.md -o examples_output/markdown_graph.pdf -f pdf -t light
echo "✓ Created: examples_output/markdown_graph.pdf"
echo ""

echo "Example 5: PDF to HTML"
echo "----------------------"
if [ ! -f examples/sample_paper.pdf ]; then
    echo "Creating sample PDF..."
    python3 examples/create_sample_pdf.py
fi
python3 -m tograph.main examples/sample_paper.pdf -o examples_output/pdf_graph.html -t light --title "Neural Networks"
echo "✓ Created: examples_output/pdf_graph.html"
echo ""

echo "Example 6: All Formats (Markdown)"
echo "----------------------------------"
python3 -m tograph.main examples/sample.md -o examples_output/all_formats.html -f html png pdf -t dark --title "Complete Export"
echo "✓ Created: examples_output/all_formats.html"
echo "✓ Created: examples_output/all_formats.png"
echo "✓ Created: examples_output/all_formats.pdf"
echo ""

echo "========================"
echo "All examples completed!"
echo "========================"
echo ""
echo "Generated files in examples_output/:"
ls -lh examples_output/
echo ""
echo "Open HTML files in your browser to see interactive graphs!"
