#!/usr/bin/env python3
"""Test script to verify the FastAPI application imports and runs correctly."""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath('.'))

try:
    from app.main import app
    print("✓ Application imported successfully!")

    # Test that we can access the basic routes
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Test the root endpoint
    response = client.get("/")
    if response.status_code == 200:
        print("✓ Root endpoint working:", response.json())
    else:
        print("✗ Root endpoint failed with status:", response.status_code)

    # Test the health endpoint
    response = client.get("/health")
    if response.status_code == 200:
        print("✓ Health endpoint working:", response.json())
    else:
        print("✗ Health endpoint failed with status:", response.status_code)

    print("\n✓ All tests passed! The FastAPI application is working correctly.")

except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error during testing: {e}")
    sys.exit(1)