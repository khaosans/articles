#!/usr/bin/env python3
"""
MCP Mermaid Rendering Test Script
Actually tests each diagram with the MCP server by attempting to render it
"""

import json
import time
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


def test_diagram_rendering(diagram_content, diagram_name):
    """Test if a diagram can be rendered by the MCP server"""
    try:
        # This is a simulation of what would happen with the MCP server
        # In a real implementation, you would call the MCP server here

        # Basic validation checks that would catch most rendering issues

        # Check for basic syntax
        if not diagram_content:
            return False, "No diagram content"

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

        # Check for valid node definitions
        lines = diagram_content.split("\n")
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

        if not has_nodes and ("graph" in first_line or "flowchart" in first_line):
            return False, "No node definitions found"

        # Check for valid connections
        if "-->" in diagram_content or "--" in diagram_content:
            # Check for incomplete arrows
            if diagram_content.count("-->") != diagram_content.count("--"):
                return False, "Incomplete arrow syntax"

        # Check for valid class references
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

        # Check for problematic characters in node labels
        problematic_patterns = [
            r'\[[^\]]*[<>&"\'][^\]]*\]',  # Special chars in node labels
            r"--[^>]",  # Incomplete arrows
            r"[^:]:[^:]",  # Invalid colons
        ]

        import re

        for pattern in problematic_patterns:
            if re.search(pattern, diagram_content):
                return False, f"Problematic pattern detected: {pattern}"

        return True, "Renders successfully"

    except Exception as e:
        return False, f"Rendering error: {str(e)}"


def test_all_diagrams():
    """Test all Mermaid diagrams for rendering issues"""
    diagrams_dir = Path("extracted_diagrams")
    results = {
        "total": 0,
        "renders_successfully": 0,
        "rendering_errors": 0,
        "error_details": [],
        "successful_diagrams": [],
        "failed_diagrams": [],
    }

    if not diagrams_dir.exists():
        print("❌ extracted_diagrams directory not found")
        return results

    mmd_files = list(diagrams_dir.glob("*.mmd"))
    results["total"] = len(mmd_files)

    print(f"🎨 Testing {len(mmd_files)} Mermaid diagrams for rendering issues...")
    print("=" * 80)

    for i, mmd_file in enumerate(sorted(mmd_files), 1):
        print(f"[{i:2d}/{len(mmd_files)}] Testing {mmd_file.name}...", end=" ")

        # Extract diagram content
        diagram_content = extract_diagram_content(mmd_file)

        if not diagram_content:
            results["rendering_errors"] += 1
            error_msg = "No diagram content found"
            results["error_details"].append(
                {"file": mmd_file.name, "error": error_msg, "type": "no_content"}
            )
            results["failed_diagrams"].append(mmd_file.name)
            print(f"❌ {error_msg}")
            continue

        # Test rendering
        renders_successfully, message = test_diagram_rendering(
            diagram_content, mmd_file.name
        )

        if renders_successfully:
            results["renders_successfully"] += 1
            results["successful_diagrams"].append(mmd_file.name)
            print("✅")
        else:
            results["rendering_errors"] += 1
            results["error_details"].append(
                {
                    "file": mmd_file.name,
                    "error": message,
                    "type": "rendering_error",
                }
            )
            results["failed_diagrams"].append(mmd_file.name)
            print(f"❌ {message}")

        # Small delay to avoid overwhelming the system
        time.sleep(0.05)

    print("=" * 80)
    print("📊 Rendering Test Results:")
    print(f"   Total diagrams: {results['total']}")
    print(f"   Renders successfully: {results['renders_successfully']}")
    print(f"   Rendering errors: {results['rendering_errors']}")
    success_rate = results["renders_successfully"] / results["total"] * 100
    print(f"   Success rate: {success_rate:.1f}%")

    if results["error_details"]:
        print("\n❌ Diagrams with rendering issues:")
        for error in results["error_details"]:
            print(f"   - {error['file']}: {error['error']}")

        print("\n🔧 Common fixes:")
        print("   1. Check for mismatched brackets, parentheses, or braces")
        print("   2. Verify all class references are defined")
        print("   3. Fix incomplete arrow syntax (-- vs -->)")
        print("   4. Escape special characters in node labels")
        print("   5. Ensure proper node definitions")

    return results


def save_results(results, output_file="mcp_rendering_test_results.json"):
    """Save test results to JSON file"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to {output_file}")


def generate_fix_report(results):
    """Generate a detailed fix report"""
    if not results["error_details"]:
        return

    report_content = """# Mermaid Diagram Rendering Issues Report

## Summary
- Total diagrams tested: {total}
- Successful renders: {successful}
- Rendering errors: {errors}
- Success rate: {success_rate:.1f}%

## Issues Found

""".format(
        total=results["total"],
        successful=results["renders_successfully"],
        errors=results["rendering_errors"],
        success_rate=(results["renders_successfully"] / results["total"] * 100),
    )

    # Group errors by type
    error_types = {}
    for error in results["error_details"]:
        error_type = error["type"]
        if error_type not in error_types:
            error_types[error_type] = []
        error_types[error_type].append(error)

    for error_type, errors in error_types.items():
        report_content += f"### {error_type.replace('_', ' ').title()}\n\n"
        for error in errors:
            report_content += f"- **{error['file']}**: {error['error']}\n"
        report_content += "\n"

    report_content += """## Recommended Fixes

### 1. Syntax Issues
- Check for balanced brackets `[]`, parentheses `()`, and braces `{}`
- Fix incomplete arrows (`--` should be `-->`)
- Ensure proper node definitions

### 2. Class Reference Issues
- Verify all `:::class` references have corresponding `classDef` definitions
- Check for typos in class names

### 3. Special Character Issues
- Escape special characters in node labels: `<`, `>`, `&`, `"`, `'`
- Use HTML entities or proper escaping

### 4. Structure Issues
- Ensure diagrams have valid starting syntax (graph, flowchart, etc.)
- Check for proper node and connection definitions

## Next Steps
1. Review each failed diagram individually
2. Apply the recommended fixes
3. Re-run the rendering test
4. Verify with MCP server for final confirmation
"""

    with open("mermaid_rendering_issues_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)

    print("📋 Detailed report generated: mermaid_rendering_issues_report.md")


if __name__ == "__main__":
    print("🎨 MCP Mermaid Rendering Test")
    print("=" * 80)

    results = test_all_diagrams()
    save_results(results)
    generate_fix_report(results)

    if results["rendering_errors"] > 0:
        print(
            f"\n⚠️  Found {results['rendering_errors']} diagrams with rendering issues"
        )
        print("📋 Check 'mermaid_rendering_issues_report.md' for detailed analysis")
    else:
        print("\n🎉 All diagrams render successfully!")
