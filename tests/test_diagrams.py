#!/usr/bin/env python3
"""
Tests for Mermaid diagram validation and MCP testing
"""

import pytest
from pathlib import Path
import sys
import os

# Add tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))


def test_mermaid_syntax():
    """Test that all Mermaid diagrams have valid syntax"""
    diagrams_dir = Path("extracted_diagrams")
    assert diagrams_dir.exists(), "extracted_diagrams directory not found"

    mmd_files = list(diagrams_dir.glob("*.mmd"))
    assert len(mmd_files) > 0, "No .mmd files found"

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

    for mmd_file in mmd_files:
        with open(mmd_file, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        first_diagram_line = None

        for line in lines:
            line = line.strip()
            if line and not line.startswith("%%") and not line.startswith("//"):
                first_diagram_line = line
                break

        if first_diagram_line:
            has_valid_starter = any(
                first_diagram_line.startswith(starter) for starter in valid_starters
            )
            assert (
                has_valid_starter
            ), f"Invalid diagram type in {mmd_file.name}: {first_diagram_line}"
        else:
            assert False, f"No valid diagram content found in {mmd_file.name}"


def test_enhanced_diagrams():
    """Test that enhanced diagrams have proper styling"""
    diagrams_dir = Path("extracted_diagrams")
    enhanced_files = list(diagrams_dir.glob("*_enhanced.mmd"))

    for mmd_file in enhanced_files:
        with open(mmd_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for enhanced styling
        assert (
            "classDef" in content
        ), f"Enhanced diagram {mmd_file.name} missing classDef"
        assert (
            "font-size" in content
        ), f"Enhanced diagram {mmd_file.name} missing font-size"
        assert (
            "font-weight" in content
        ), f"Enhanced diagram {mmd_file.name} missing font-weight"


def test_no_duplicate_enhanced():
    """Test that no _enhanced_enhanced.mmd files exist"""
    diagrams_dir = Path("extracted_diagrams")
    duplicate_files = list(diagrams_dir.glob("*_enhanced_enhanced.mmd"))
    assert (
        len(duplicate_files) == 0
    ), f"Found duplicate enhanced files: {[f.name for f in duplicate_files]}"


def test_fast_mcp_test_import():
    """Test that fast MCP test module can be imported"""
    try:
        from fast_mcp_test import test_diagram_with_mcp_simulation, quick_syntax_check

        assert callable(test_diagram_with_mcp_simulation)
        assert callable(quick_syntax_check)
    except ImportError as e:
        pytest.skip(f"Fast MCP test module not available: {e}")


def test_mcp_test_import():
    """Test that MCP test module can be imported"""
    try:
        from test_mcp_render import test_diagram_rendering, extract_diagram_content

        assert callable(test_diagram_rendering)
        assert callable(extract_diagram_content)
    except ImportError as e:
        pytest.skip(f"MCP test module not available: {e}")


def test_quick_mermaid_check_import():
    """Test that quick Mermaid check module can be imported"""
    try:
        from quick_mermaid_check import verify_mermaid_syntax, main

        assert callable(verify_mermaid_syntax)
        assert callable(main)
    except ImportError as e:
        pytest.skip(f"Quick Mermaid check module not available: {e}")


def test_diagram_content_extraction():
    """Test diagram content extraction functionality"""
    try:
        from fast_mcp_test import extract_diagram_content

        # Create a test diagram file
        test_content = """%% Test diagram
%% This is a comment
graph TD
    A[Start] --> B[End]
    style A fill:#f9f
    style B fill:#bbf
"""

        test_file = Path("test_diagram.mmd")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        try:
            extracted = extract_diagram_content(test_file)
            assert extracted is not None
            assert "graph TD" in extracted
            assert "A[Start] --> B[End]" in extracted
            assert "%% Test diagram" not in extracted  # Comments should be removed
        finally:
            test_file.unlink()  # Clean up

    except ImportError as e:
        pytest.skip(f"Fast MCP test module not available: {e}")


def test_syntax_validation():
    """Test syntax validation functionality"""
    try:
        from fast_mcp_test import quick_syntax_check

        # Test valid diagram
        valid_diagram = """graph TD
    A[Start] --> B[End]
"""
        is_valid, message = quick_syntax_check(valid_diagram)
        assert is_valid, f"Valid diagram failed validation: {message}"

        # Test invalid diagram (mismatched brackets)
        invalid_diagram = """graph TD
    A[Start --> B[End]
"""
        is_valid, message = quick_syntax_check(invalid_diagram)
        assert not is_valid, "Invalid diagram passed validation"
        assert "Mismatched brackets" in message

    except ImportError as e:
        pytest.skip(f"Fast MCP test module not available: {e}")


def test_makefile_targets():
    """Test that Makefile targets exist"""
    makefile_path = Path("Makefile")
    assert makefile_path.exists(), "Makefile not found"

    with open(makefile_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for new MCP testing targets
    assert "test-mcp:" in content, "test-mcp target not found in Makefile"
    assert "test-mcp-fast:" in content, "test-mcp-fast target not found in Makefile"
    assert "fix-diagrams:" in content, "fix-diagrams target not found in Makefile"
    assert "quality:" in content, "quality target not found in Makefile"


def test_ci_workflow_includes_mcp():
    """Test that CI workflow includes MCP testing"""
    ci_path = Path(".github/workflows/ci.yml")
    assert ci_path.exists(), "CI workflow not found"

    with open(ci_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for MCP testing steps
    assert (
        "Verify Mermaid diagrams (fast)" in content
    ), "MCP testing step not found in CI"
    assert "fast_mcp_test.py" in content, "Fast MCP test script not referenced in CI"
