"""Tests for utility tools."""

import pytest
from pathlib import Path
import sys
import os

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))


def test_quick_mermaid_check_import():
    """Test that quick_mermaid_check can be imported."""
    try:
        import quick_mermaid_check

        assert quick_mermaid_check is not None
    except ImportError as e:
        pytest.fail(f"Failed to import quick_mermaid_check: {e}")


def test_enhance_mermaid_diagrams_import():
    """Test that enhance_mermaid_diagrams can be imported."""
    try:
        import enhance_mermaid_diagrams

        assert enhance_mermaid_diagrams is not None
    except ImportError as e:
        pytest.fail(f"Failed to import enhance_mermaid_diagrams: {e}")


def test_extracted_diagrams_exist():
    """Test that extracted_diagrams directory exists and contains files."""
    diagrams_dir = Path("extracted_diagrams")
    assert diagrams_dir.exists(), "extracted_diagrams directory should exist"

    mmd_files = list(diagrams_dir.glob("*.mmd"))
    assert len(mmd_files) > 0, "Should have at least one .mmd file"


def test_docs_directory_exists():
    """Test that docs directory exists."""
    docs_dir = Path("docs")
    assert docs_dir.exists(), "docs directory should exist"


def test_tools_directory_exists():
    """Test that tools directory exists."""
    tools_dir = Path("tools")
    assert tools_dir.exists(), "tools directory should exist"
