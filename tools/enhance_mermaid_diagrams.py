#!/usr/bin/env python3
"""
Mermaid Diagram Enhancement Script
This script enhances all Mermaid diagrams with better fonts, colors, and readability.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Enhanced color schemes for better readability
COLOR_SCHEMES = {
    "primary": {
        "fill": "#e8f4fd",
        "stroke": "#1976d2",
        "color": "#0d47a1",
        "font_size": "14px",
        "font_weight": "bold",
    },
    "secondary": {
        "fill": "#f3e5f5",
        "stroke": "#7b1fa2",
        "color": "#4a148c",
        "font_size": "13px",
        "font_weight": "bold",
    },
    "success": {
        "fill": "#e8f5e8",
        "stroke": "#388e3c",
        "color": "#1b5e20",
        "font_size": "13px",
        "font_weight": "bold",
    },
    "warning": {
        "fill": "#fff3e0",
        "stroke": "#f57c00",
        "color": "#e65100",
        "font_size": "13px",
        "font_weight": "bold",
    },
    "danger": {
        "fill": "#ffebee",
        "stroke": "#c62828",
        "color": "#b71c1c",
        "font_size": "13px",
        "font_weight": "bold",
    },
    "info": {
        "fill": "#e0f2f1",
        "stroke": "#00695c",
        "color": "#004d40",
        "font_size": "13px",
        "font_weight": "bold",
    },
    "light": {
        "fill": "#fff8e1",
        "stroke": "#fbc02d",
        "color": "#f57f17",
        "font_size": "13px",
        "font_weight": "bold",
    },
}

# Emoji mappings for better visual hierarchy
EMOJI_MAPPINGS = {
    "start": "🚀",
    "end": "🏁",
    "decision": "❓",
    "process": "⚙️",
    "data": "📊",
    "ai": "🤖",
    "ml": "🧠",
    "security": "🔒",
    "cost": "💰",
    "performance": "⚡",
    "quality": "💎",
    "analysis": "🔍",
    "development": "🛠️",
    "testing": "🧪",
    "deployment": "🚀",
    "monitoring": "📈",
    "business": "💼",
    "technical": "🔧",
    "user": "👤",
    "system": "🖥️",
    "network": "🌐",
    "database": "🗄️",
    "api": "🔌",
    "model": "🎯",
    "training": "🏋️",
    "evaluation": "📊",
    "communication": "📢",
    "impact": "💼",
}


def add_emojis_to_text(text: str) -> str:
    """Add relevant emojis to text based on keywords."""
    text_lower = text.lower()

    for keyword, emoji in EMOJI_MAPPINGS.items():
        if keyword in text_lower:
            # Add emoji at the beginning if not already present
            if not any(e in text for e in EMOJI_MAPPINGS.values()):
                text = f"{emoji} {text}"
            break

    return text


def enhance_node_styling(content: str) -> str:
    """Enhance node styling with better colors and fonts."""

    # Add enhanced class definitions
    enhanced_classes = []
    for i, (name, scheme) in enumerate(COLOR_SCHEMES.items()):
        enhanced_classes.append(
            f"classDef {name} fill:{scheme['fill']},stroke:{scheme['stroke']},"
            f"stroke-width:3px,color:{scheme['color']},"
            f"font-size:{scheme['font_size']},font-weight:{scheme['font_weight']}"
        )

    # Find existing classDef lines and replace them
    lines = content.split("\n")
    enhanced_lines = []
    class_def_found = False

    for line in lines:
        if line.strip().startswith("classDef"):
            if not class_def_found:
                # Add enhanced class definitions
                enhanced_lines.extend(enhanced_classes)
                class_def_found = True
            # Skip original classDef lines
            continue
        enhanced_lines.append(line)

    if not class_def_found:
        # Add enhanced class definitions at the end
        enhanced_lines.extend([""] + enhanced_classes)

    return "\n".join(enhanced_lines)


def enhance_node_labels(content: str) -> str:
    """Enhance node labels with emojis and better formatting."""

    # Pattern to match node definitions like A[text] or A["text"]
    node_pattern = r"(\w+)\[([^]]+)\]"

    def enhance_node(match):
        node_id = match.group(1)
        node_text = match.group(2)

        # Remove quotes if present
        if node_text.startswith('"') and node_text.endswith('"'):
            node_text = node_text[1:-1]

        # Add emojis and enhance formatting
        enhanced_text = add_emojis_to_text(node_text)

        # Add line breaks for better readability if text is long
        if len(enhanced_text) > 30 and "<br/>" not in enhanced_text:
            words = enhanced_text.split()
            if len(words) > 3:
                mid = len(words) // 2
                enhanced_text = " ".join(words[:mid]) + "<br/>" + " ".join(words[mid:])

        return f'{node_id}["{enhanced_text}"]'

    return re.sub(node_pattern, enhance_node, content)


def enhance_subgraph_labels(content: str) -> str:
    """Enhance subgraph labels with emojis."""

    # Pattern to match subgraph definitions
    subgraph_pattern = r'subgraph\s+"([^"]+)"'

    def enhance_subgraph(match):
        label = match.group(1)
        enhanced_label = add_emojis_to_text(label)
        return f'subgraph "{enhanced_label}"'

    return re.sub(subgraph_pattern, enhance_subgraph, content)


def enhance_diagram(content: str, filename: str) -> str:
    """Enhance a Mermaid diagram with better styling."""

    print(f"🎨 Enhancing: {filename}")

    # Add enhancement comment
    enhanced_content = f"%% Enhanced {filename} with better fonts and colors\n"
    enhanced_content += f"%% Generated by enhance_mermaid_diagrams.py\n\n"
    enhanced_content += content

    # Apply enhancements
    enhanced_content = enhance_node_labels(enhanced_content)
    enhanced_content = enhance_subgraph_labels(enhanced_content)
    enhanced_content = enhance_node_styling(enhanced_content)

    return enhanced_content


def process_all_diagrams():
    """Process all Mermaid diagrams in the extracted_diagrams directory."""

    diagram_dir = Path("extracted_diagrams")
    mmd_files = list(diagram_dir.glob("*.mmd"))

    print("🎨 Mermaid Diagram Enhancement")
    print("=" * 50)
    print(f"Found {len(mmd_files)} diagrams to enhance")

    enhanced_count = 0
    errors = []

    for file_path in mmd_files:
        try:
            # Read original content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip if already enhanced
            if "Enhanced" in content and "enhance_mermaid_diagrams.py" in content:
                print(f"⏭️  Skipping already enhanced: {file_path.name}")
                continue

            # Enhance the diagram
            enhanced_content = enhance_diagram(content, file_path.name)

            # Create enhanced version
            enhanced_path = file_path.parent / f"{file_path.stem}_enhanced.mmd"
            with open(enhanced_path, "w", encoding="utf-8") as f:
                f.write(enhanced_content)

            enhanced_count += 1
            print(f"✅ Enhanced: {file_path.name} -> {enhanced_path.name}")

        except Exception as e:
            error_msg = f"Error enhancing {file_path.name}: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")

    # Summary
    print(f"\n📊 Enhancement Summary:")
    print(f"   Total diagrams: {len(mmd_files)}")
    print(f"   Enhanced: {enhanced_count}")
    print(f"   Errors: {len(errors)}")

    if errors:
        print(f"\n❌ Errors encountered:")
        for error in errors:
            print(f"   - {error}")

    return enhanced_count, errors


def create_enhancement_report():
    """Create a report of the enhancement process."""

    diagram_dir = Path("extracted_diagrams")
    enhanced_files = list(diagram_dir.glob("*_enhanced.mmd"))

    report = {
        "enhanced_diagrams": [f.name for f in enhanced_files],
        "enhancement_features": {
            "emojis": "Added relevant emojis for better visual hierarchy",
            "colors": "Enhanced color schemes for better contrast and readability",
            "fonts": "Improved font sizes and weights for better legibility",
            "formatting": "Added line breaks and better text formatting",
        },
        "color_schemes": COLOR_SCHEMES,
        "emoji_mappings": EMOJI_MAPPINGS,
    }

    with open("mermaid_enhancement_report.json", "w", encoding="utf-8") as f:
        import json

        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Enhancement report saved to: mermaid_enhancement_report.json")


if __name__ == "__main__":
    enhanced_count, errors = process_all_diagrams()
    create_enhancement_report()

    if enhanced_count > 0:
        print(f"\n🎉 Successfully enhanced {enhanced_count} diagrams!")
        print(f"   Enhanced diagrams have '_enhanced' suffix")
        print(f"   Original diagrams are preserved")
    else:
        print(f"\n⚠️  No diagrams were enhanced")
