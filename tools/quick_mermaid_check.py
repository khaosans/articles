#!/usr/bin/env python3
"""
Quick Mermaid Diagram Check
A lightweight script to quickly verify Mermaid diagrams are still valid.
"""

from pathlib import Path
import json


def quick_check():
    """Perform a quick check of all Mermaid diagrams."""

    diagram_dir = Path("extracted_diagrams")
    mmd_files = list(diagram_dir.glob("*.mmd"))

    print("🔍 Quick Mermaid Diagram Check")
    print("=" * 40)

    total = len(mmd_files)
    valid = 0
    errors = []

    for file_path in mmd_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            # Basic validation - find the first non-comment line
            lines = content.split("\n")
            first_diagram_line = None

            for line in lines:
                line = line.strip()
                if line and not line.startswith("%%") and not line.startswith("//"):
                    first_diagram_line = line
                    break

            if first_diagram_line and any(
                first_diagram_line.startswith(starter)
                for starter in [
                    "graph",
                    "flowchart",
                    "sequenceDiagram",
                    "classDiagram",
                    "mindmap",
                    "radar",
                    "stateDiagram",
                    "erDiagram",
                    "journey",
                    "gantt",
                    "pie",
                    "quadrantChart",
                ]
            ):
                valid += 1
            else:
                errors.append(f"{file_path.name}: Invalid diagram type")

        except Exception as e:
            errors.append(f"{file_path.name}: {e}")

    # Results
    print(f"📊 Results:")
    print(f"   Total diagrams: {total}")
    print(f"   Valid: {valid}")
    print(f"   Errors: {len(errors)}")
    print(f"   Success rate: {(valid/total*100):.1f}%")

    if errors:
        print(f"\n❌ Errors found:")
        for error in errors:
            print(f"   - {error}")
    else:
        print(f"\n✅ All diagrams are valid!")

    return valid == total


if __name__ == "__main__":
    success = quick_check()
    exit(0 if success else 1)
