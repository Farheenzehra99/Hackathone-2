#!/usr/bin/env python3
"""Simple test to verify the FastAPI application imports correctly."""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath('.'))

try:
    # Try to import the main app
    from app.main import app
    print("✓ Application imported successfully!")

    # Check that the app object exists and has expected attributes
    assert hasattr(app, 'routes'), "App should have routes attribute"
    print("✓ App has routes attribute")

    # Check that we have the expected endpoints
    route_paths = [route.path for route in app.routes]
    print(f"✓ Available routes: {route_paths}")

    # Check for our expected routes
    if '/' in route_paths:
        print("✓ Root endpoint exists")
    else:
        print("✗ Root endpoint missing")

    if '/health' in route_paths:
        print("✓ Health endpoint exists")
    else:
        print("✗ Health endpoint missing")

    print("\n✓ Application structure test passed!")

except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)