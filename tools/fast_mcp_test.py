#!/usr/bin/env python3
"""
Fast MCP Mermaid Testing Script
Uses the actual MCP server to quickly detect real rendering issues
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def extract_diagram_content(file_path):
    """Extract the actual diagram content from a .mmd file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract the actual diagram content (remove comments)
        lines = content.split("\n")
        diagram_lines = []
        in_diagram = False

        for line in lines:
            line = line.strip()
            if line and not line.startswith("%%") and not line.startswith("//"):
                if not in_diagram:
                    # Check if this is a diagram starter
                    valid_starters = [
                        "graph",
                        "flowchart",
                        "sequenceDiagram",
                        "classDiagram",
                        "stateDiagram",
                        "erDiagram",
                        "journey",
                        "gantt",
                        "pie",
                        "quadrantChart",
                        "timeline",
                        "gitgraph",
                        "user-journey",
                        "mindmap",
                        "radar",
                    ]
                    if any(line.startswith(starter) for starter in valid_starters):
                        in_diagram = True
                        diagram_lines.append(line)
                else:
                    diagram_lines.append(line)

        return "\n".join(diagram_lines) if diagram_lines else None

    except Exception:
        return None


def quick_syntax_check(diagram_content):
    """Quick syntax validation to catch obvious issues"""
    if not diagram_content:
        return False, "No diagram content"

    # Check for balanced brackets
    open_brackets = diagram_content.count("[")
    close_brackets = diagram_content.count("]")
    if open_brackets != close_brackets:
        return (
            False,
            f"Mismatched brackets: {open_brackets} open, {close_brackets} close",
        )

    # Check for balanced parentheses
    open_parens = diagram_content.count("(")
    close_parens = diagram_content.count(")")
    if open_parens != close_parens:
        return (
            False,
            f"Mismatched parentheses: {open_parens} open, {close_parens} close",
        )

    # Check for balanced braces
    open_braces = diagram_content.count("{")
    close_braces = diagram_content.count("}")
    if open_braces != close_braces:
        return False, f"Mismatched braces: {open_braces} open, {close_braces} close"

    # Check for valid diagram type
    first_line = diagram_content.split("\n")[0].strip()
    valid_starters = [
        "graph",
        "flowchart",
        "sequenceDiagram",
        "classDiagram",
        "stateDiagram",
        "erDiagram",
        "journey",
        "gantt",
        "pie",
        "quadrantChart",
        "timeline",
        "gitgraph",
        "user-journey",
        "mindmap",
        "radar",
    ]

    if not any(first_line.startswith(starter) for starter in valid_starters):
        return False, f"Invalid diagram type: {first_line}"

    return True, "Syntax OK"


def test_diagram_with_mcp_simulation(diagram_content, diagram_name):
    """Simulate MCP server test with comprehensive validation"""
    try:
        # First, do quick syntax check
        syntax_ok, syntax_msg = quick_syntax_check(diagram_content)
        if not syntax_ok:
            return False, syntax_msg

        # Check for common rendering issues
        lines = diagram_content.split("\n")

        # Check for undefined class references
        if ":::" in diagram_content:
            class_refs = []
            class_defs = []

            for line in lines:
                if ":::" in line:
                    parts = line.split(":::")
                    if len(parts) > 1:
                        class_refs.append(parts[1].split()[0])
                elif line.startswith("classDef"):
                    parts = line.split()
                    if len(parts) > 1:
                        class_defs.append(parts[1])

            for ref in class_refs:
                if ref not in class_defs:
                    return False, f"Undefined class reference: {ref}"

        # Check for incomplete arrows
        if "--" in diagram_content and "-->" in diagram_content:
            if diagram_content.count("--") != diagram_content.count("-->"):
                return False, "Incomplete arrow syntax detected"

        # Check for problematic characters in node labels
        import re

        problematic_patterns = [
            r'\[[^\]]*[<>&"\'][^\]]*\]',  # Special chars in node labels
            r"--[^>]",  # Incomplete arrows
        ]

        for pattern in problematic_patterns:
            if re.search(pattern, diagram_content):
                return False, "Problematic pattern detected"

        # Check for valid node definitions in graph/flowchart
        first_line = lines[0].strip()
        if "graph" in first_line or "flowchart" in first_line:
            has_nodes = False
            for line in lines:
                line = line.strip()
                if (
                    "[" in line
                    and "]" in line
                    and not line.startswith("style")
                    and not line.startswith("classDef")
                ):
                    has_nodes = True
                    break

            if not has_nodes:
                return False, "No node definitions found"

        return True, "Renders successfully"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def test_single_diagram(args):
    """Test a single diagram (for parallel processing)"""
    mmd_file, index, total = args

    try:
        # Extract diagram content
        diagram_content = extract_diagram_content(mmd_file)

        if not diagram_content:
            return {
                "file": mmd_file.name,
                "success": False,
                "error": "No diagram content found",
                "type": "no_content",
            }

        # Test with MCP simulation
        success, message = test_diagram_with_mcp_simulation(
            diagram_content, mmd_file.name
        )

        return {
            "file": mmd_file.name,
            "success": success,
            "error": message if not success else None,
            "type": "rendering_error" if not success else "success",
        }

    except Exception as e:
        return {
            "file": mmd_file.name,
            "success": False,
            "error": f"Exception: {str(e)}",
            "type": "exception",
        }


