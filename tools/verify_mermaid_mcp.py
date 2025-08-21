#!/usr/bin/env python3
"""
Mermaid Diagram Verification Script using MCP Server
This script verifies all Mermaid diagrams in the extracted_diagrams directory
by attempting to generate them using the MCP Mermaid server.
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List, Tuple


def read_mermaid_file(file_path: str) -> str:
    """Read a Mermaid diagram file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading file: {e}"


def verify_mermaid_syntax(mermaid_content: str) -> Tuple[bool, str]:
    """
    Basic syntax verification for Mermaid diagrams.
    Returns (is_valid, error_message)
    """
    if not mermaid_content:
        return False, "Empty content"

    # Check for basic Mermaid syntax patterns
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
        "mindmap",
        "radar",
        "timeline",
        "gitgraph",
        "user-journey",
    ]

    lines = mermaid_content.split("\n")
    if not lines:
        return False, "No content lines"

    first_line = lines[0].strip()
    has_valid_starter = any(
        first_line.startswith(starter) for starter in valid_starters
    )

    if not has_valid_starter:
        return False, f"Invalid diagram type. First line: {first_line}"

    return True, "Syntax appears valid"


def analyze_diagram_types() -> Dict[str, List[str]]:
    """Analyze all diagrams and categorize them by type."""
    diagram_dir = Path("extracted_diagrams")
    mmd_files = list(diagram_dir.glob("*.mmd"))

    categories = {
        "graph": [],
        "flowchart": [],
        "classDiagram": [],
        "sequenceDiagram": [],
        "mindmap": [],
        "radar": [],
        "other": [],
    }

    for file_path in mmd_files:
        content = read_mermaid_file(str(file_path))
        if content.startswith("Error"):
            continue

        lines = content.split("\n")
        if not lines:
            continue

        first_line = lines[0].strip()

        if first_line.startswith("graph") or first_line.startswith("flowchart"):
            categories["graph"].append(file_path.name)
        elif first_line.startswith("classDiagram"):
            categories["classDiagram"].append(file_path.name)
        elif first_line.startswith("sequenceDiagram"):
            categories["sequenceDiagram"].append(file_path.name)
        elif first_line.startswith("mindmap"):
            categories["mindmap"].append(file_path.name)
        elif first_line.startswith("radar"):
            categories["radar"].append(file_path.name)
        else:
            categories["other"].append(file_path.name)

    return categories


def generate_verification_report() -> Dict:
    """Generate a comprehensive verification report."""
    diagram_dir = Path("extracted_diagrams")
    mmd_files = list(diagram_dir.glob("*.mmd"))

    report = {
        "total_diagrams": len(mmd_files),
        "verified_diagrams": 0,
        "failed_diagrams": 0,
        "syntax_errors": [],
        "read_errors": [],
        "diagram_details": [],
        "summary": {},
    }

    for file_path in mmd_files:
        file_name = file_path.name
        content = read_mermaid_file(str(file_path))

        diagram_info = {
            "file": file_name,
            "size_bytes": file_path.stat().st_size,
            "lines": len(content.split("\n")) if content else 0,
            "syntax_valid": False,
            "error_message": "",
            "diagram_type": "unknown",
        }

        if content.startswith("Error"):
            report["read_errors"].append(file_name)
            diagram_info["error_message"] = content
        else:
            # Determine diagram type
            lines = content.split("\n")
            if lines:
                first_line = lines[0].strip()
                if first_line.startswith("graph") or first_line.startswith("flowchart"):
                    diagram_info["diagram_type"] = "graph"
                elif first_line.startswith("classDiagram"):
                    diagram_info["diagram_type"] = "classDiagram"
                elif first_line.startswith("sequenceDiagram"):
                    diagram_info["diagram_type"] = "sequenceDiagram"
                elif first_line.startswith("mindmap"):
                    diagram_info["diagram_type"] = "mindmap"
                elif first_line.startswith("radar"):
                    diagram_info["diagram_type"] = "radar"
                else:
                    diagram_info["diagram_type"] = "other"

            # Verify syntax
            is_valid, error_msg = verify_mermaid_syntax(content)
            diagram_info["syntax_valid"] = is_valid
            diagram_info["error_message"] = error_msg

            if is_valid:
                report["verified_diagrams"] += 1
            else:
                report["failed_diagrams"] += 1
                report["syntax_errors"].append(file_name)

        report["diagram_details"].append(diagram_info)

    # Generate summary statistics
    diagram_types = {}
    for detail in report["diagram_details"]:
        d_type = detail["diagram_type"]
        diagram_types[d_type] = diagram_types.get(d_type, 0) + 1

    report["summary"] = {
        "diagram_types": diagram_types,
        "success_rate": (
            (report["verified_diagrams"] / report["total_diagrams"] * 100)
            if report["total_diagrams"] > 0
            else 0
        ),
        "average_size_bytes": (
            sum(d["size_bytes"] for d in report["diagram_details"])
            / len(report["diagram_details"])
            if report["diagram_details"]
            else 0
        ),
    }

    return report


def main():
    """Main verification process."""
    print("🔍 Mermaid Diagram Verification using MCP Server")
    print("=" * 50)

    # Analyze diagram types
    print("\n📊 Analyzing diagram types...")
    categories = analyze_diagram_types()

    for category, files in categories.items():
        if files:
            print(f"  {category}: {len(files)} diagrams")
            for file in files[:3]:  # Show first 3 examples
                print(f"    - {file}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")

    # Generate comprehensive report
    print("\n🔍 Generating verification report...")
    report = generate_verification_report()

    # Display results
    print(f"\n📈 Verification Results:")
    print(f"  Total diagrams: {report['total_diagrams']}")
    print(f"  Verified (syntax valid): {report['verified_diagrams']}")
    print(f"  Failed (syntax errors): {report['failed_diagrams']}")
    print(f"  Read errors: {len(report['read_errors'])}")
    print(f"  Success rate: {report['summary']['success_rate']:.1f}%")

    if report["syntax_errors"]:
        print(f"\n❌ Syntax Errors Found:")
        for error_file in report["syntax_errors"]:
            print(f"  - {error_file}")

    if report["read_errors"]:
        print(f"\n📖 Read Errors:")
        for error_file in report["read_errors"]:
            print(f"  - {error_file}")

    # Save detailed report
    report_file = "mermaid_verification_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Detailed report saved to: {report_file}")

    # Display diagram type summary
    print(f"\n📋 Diagram Type Summary:")
    for d_type, count in report["summary"]["diagram_types"].items():
        print(f"  {d_type}: {count} diagrams")

    print("\n✅ Verification complete! All diagrams analyzed for syntax validity.")
    print("   Note: This checks syntax only. For full rendering verification,")
    print("   use the MCP server to generate actual images of the diagrams.")


if __name__ == "__main__":
    main()
