#!/usr/bin/env python3
"""
ReviewResults Splitter Script for v25R2

This script parses the ReviewResults.md file and splits it by main header sections,
using the VaultAPIDocs sections as an authoritative anchor for alignment.
It creates files that match the API documentation structure and reports discrepancies.

Author: VeevaTools Development Team
Date: August 30, 2025
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set

def load_api_sections_as_anchor(api_sections_dir: Path) -> Dict[str, str]:
    """
    Load API sections as the authoritative anchor for section naming and ordering.
    
    Args:
        api_sections_dir: Path to the API sections directory
    
    Returns:
        Dictionary mapping normalized section titles to API filenames
    """
    api_anchor = {}
    
    if not api_sections_dir.exists():
        print(f"⚠️  Warning: API sections directory not found: {api_sections_dir}")
        return api_anchor
    
    for file_path in api_sections_dir.glob("*.md"):
        if file_path.name == "README.md":
            continue
            
        # Read the first few lines to get the section title
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # Read first 500 chars to get header
                
            # Extract the main header (# Section Name)
            header_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if header_match:
                section_title = header_match.group(1).strip()
                # Normalize the title for matching
                normalized_title = normalize_section_title(section_title)
                api_anchor[normalized_title] = file_path.name
                
        except Exception as e:
            print(f"⚠️  Warning: Could not read {file_path.name}: {e}")
    
    return api_anchor

def normalize_section_title(title: str) -> str:
    """
    Normalize section titles for consistent matching.
    
    Args:
        title: Raw section title
    
    Returns:
        Normalized title for comparison
    """
    # Remove markdown markers and clean
    clean_title = re.sub(r'^#+\s*', '', title.strip())
    
    # Convert to lowercase and remove special characters for comparison
    normalized = re.sub(r'[^\w\s]', '', clean_title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def extract_review_sections(markdown_content: str) -> Dict[str, Tuple[str, str, int]]:
    """
    Extract sections from review results markdown content.
    
    Args:
        markdown_content: The full markdown content
    
    Returns:
        Dictionary mapping normalized titles to (original_title, content, line_number)
    """
    lines = markdown_content.split('\n')
    sections = {}
    current_section = None
    current_content = []
    current_normalized = None
    
    for line_num, line in enumerate(lines, 1):
        # Check if this is a main header (starts with exactly two ##)
        if re.match(r'^## [^#]', line):
            # Save the previous section if it exists
            if current_section is not None and current_normalized:
                section_content = '\n'.join(current_content).strip()
                sections[current_normalized] = (current_section, section_content, section_start_line)
            
            # Start new section
            current_section = line
            section_start_line = line_num
            current_content = [line]
            current_normalized = normalize_section_title(line)
        else:
            # Add to current section content
            if current_section is not None:
                current_content.append(line)
    
    # Don't forget the last section
    if current_section is not None and current_normalized:
        section_content = '\n'.join(current_content).strip()
        sections[current_normalized] = (current_section, section_content, section_start_line)
    
    return sections

def create_aligned_files(review_sections: Dict[str, Tuple[str, str, int]], 
                        api_anchor: Dict[str, str], 
                        output_dir: Path) -> Tuple[Dict[str, str], List[str], List[str]]:
    """
    Create review files aligned with API documentation structure.
    
    Args:
        review_sections: Dictionary of review sections
        api_anchor: Dictionary mapping normalized titles to API filenames
        output_dir: Directory to save files
    
    Returns:
        Tuple of (created_files, missing_reviews, extra_reviews)
    """
    created_files = {}
    missing_reviews = []
    extra_reviews = []
    
    # Create files for API sections that have reviews
    for normalized_title, api_filename in api_anchor.items():
        if normalized_title in review_sections:
            original_title, content, line_num = review_sections[normalized_title]
            
            # Use the API filename for consistency
            file_path = output_dir / api_filename
            
            # Add metadata header
            file_content = f"""<!-- 
ReviewResults Section: {original_title.strip()}
API Section Match: {api_filename}
Original Line Number: {line_num}
API Version: v25R2
Generated: August 30, 2025
-->

{content}
"""
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            created_files[original_title.strip()] = api_filename
            print(f"✅ Created (aligned): {api_filename}")
        else:
            missing_reviews.append(api_filename)
            print(f"❌ Missing review: {api_filename}")
    
    # Identify review sections without corresponding API sections
    for normalized_title, (original_title, content, line_num) in review_sections.items():
        if normalized_title not in api_anchor:
            # Create a review-only file with 'r_' prefix
            safe_title = re.sub(r'[^\w\s\-]', '', original_title.replace('## ', '').strip())
            safe_title = re.sub(r'[\s\-]+', '_', safe_title).lower().strip('_')
            filename = f"r_{safe_title}.md"
            
            file_path = output_dir / filename
            
            file_content = f"""<!-- 
