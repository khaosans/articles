"""Tests for Mermaid diagrams."""

import pytest
from pathlib import Path
import re

def test_mermaid_syntax():
    """Test that all Mermaid diagrams have valid syntax."""
    diagrams_dir = Path("extracted_diagrams")
    
    for mmd_file in diagrams_dir.glob("*.mmd"):
        with open(mmd_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for basic Mermaid syntax
        valid_starters = [
            'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
            'mindmap', 'radar', 'stateDiagram', 'erDiagram', 'journey', 
            'gantt', 'pie', 'quadrantChart'
        ]
        
        lines = content.split('\n')
        first_diagram_line = None
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('%%') and not line.startswith('//'):
                first_diagram_line = line
                break
        
        if first_diagram_line:
            has_valid_starter = any(first_diagram_line.startswith(starter) for starter in valid_starters)
            assert has_valid_starter, f"Invalid diagram type in {mmd_file.name}: {first_diagram_line}"
        else:
            assert False, f"No valid diagram content found in {mmd_file.name}"

def test_enhanced_diagrams():
    """Test that enhanced diagrams have proper styling."""
    diagrams_dir = Path("extracted_diagrams")
    
    for mmd_file in diagrams_dir.glob("*_enhanced.mmd"):
        with open(mmd_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for enhanced styling
        assert "classDef" in content, f"Enhanced diagram {mmd_file.name} should have classDef"
        assert "font-size" in content, f"Enhanced diagram {mmd_file.name} should have font-size"
        assert "font-weight" in content, f"Enhanced diagram {mmd_file.name} should have font-weight"

def test_no_duplicate_enhanced():
    """Test that there are no duplicate enhanced files."""
    diagrams_dir = Path("extracted_diagrams")
    
    enhanced_files = [f.name for f in diagrams_dir.glob("*_enhanced.mmd")]
    duplicate_enhanced = [f for f in enhanced_files if "_enhanced_enhanced" in f]
    
    assert len(duplicate_enhanced) == 0, f"Found duplicate enhanced files: {duplicate_enhanced}"
