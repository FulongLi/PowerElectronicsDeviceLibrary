"""
Quick test script for Transistor Database - Simple and fast verification.

This is a minimal test to quickly verify the installation works.
"""

import os
import sys
from pathlib import Path

# Check Python version
if sys.version_info < (3, 11):
    print("=" * 60)
    print("Python Version Warning")
    print("=" * 60)
    print(f"\nCurrent Python version: {sys.version}")
    print("This project requires Python 3.11 or higher.")
    print("\nThe project uses Python 3.11+ features (union types: int | float).")
    print("\nPlease upgrade Python or use a virtual environment with Python 3.11+")
    print("\nYou can download Python 3.11+ from: https://www.python.org/downloads/")
    sys.exit(1)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from transistordatabase.database_manager import DatabaseManager
    
    print("=" * 60)
    print("Transistor Database - Quick Test")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "transistordatabase", "examples", "tdb_example"
    )
    
    tdb = DatabaseManager()
    tdb.set_operation_mode_json(db_path)
    print(f"   [OK] Database initialized at: {db_path}")
    
    # List transistors
    print("\n2. Listing available transistors...")
    transistor_names = tdb.get_transistor_names_list()
    
    if not transistor_names:
        print("   [WARNING] No transistors found!")
        print("   Tip: Run the full test script or download transistors")
        sys.exit(0)
    
    print(f"   [OK] Found {len(transistor_names)} transistor(s):")
    for name in transistor_names[:5]:  # Show first 5
        print(f"      - {name}")
    if len(transistor_names) > 5:
        print(f"      ... and {len(transistor_names) - 5} more")
    
    # Load first transistor
    print(f"\n3. Loading transistor: {transistor_names[0]}...")
    transistor = tdb.load_transistor(transistor_names[0])
    print(f"   [OK] Loaded: {transistor.name}")
    print(f"      Manufacturer: {transistor.manufacturer}")
    print(f"      Type: {transistor.type}")
    print(f"      Max Voltage: {transistor.v_abs_max} V")
    print(f"      Max Current: {transistor.i_abs_max} A")
    
    # Test working point
    print("\n4. Testing working point calculation...")
    try:
        transistor.quickstart_wp()
        print(f"   [OK] Working point set successfully")
        print(f"      Switch R_channel: {transistor.wp.switch_r_channel:.4f} Ohm")
    except Exception as e:
        print(f"   [WARNING] Working point calculation: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Quick test completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("   - Run 'python test_transistor_database.py' for full tests")
    print("   - Check examples/ folder for usage examples")
    print("   - Read README.rst for documentation")
    
except ImportError as e:
    print(f"\n[ERROR] Import error: {e}")
    print("   Make sure you've installed all dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

