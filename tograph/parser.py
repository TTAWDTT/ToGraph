"""Document parsers for PDF and Markdown files."""

import re
from typing import Dict, List, Tuple
from pathlib import Path
import pdfplumber
import markdown
from markdown.extensions import tables, fenced_code
from bs4 import BeautifulSoup


class DocumentNode:
    """Represents a node in the document structure."""
    
    def __init__(self, title: str, level: int, content: str, position: int = 0):
        self.title = title
        self.level = level
        self.content = content
        self.position = position
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def __repr__(self):
        return f"DocumentNode(title='{self.title}', level={self.level}, children={len(self.children)})"


class PDFParser:
    """Parser for PDF documents."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.nodes = []
        self.text_content = []
        
    def parse(self) -> List[DocumentNode]:
        """Parse PDF and extract structured content."""
        with pdfplumber.open(self.file_path) as pdf:
            full_text = []
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text.append(text)
                    self.text_content.append({
                        'page': page_num + 1,
                        'text': text
                    })
            
            combined_text = "\n".join(full_text)
            self.nodes = self._extract_structure(combined_text)
            
        return self.nodes
    
    def _extract_structure(self, text: str) -> List[DocumentNode]:
        """Extract hierarchical structure from text with improved detection."""
        lines = text.split('\n')
        nodes = []
        current_section = None
        current_subsection = None
        current_subsubsection = None
        section_content = []
        position = 0
        
        # Enhanced patterns for detecting headers
        # Match numbered sections: "1.", "1.1", "1.1.1", "Chapter 1", "Section 2.3"
        numbered_pattern = re.compile(r'^(?:Chapter|Section|Part|Article)?\s*(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?\s*[-:]?\s*([A-Z].*)', re.IGNORECASE)
        # Match Roman numerals: "I.", "II.", "III.", etc.
        roman_pattern = re.compile(r'^([IVXLCDM]+)\.\s+([A-Z].*)')
        # Match all-caps or title case headers (improved)
        title_pattern = re.compile(r'^[A-Z][A-Za-z\s\-]+$')
        # Match headers with special formatting
        header_pattern = re.compile(r'^[=\-#*]{2,}$')
        
        prev_line = ''
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if previous line was a header indicator (underline)
            if header_pattern.match(line):
                if prev_line and len(prev_line) > 3:
                    # Previous line was a header
                    if current_section:
                        current_section.content = '\n'.join(section_content)
                        section_content = []
                    
                    node = DocumentNode(prev_line, 1, '', position)
                    position += 1
                    nodes.append(node)
                    current_section = node
                    current_subsection = None
                    current_subsubsection = None
                    prev_line = line
                    continue
            
            # Check for numbered sections
            numbered_match = numbered_pattern.match(line)
            if numbered_match:
                # Save previous section content
                if current_section:
                    if current_subsubsection:
                        current_subsubsection.content = '\n'.join(section_content)
                    elif current_subsection:
                        current_subsection.content = '\n'.join(section_content)
                    else:
                        current_section.content = '\n'.join(section_content)
                    section_content = []
                
                # Determine level based on numbering
                groups = numbered_match.groups()
                level = sum(1 for g in groups[:4] if g is not None)
                title = groups[4].strip()
                
                node = DocumentNode(title, level, '', position)
                position += 1
                
                if level == 1:
                    nodes.append(node)
                    current_section = node
                    current_subsection = None
                    current_subsubsection = None
                elif level == 2 and current_section:
                    current_section.add_child(node)
                    current_subsection = node
                    current_subsubsection = None
                elif level == 3 and current_subsection:
                    current_subsection.add_child(node)
                    current_subsubsection = node
                elif level > 3 and current_subsubsection:
                    current_subsubsection.add_child(node)
                    
            # Check for Roman numeral sections
            elif roman_pattern.match(line):
                roman_match = roman_pattern.match(line)
                if current_section:
                    current_section.content = '\n'.join(section_content)
                    section_content = []
                
                title = roman_match.group(2).strip()
                node = DocumentNode(title, 1, '', position)
                position += 1
                nodes.append(node)
                current_section = node
                current_subsection = None
                current_subsubsection = None
                    
            # Check for title case headers (stricter criteria)
            elif (title_pattern.match(line) and 
                  len(line) > 3 and 
                  len(line.split()) >= 2 and 
                  len(line.split()) <= 8 and
                  not line.endswith('.') and
                  not line.endswith(',') and
                  len(line) < 100):
                # Only treat as header if it looks like a title
                if current_section:
                    if current_subsection:
                        current_subsection.content = '\n'.join(section_content)
                    else:
                        current_section.content = '\n'.join(section_content)
                    section_content = []
                
                node = DocumentNode(line, 2 if current_section else 1, '', position)
                position += 1
                
                if current_section:
                    current_section.add_child(node)
                    current_subsection = node
                    current_subsubsection = None
                else:
                    nodes.append(node)
                    current_section = node
                    current_subsection = None
                    current_subsubsection = None
            else:
                section_content.append(line)
            
            prev_line = line
        
        # Save last section
        if current_section:
            if current_subsubsection:
                current_subsubsection.content = '\n'.join(section_content)
            elif current_subsection:
                current_subsection.content = '\n'.join(section_content)
            else:
                current_section.content = '\n'.join(section_content)
        
        # If no structure found, try to create structure from content
        if not nodes:
            # Try to split by paragraphs and create pseudo-sections
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            if len(paragraphs) > 1:
                for i, para in enumerate(paragraphs[:10]):  # Limit to first 10 paragraphs
                    # Use first line or first 50 chars as title
                    first_line = para.split('\n')[0]
                    title = first_line[:50] + '...' if len(first_line) > 50 else first_line
                    node = DocumentNode(title or f"Section {i+1}", 1, para, i)
                    nodes.append(node)
            else:
                nodes.append(DocumentNode("Document", 1, text, 0))
            
        return nodes
    
    def get_text_content(self) -> List[Dict]:
        """Get the raw text content by page."""
        return self.text_content


class MarkdownParser:
    """Parser for Markdown documents."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.nodes = []
        self.raw_content = ""
        
    def parse(self) -> List[DocumentNode]:
        """Parse Markdown and extract structured content."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_content = f.read()
        
        # Convert to HTML for parsing
        html = markdown.markdown(
            self.raw_content,
            extensions=['extra', 'codehilite', 'toc']
        )
        
        self.nodes = self._extract_structure_from_markdown(self.raw_content)
        return self.nodes
    
    def _extract_structure_from_markdown(self, content: str) -> List[DocumentNode]:
        """Extract hierarchical structure from markdown."""
        lines = content.split('\n')
        nodes = []
        stack = []  # Stack to maintain hierarchy
        current_content = []
        position = 0
        
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        
        for line in lines:
            header_match = header_pattern.match(line)
            
            if header_match:
                # Process accumulated content
                if stack:
                    stack[-1].content = '\n'.join(current_content).strip()
                    current_content = []
                
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                node = DocumentNode(title, level, '', position)
                position += 1
                
                # Pop stack until we find the right parent level
                while stack and stack[-1].level >= level:
                    stack.pop()
                
                # Add to parent or root
                if stack:
                    stack[-1].add_child(node)
                else:
                    nodes.append(node)
                
                stack.append(node)
            else:
                current_content.append(line)
        
        # Process final content
        if stack:
            stack[-1].content = '\n'.join(current_content).strip()
        
        # If no headers found, create a single node
        if not nodes:
            nodes.append(DocumentNode("Document", 1, content, 0))
            
        return nodes
    
    def get_raw_content(self) -> str:
        """Get the raw markdown content."""
        return self.raw_content