ReviewResults Section: {original_title.strip()}
API Section Match: NONE (Review-only section)
Original Line Number: {line_num}
API Version: v25R2
Generated: August 30, 2025
-->

{content}
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            created_files[original_title.strip()] = filename
            extra_reviews.append(filename)
            print(f"⚠️  Created (review-only): {filename}")
    
    return created_files, missing_reviews, extra_reviews

def create_discrepancy_report(missing_reviews: List[str], 
                             extra_reviews: List[str], 
                             api_anchor: Dict[str, str],
                             created_files: Dict[str, str],
                             output_dir: Path) -> None:
    """
    Create a detailed discrepancy report between API docs and review results.
    """
    total_api_sections = len(api_anchor)
    total_review_sections = len(created_files)
    aligned_sections = total_api_sections - len(missing_reviews)
    
    report_content = f"""# API Documentation vs Review Results Discrepancy Report

**API Version:** v25R2  
**Generated:** August 30, 2025  

## Executive Summary

- **Total API Sections**: {total_api_sections}
- **Total Review Sections**: {total_review_sections}
- **Aligned Sections**: {aligned_sections}
- **Missing Reviews**: {len(missing_reviews)}
- **Extra Review Sections**: {len(extra_reviews)}
- **Alignment Rate**: {(aligned_sections / total_api_sections * 100):.1f}%

## ✅ Successfully Aligned Sections ({aligned_sections})

These sections have corresponding reviews and are properly aligned:

"""
    
    # List aligned sections
    aligned_files = [filename for filename in created_files.values() if not filename.startswith('r_')]
    for filename in sorted(aligned_files):
        section_name = filename.replace('.md', '').replace('_', ' ').title()
        report_content += f"- `{filename}` - {section_name}\n"
    
    if missing_reviews:
        report_content += f"""
## ❌ Missing Reviews ({len(missing_reviews)})

These API sections exist but have no corresponding review results:

"""
        for filename in sorted(missing_reviews):
            section_name = filename.replace('.md', '').replace('_', ' ').title()
            report_content += f"- `{filename}` - **{section_name}** ⚠️ *Requires Review*\n"
    
    if extra_reviews:
        report_content += f"""
## 📝 Extra Review Sections ({len(extra_reviews)})

These review sections don't have corresponding API documentation:

"""
        for filename in sorted(extra_reviews):
            section_name = filename.replace('r_', '').replace('.md', '').replace('_', ' ').title()
            report_content += f"- `{filename}` - **{section_name}** (Implementation-specific)\n"
    
    # Recommendations section
    report_content += """
## 📋 Action Items

"""
    
    if missing_reviews:
        report_content += f"""
### High Priority - Missing Reviews ({len(missing_reviews)} items)

The following API sections require review implementation:

"""
        for i, filename in enumerate(sorted(missing_reviews), 1):
            section_name = filename.replace('.md', '').replace('_', ' ').title()
            report_content += f"{i}. **{section_name}** (`{filename}`)\n"
        
        report_content += """
**Recommended Actions:**
- Create review entries for each missing section
- Validate API implementation against documentation
- Update test coverage for these areas
- Document any implementation decisions

"""
    
    if extra_reviews:
        report_content += f"""
### Medium Priority - Review-Only Sections ({len(extra_reviews)} items)

These sections may represent:
- Implementation-specific features
- Custom extensions
- Legacy functionality
- Documentation gaps

**Recommended Actions:**
- Verify if these should be in API documentation
- Consider if they represent custom implementations
- Document the purpose of each extra section

"""
    
    if aligned_sections == total_api_sections and len(extra_reviews) == 0:
        report_content += """
### ✅ Perfect Alignment Achieved!

All API sections have corresponding reviews and no extra sections exist.
The documentation and review process are perfectly synchronized.

"""
    
    report_content += f"""
## 📊 Quality Metrics

- **Completeness**: {(aligned_sections / total_api_sections * 100):.1f}% of API sections reviewed
- **Coverage Gaps**: {len(missing_reviews)} sections need attention
- **Extra Work**: {len(extra_reviews)} non-API sections reviewed
- **Overall Health**: {'🟢 Excellent' if aligned_sections / total_api_sections > 0.9 else '🟡 Good' if aligned_sections / total_api_sections > 0.7 else '🔴 Needs Improvement'}

## 🔄 Process Improvements

1. **Automated Sync**: Use this script after API doc updates
2. **Review Templates**: Create templates for missing sections
3. **Validation Pipeline**: Integrate alignment checks in CI/CD
4. **Documentation Standards**: Ensure consistent section naming

---

*This report was generated automatically using VaultAPIDocs sections as the authoritative anchor.*
*Report location: `{output_dir}/discrepancy_report.md`*
"""
    
    report_path = output_dir / "discrepancy_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📊 Created discrepancy report: discrepancy_report.md")

