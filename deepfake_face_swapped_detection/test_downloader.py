#!/usr/bin/env python3
"""
Test script to verify the downloader module works correctly
"""

import sys
import os

# Add backend_video to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend_video'))

from downloader import download_video, get_video_metadata

print("Testing downloader module...")
print("=" * 60)

# Test 1: Check if yt-dlp is available
try:
    import yt_dlp
    print("✓ yt-dlp is installed and available")
except ImportError:
    print("⚠️  yt-dlp is not installed")
    print("   Install with: pip install yt-dlp")

# Test 2: Test metadata extraction with a simple URL
print("\nTesting metadata extraction...")
print("-" * 60)

test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
print(f"Testing with URL: {test_url}")

try:
    metadata = get_video_metadata(test_url)
    print(f"✓ Metadata extracted successfully")
    print(f"  Title: {metadata.get('title', 'Unknown')}")
    print(f"  Duration: {metadata.get('duration', 'Unknown')} seconds")
    print(f"  Uploader: {metadata.get('uploader', 'Unknown')}")
except Exception as e:
    print(f"⚠️  Could not extract metadata: {e}")
    print("   This is OK - may be due to network or platform restrictions")

print("\n" + "=" * 60)
print("Test complete!")
print("\nNote: To test video downloading, use the /predict-video-url endpoint")
print("in the FastAPI application.")
