#!/usr/bin/env python3
"""
VaultAPIDocs Splitter Script

This script parses the VaultAPIDocs.md file and splits it by main header sections,
creating separate markdown files for each section with path-safe names.

Author: VeevaTools Development Team
Date: August 30, 2025
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

def create_path_safe_name(section_title: str, index: int) -> str:
    """
    Convert a section title to a path-safe filename.
    
    Args:
        section_title: The section title from the markdown header
        index: The order index of the section
    
    Returns:
        A path-safe filename with leading number
    """
    # Remove the '# ' prefix and clean the title
    clean_title = section_title.replace('# ', '').strip()
    
    # Replace problematic characters with underscores
    safe_title = re.sub(r'[^\w\s\-&]', '', clean_title)
    safe_title = re.sub(r'[\s\-&]+', '_', safe_title)
    safe_title = safe_title.lower().strip('_')
    
    # Handle special cases
    if 'postman' in safe_title:
        safe_title = 'run_in_postman'
    elif 'document_binder_roles' in safe_title:
        safe_title = 'document_and_binder_roles'
    elif 'managing_vault_java_sdk' in safe_title:
        safe_title = 'vault_java_sdk'
    
    # Format with leading zeros for proper ordering
    return f"{index:02d}_{safe_title}.md"

def extract_sections(markdown_content: str) -> List[Tuple[str, str, int]]:
    """
    Extract sections from markdown content based on main headers (# Header).
    Skips the first two sections (API Reference and Run in Postman).
    
    Args:
        markdown_content: The full markdown content
    
    Returns:
        List of tuples containing (section_title, section_content, line_number)
    """
    lines = markdown_content.split('\n')
    sections = []
    current_section = None
    current_content = []
    section_count = 0
    
    for line_num, line in enumerate(lines, 1):
        # Check if this is a main header (starts with exactly one #)
        if re.match(r'^# [^#]', line):
            # Save the previous section if it exists and we're past the first 2 sections
            if current_section is not None and section_count > 2:
                section_content = '\n'.join(current_content).strip()
                sections.append((current_section, section_content, section_start_line))
            
            # Increment section counter
            section_count += 1
            
            # Only start tracking sections after the first 2 (API Reference and Run in Postman)
            if section_count > 2:
                current_section = line
                section_start_line = line_num
                current_content = [line]
            else:
                current_section = None
                current_content = []
        else:
            # Add to current section content only if we're tracking this section
            if current_section is not None:
                current_content.append(line)
    
    # Don't forget the last section
    if current_section is not None:
        section_content = '\n'.join(current_content).strip()
        sections.append((current_section, section_content, section_start_line))
    
    return sections

def create_section_files(sections: List[Tuple[str, str, int]], output_dir: Path) -> Dict[str, str]:
    """
    Create individual markdown files for each section.
    
    Args:
        sections: List of section tuples (title, content, line_number)
        output_dir: Directory to save the section files
    
    Returns:
        Dictionary mapping section titles to created filenames
    """
    created_files = {}
    
    for i, (section_title, section_content, line_num) in enumerate(sections, 1):
        filename = create_path_safe_name(section_title, i)
        file_path = output_dir / filename
        
        # Add metadata header to each file
        file_content = f"""<!-- 
VaultAPIDocs Section: {section_title.strip()}
Original Line Number: {line_num}
Generated: August 30, 2025
Part {i} of {len(sections)}
-->

{section_content}
"""
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        created_files[section_title.strip()] = filename
        print(f"✅ Created: {filename}")
    
    return created_files

def create_index_file(created_files: Dict[str, str], output_dir: Path) -> None:
    """
    Create an index file that lists all the generated section files.
    
    Args:
        created_files: Dictionary mapping section titles to filenames
        output_dir: Directory where files are saved
    """
    index_content = """# VaultAPIDocs Split Index

This directory contains the VaultAPIDocs.md file split into individual sections for easier navigation and maintenance.

**Note**: The first two sections (API Reference and Run in Postman) have been excluded from this split as they are general overview sections.

## Generated Files

"""
    
    for i, (section_title, filename) in enumerate(created_files.items(), 1):
        # Clean section title for display
        display_title = section_title.replace('# ', '')
        index_content += f"{i:2d}. **[{display_title}](./{filename})**\n"
    
    index_content += f"""
## Usage

Each file contains:
- Original section content
- Metadata header with source information
- Proper markdown formatting

## Excluded Sections

The following sections from the original file were intentionally excluded:
1. **API Reference** - General overview section
2. **Run in Postman™** - General setup instructions

## Original File

The complete original file is: `VaultAPIDocs.md`

## Generated Information

- **Total Sections**: {len(created_files)} (of 40 total sections in original file)
- **Excluded Sections**: 2 (API Reference, Run in Postman)
- **Generated**: August 30, 2025
- **Script**: `split_api_docs.py`

---

*This index was automatically generated by the VaultAPIDocs splitter script.*
"""
    
    index_path = output_dir / "README.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Created index file: README.md")

def main():
    """Main function to execute the splitting process."""
    print("🔧 VaultAPIDocs Splitter Script")
    print("=" * 50)
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Input file path
    input_file = script_dir / "VaultAPIDocs.md"
    
    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Error: VaultAPIDocs.md not found in {script_dir}")
        print("   Please ensure the file is in the same directory as this script.")
        return 1
    
    # Create output directory for split files
    output_dir = script_dir / "sections"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📂 Input file: {input_file}")
    print(f"📂 Output directory: {output_dir}")
    
    try:
        # Read the markdown file
        print("📖 Reading VaultAPIDocs.md...")
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"📊 File size: {len(markdown_content):,} characters")
        
        # Extract sections
        print("🔍 Extracting sections (skipping API Reference and Run in Postman)...")
        sections = extract_sections(markdown_content)
        
        print(f"📋 Found {len(sections)} main sections (excluding first 2):")
        for i, (section_title, _, line_num) in enumerate(sections, 1):
            print(f"   {i:2d}. {section_title.strip()} (line {line_num})")
        
        # Create section files
        print("\n📝 Creating section files...")
        created_files = create_section_files(sections, output_dir)
        
        # Create index file
        print("\n📑 Creating index file...")
        create_index_file(created_files, output_dir)
        
        print(f"\n✅ Successfully split VaultAPIDocs.md into {len(sections)} sections (excluding API Reference and Run in Postman)!")
        print(f"📂 All files saved to: {output_dir}")
        print(f"📖 See README.md for navigation index")
        print(f"ℹ️  Note: Skipped sections - API Reference and Run in Postman (first 2 sections)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
