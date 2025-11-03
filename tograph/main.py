#!/usr/bin/env python3
"""Main CLI interface for ToGraph."""

import argparse
import sys
from pathlib import Path
from .parser import PDFParser, MarkdownParser
from .graph_builder import GraphBuilder
from .visualizer import GraphVisualizer


def main():
    """Main entry point for ToGraph CLI."""
    parser = argparse.ArgumentParser(
        description="Convert PDF and Markdown documents to beautiful knowledge graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDF to HTML with dark theme
  tograph input.pdf -o output.html -t dark
  
  # Convert Markdown to PNG with light theme
  tograph input.md -o output.png -t light
  
  # Convert PDF to all formats
  tograph paper.pdf -o graph.html -f html png pdf
        """
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Input file (PDF or Markdown)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output file path'
    )
    
    parser.add_argument(
        '-f', '--formats',
        type=str,
        nargs='+',
        choices=['html', 'png', 'pdf'],
        default=['html'],
        help='Output formats (default: html)'
    )
    
    parser.add_argument(
        '-t', '--theme',
        type=str,
        choices=['light', 'dark'],
        default='light',
        help='Color theme (default: light)'
    )
    
    parser.add_argument(
        '--title',
        type=str,
        default='Knowledge Graph',
        help='Title for the graph (default: Knowledge Graph)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='DPI for PNG output (default: 300)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1
    
    # Determine file type
    file_ext = input_path.suffix.lower()
    
    try:
        print(f"Processing {input_path.name}...")
        
        # Parse document
        if file_ext == '.pdf':
            print("Parsing PDF document...")
            parser_obj = PDFParser(str(input_path))
            nodes = parser_obj.parse()
            raw_content = '\n'.join([tc['text'] for tc in parser_obj.get_text_content()])
        elif file_ext in ['.md', '.markdown']:
            print("Parsing Markdown document...")
            parser_obj = MarkdownParser(str(input_path))
            nodes = parser_obj.parse()
            raw_content = parser_obj.get_raw_content()
        else:
            print(f"Error: Unsupported file format '{file_ext}'. Use .pdf, .md, or .markdown", 
                  file=sys.stderr)
            return 1
        
        print(f"Extracted {len(nodes)} top-level sections")
        
        # Build graph
        print("Building knowledge graph...")
        builder = GraphBuilder(nodes, raw_content)
        graph = builder.build()
        entity_content = builder.get_entity_content()
        
        print(f"Graph created with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
        
        # Visualize
        visualizer = GraphVisualizer(graph, entity_content)
        
        # Generate outputs
        output_path = Path(args.output)
        base_path = output_path.parent / output_path.stem
        
        for fmt in args.formats:
            print(f"Generating {fmt.upper()} output...")
            
            if fmt == 'html':
                output_file = f"{base_path}.html" if len(args.formats) > 1 else str(output_path)
                visualizer.save_html(output_file, theme=args.theme, title=args.title)
                
            elif fmt == 'png':
                output_file = f"{base_path}.png" if len(args.formats) > 1 else str(output_path)
                visualizer.save_png(output_file, theme=args.theme, dpi=args.dpi)
                
            elif fmt == 'pdf':
                output_file = f"{base_path}.pdf" if len(args.formats) > 1 else str(output_path)
                visualizer.save_pdf(output_file, theme=args.theme)
        
        print("\n✓ Conversion complete!")
        return 0
        
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