def create_index_file(created_files: Dict[str, str], 
                     missing_reviews: List[str], 
                     extra_reviews: List[str], 
                     output_dir: Path) -> None:
    """
    Create an index file for the review results.
    """
    total_files = len(created_files)
    aligned_files = [f for f in created_files.values() if not f.startswith('r_')]
    
    index_content = f"""# Review Results Index - v25R2

This directory contains review results split and aligned with VaultAPIDocs sections.

## 📊 Summary

- **Total Files**: {total_files}
- **API-Aligned Files**: {len(aligned_files)}
- **Review-Only Files**: {len(extra_reviews)}
- **Missing Reviews**: {len(missing_reviews)}

## 📁 Generated Files

### ✅ API-Aligned Reviews
"""
    
    # List API-aligned files
    for filename in sorted(aligned_files):
        section_name = filename.replace('.md', '').replace('_', ' ').title()
        index_content += f"- **[{section_name}](./{filename})**\n"
    
    if extra_reviews:
        index_content += f"""
### 📝 Review-Only Sections
"""
        for filename in sorted(extra_reviews):
            section_name = filename.replace('r_', '').replace('.md', '').replace('_', ' ').title()
            index_content += f"- **[{section_name}](./{filename})** (Implementation-specific)\n"
    
    index_content += f"""
## 📋 Related Files

- **[Discrepancy Report](./discrepancy_report.md)** - Detailed alignment analysis
- **[Original File](./ReviewResults.md)** - Source review results
- **[API Sections](../../sections/)** - API documentation sections

## 🔍 File Structure

- Files matching API docs use the same naming (e.g., `01_authentication.md`)
- Review-only files have `r_` prefix (e.g., `r_custom_feature.md`)
- All files include metadata headers with alignment information

## 📈 Usage

1. **Find Reviews**: Use API section names to locate corresponding review files
2. **Check Coverage**: Review the discrepancy report for missing items
3. **Validate Changes**: Ensure API updates trigger review updates
4. **Track Progress**: Monitor alignment rate over time

---

**Generated**: August 30, 2025  
**Script**: `split_review_results.py`  
**Anchor**: VaultAPIDocs sections  
"""
    
    index_path = output_dir / "README.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Created index file: README.md")

def main():
    """Main function to execute the splitting process."""
    print("🔧 ReviewResults Splitter Script - v25R2 (API-Anchored)")
    print("=" * 60)
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Input file path
    input_file = script_dir / "ReviewResults.md"
    
    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Error: ReviewResults.md not found in {script_dir}")
        print("   Please ensure the file is in the same directory as this script.")
        return 1
    
    # API sections directory for anchor
    api_sections_dir = script_dir.parent.parent / "sections"
    
    print(f"📂 Input file: {input_file}")
    print(f"📂 Output directory: {script_dir}")
    print(f"⚓ API anchor directory: {api_sections_dir}")
    
    try:
        # Load API sections as authoritative anchor
        print("⚓ Loading API sections as anchor...")
        api_anchor = load_api_sections_as_anchor(api_sections_dir)
        print(f"📚 Found {len(api_anchor)} API sections to use as anchor")
        
        if not api_anchor:
            print("❌ Error: No API sections found to use as anchor")
            print("   Please ensure the API docs have been split first")
            return 1
        
        # Read the review results file
        print("📖 Reading ReviewResults.md...")
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"📊 File size: {len(markdown_content):,} characters")
        
        # Extract review sections
        print("🔍 Extracting review sections...")
        review_sections = extract_review_sections(markdown_content)
        
        print(f"📋 Found {len(review_sections)} review sections:")
        for normalized_title, (original_title, _, line_num) in review_sections.items():
            print(f"   - {original_title.strip()} (line {line_num})")
        
        # Create aligned files
        print("\n📝 Creating aligned files...")
        created_files, missing_reviews, extra_reviews = create_aligned_files(
            review_sections, api_anchor, script_dir
        )
        
        # Create discrepancy report
        print("\n📊 Creating discrepancy report...")
        create_discrepancy_report(missing_reviews, extra_reviews, api_anchor, created_files, script_dir)
        
        # Create index file
        print("\n📑 Creating index file...")
        create_index_file(created_files, missing_reviews, extra_reviews, script_dir)
        
        # Summary
        print(f"\n✅ Successfully processed ReviewResults.md!")
        print(f"📂 All files saved to: {script_dir}")
        print(f"📈 Alignment summary:")
        print(f"   - API-aligned files: {len(created_files) - len(extra_reviews)}")
        print(f"   - Review-only files: {len(extra_reviews)}")
        print(f"   - Missing reviews: {len(missing_reviews)}")
        print(f"   - Alignment rate: {((len(api_anchor) - len(missing_reviews)) / len(api_anchor) * 100):.1f}%")
        print(f"📖 See README.md for navigation")
        print(f"📊 See discrepancy_report.md for detailed analysis")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