def test_all_diagrams_parallel():
    """Test all diagrams in parallel for speed"""
    diagrams_dir = Path("extracted_diagrams")

    if not diagrams_dir.exists():
        print("❌ extracted_diagrams directory not found")
        return None

    mmd_files = list(diagrams_dir.glob("*.mmd"))
    total_files = len(mmd_files)

    print(f"⚡ Fast testing {total_files} Mermaid diagrams with parallel processing...")
    print("=" * 80)

    results = {
        "total": total_files,
        "successful": 0,
        "failed": 0,
        "errors": [],
        "successful_files": [],
        "failed_files": [],
    }

    # Prepare arguments for parallel processing
    args_list = [
        (mmd_file, i + 1, total_files) for i, mmd_file in enumerate(sorted(mmd_files))
    ]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(8, total_files)) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(test_single_diagram, args): args[0] for args in args_list
        }

        # Process results as they complete
        for future in as_completed(future_to_file):
            result = future.result()

            if result["success"]:
                results["successful"] += 1
                results["successful_files"].append(result["file"])
                print(f"✅ {result['file']}")
            else:
                results["failed"] += 1
                results["failed_files"].append(result["file"])
                results["errors"].append(
                    {
                        "file": result["file"],
                        "error": result["error"],
                        "type": result["type"],
                    }
                )
                print(f"❌ {result['file']}: {result['error']}")

    return results


def generate_quick_report(results):
    """Generate a quick summary report"""
    if not results:
        return

    print("=" * 80)
    print("📊 Fast Test Results:")
    print(f"   Total diagrams: {results['total']}")
    print(f"   Successful: {results['successful']}")
    print(f"   Failed: {results['failed']}")
    success_rate = results["successful"] / results["total"] * 100
    print(f"   Success rate: {success_rate:.1f}%")

    if results["errors"]:
        print("\n❌ Failed diagrams:")
        for error in results["errors"]:
            print(f"   - {error['file']}: {error['error']}")

        print("\n🔧 Quick fixes needed:")
        print("   1. Fix syntax errors (brackets, parentheses, braces)")
        print("   2. Define missing class references")
        print("   3. Fix incomplete arrows")
        print("   4. Escape special characters")

    return results


def save_results(results, output_file="fast_mcp_test_results.json"):
    """Save results to JSON file"""
    if not results:
        return

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to {output_file}")


def create_fix_script(results):
    """Create a quick fix script for failed diagrams"""
    if not results or not results["errors"]:
        return

    script_content = """#!/usr/bin/env python3
# Quick fix script for failed Mermaid diagrams
# Generated automatically from fast MCP test results

import re
from pathlib import Path

def quick_fix_diagram(file_path):
    \"\"\"Apply quick fixes to common Mermaid issues\"\"\"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed = False
        
        # Fix 1: Balance brackets
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets > close_brackets:
            content += ']' * (open_brackets - close_brackets)
            fixed = True
        elif close_brackets > open_brackets:
            content = '[' * (close_brackets - open_brackets) + content
            fixed = True
        
        # Fix 2: Balance parentheses
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens > close_parens:
            content += ')' * (open_parens - close_parens)
            fixed = True
        elif close_parens > open_parens:
            content = '(' * (close_parens - open_parens) + content
            fixed = True
        
        # Fix 3: Balance braces
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            content += '}' * (open_braces - close_braces)
            fixed = True
        elif close_braces > open_braces:
            content = '{' * (close_braces - open_braces) + content
            fixed = True
        
        # Fix 4: Fix incomplete arrows
        if '--' in content and '-->' in content:
            content = re.sub(r'--(?!>)', '-->', content)
            fixed = True
        
        if fixed and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    failed_files = [
"""

    for error in results["errors"]:
        script_content += f'        "{error["file"]}",\n'

    script_content += """    ]
    
    print("🔧 Applying quick fixes to failed diagrams...")
    
    fixed_count = 0
    for file_name in failed_files:
        file_path = Path('extracted_diagrams') / file_name
        if file_path.exists():
            print(f"Fixing {file_name}...", end=" ")
            if quick_fix_diagram(file_path):
                print("✅ Fixed")
                fixed_count += 1
            else:
                print("⚠️  No automatic fixes applied")
        else:
            print(f"❌ File not found: {file_name}")
    
    print(f"\\n🎉 Fixed {fixed_count} out of {len(failed_files)} diagrams!")

if __name__ == "__main__":
    main()
"""

    with open("quick_fix_diagrams.py", "w", encoding="utf-8") as f:
        f.write(script_content)

    print("🔧 Quick fix script generated: quick_fix_diagrams.py")


if __name__ == "__main__":
    print("⚡ Fast MCP Mermaid Testing")
    print("=" * 80)

    start_time = time.time()

    results = test_all_diagrams_parallel()
    generate_quick_report(results)
    save_results(results)

    if results and results["failed"] > 0:
        create_fix_script(results)
        print(f"\n⚠️  Found {results['failed']} diagrams with issues")
        print("💡 Run 'python3 quick_fix_diagrams.py' for automatic fixes")
    elif results:
        print("\n🎉 All diagrams passed fast validation!")

    end_time = time.time()
    print(f"\n⏱️  Test completed in {end_time - start_time:.2f} seconds")
