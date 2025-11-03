# Installation Guide

This guide will help you install and set up ToGraph on your system.

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.8 or higher
- **RAM**: At least 2GB available
- **Disk Space**: At least 500MB for dependencies

## Installation Steps

### Step 1: Install Python

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

#### Windows
Download and install Python from [python.org](https://www.python.org/downloads/)

### Step 2: Clone the Repository

```bash
git clone https://github.com/TTAWDTT/ToGraph.git
cd ToGraph
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- pdfplumber (PDF processing)
- markdown (Markdown parsing)
- networkx (graph algorithms)
- pyvis (interactive visualization)
- matplotlib (static visualization)
- reportlab (PDF generation)
- beautifulsoup4 (HTML parsing)
- And other dependencies

### Step 5: Install ToGraph

```bash
# Install in development mode (editable)
pip install -e .
```

## Verification

Test that the installation was successful:

```bash
# Check if tograph command is available
tograph --help

# Or run directly with Python
python3 -m tograph.main --help
```

You should see the help message with all available options.

## Quick Test

Try converting the example file:

```bash
# Convert sample markdown to HTML
tograph examples/sample.md -o my_first_graph.html

# Open the generated HTML file in your browser
# On Linux:
xdg-open my_first_graph.html

# On macOS:
open my_first_graph.html

# On Windows:
start my_first_graph.html
```

## Troubleshooting

### Issue: "pip: command not found"

Install pip:
```bash
# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade
```

### Issue: "Permission denied" errors

Use virtual environment or add `--user` flag:
```bash
pip install --user -r requirements.txt
```

### Issue: Module import errors

Make sure you're in the correct directory and virtual environment is activated:
```bash
# Check current directory
pwd

# Should show: .../ToGraph

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
```

### Issue: "tograph: command not found"

Run directly with Python:
```bash
python3 -m tograph.main [arguments]
```

Or reinstall:
```bash
pip install -e .
```

### Issue: Weasyprint installation fails (Windows)

WeasyPrint has complex dependencies on Windows. If it fails:

1. The tool will still work for HTML and PNG output
2. PDF generation will use fallback method
3. To fix, follow [WeasyPrint Windows installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)

## Dependencies Explained

- **pdfplumber**: Extracts text and structure from PDF files
- **markdown**: Parses Markdown documents
- **networkx**: Creates and manipulates graph structures
- **pyvis**: Generates interactive HTML visualizations
- **matplotlib**: Creates static PNG visualizations
- **reportlab**: Generates PDF output files
- **beautifulsoup4**: Parses HTML for content extraction
- **pillow**: Image processing library
- **jinja2**: Template engine for HTML generation

## Uninstallation

```bash
# Deactivate virtual environment (if using)
deactivate

# Remove virtual environment
rm -rf venv

# Or uninstall package
pip uninstall tograph
```

## Next Steps

- Read the main [README.md](README.md) for usage examples
- Try the example files in the `examples/` directory
- Check out advanced options with `tograph --help`
