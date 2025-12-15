"""
Test script for upload module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Test imports
print("Testing imports...")
from late import Late
from late.upload import (
    SmartUploader,
    DirectUploader,
    VercelBlobUploader,
    UploadFile,
    UploadResult,
    UploadProgress,
    LargeFileError,
)
print("✓ All imports successful")

# Test files
SMALL_IMAGE = "/Users/carlos/Documents/WebDev/Freelance/miquel-palet/Schedule-Posts-API/app/apple-icon.png"
LARGE_VIDEO = "/Users/carlos/Documents/Video recordings/screen-studio/Built-in Retina Display.mp4"

# Credentials
LATE_API_KEY = "sk_fb144cafa04c50eecb9102bb240657d4871f6fc5fd43eb9c22e4b869ff030c7e"
LATE_BASE_URL = "https://getlate.dev/api"
VERCEL_BLOB_TOKEN = "vercel_blob_rw_qf6opyLdArRJW0lJ_GBJHZ2I9KR0O1zo8iq31z96CrCAnUR"

# Verify files exist
for path, name in [(SMALL_IMAGE, "Small image"), (LARGE_VIDEO, "Large video")]:
    if Path(path).exists():
        size = Path(path).stat().st_size
        print(f"✓ {name}: {size:,} bytes ({size / (1024*1024):.1f} MB)")
    else:
        print(f"✗ {name} not found: {path}")

# Create client
client = Late(api_key=LATE_API_KEY, base_url=LATE_BASE_URL)
print(f"\n✓ Late client created (base_url: {LATE_BASE_URL})")

# Test 1: Direct upload (small file)
print("\n" + "="*60)
print("TEST 1: Direct upload (small file < 4MB)")
print("="*60)
try:
    result = client.media.upload(SMALL_IMAGE)
    print(f"✓ Upload successful!")
    print(f"  URL: {result['files'][0]['url']}")
except Exception as e:
    print(f"✗ Upload failed: {e}")

# Test 2: Vercel Blob upload (large file)
print("\n" + "="*60)
print("TEST 2: Vercel Blob upload (large file ~278MB)")
print("="*60)

def progress_callback(p: UploadProgress):
    pct = p.percentage
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    print(f"  [{bar}] {pct:.1f}%", end="\r")

try:
    result = client.media.upload_large(
        LARGE_VIDEO,
        vercel_token=VERCEL_BLOB_TOKEN,
        on_progress=progress_callback
    )
    print(f"\n✓ Vercel Blob upload successful!")
    print(f"  URL: {result['url']}")
except Exception as e:
    print(f"\n✗ Vercel Blob upload failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("All tests completed!")
print("="*60)
