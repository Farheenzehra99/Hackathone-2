"""Unit tests for color utilities."""

import pytest
from src.utils.colors import get_console, COLOR_SCHEME


def test_color_scheme_contains_all_required_keys():
    """Test COLOR_SCHEME has all required semantic color keys."""
    required_keys = [
        'success', 'error', 'info', 'warning',
        'heading', 'subheading',
        'priority_high', 'priority_medium', 'priority_low',
        'completed', 'incomplete',
        'table_header', 'table_border'
    ]

    for key in required_keys:
        assert key in COLOR_SCHEME, f"COLOR_SCHEME missing required key: {key}"


def test_get_console_returns_singleton():
    """Test get_console() returns the same instance on multiple calls."""
    console1 = get_console()
    console2 = get_console()

    assert console1 is console2, "get_console() should return singleton instance"


def test_get_console_returns_console_instance():
    """Test get_console() returns a Rich Console instance."""
    from rich.console import Console

    console = get_console()
    assert isinstance(console, Console), "get_console() should return Rich Console instance"


def test_color_scheme_values_are_strings():
    """Test all COLOR_SCHEME values are valid color strings."""
    for key, value in COLOR_SCHEME.items():
        assert isinstance(value, str), f"COLOR_SCHEME['{key}'] should be a string"
        assert len(value) > 0, f"COLOR_SCHEME['{key}'] should not be empty"
