# Test Scripts for Transistor Database

This directory contains test scripts to verify the Transistor Database installation and functionality.

## Quick Start

### Option 1: Quick Test (Recommended First)
Run the quick test to verify basic functionality:

```bash
python quick_test.py
```

This will:
- Verify the installation
- Check database connectivity
- Load a sample transistor
- Test basic working point calculations

**Time:** ~5 seconds

### Option 2: Comprehensive Test
Run the full test suite for complete verification:

```bash
python test_transistor_database.py
```

This will test:
- Database initialization
- Transistor loading
- Working point calculations
- Data access
- Plotting functions (if enabled)
- Export functions (PLECS, Matlab, Simulink, etc.)
- Calculation functions
- Database operations

**Time:** ~30-60 seconds

## Configuration

You can modify the test behavior by editing the configuration at the top of `test_transistor_database.py`:

```python
ENABLE_PLOTTING = False  # Set to True to enable matplotlib plots
ENABLE_EXPORTS = True    # Set to True to test export functions
TEST_DATABASE_PATH = None  # Custom database path (uses examples/tdb_example by default)
```

## Expected Output

### Quick Test Output
```
============================================================
Transistor Database - Quick Test
============================================================

1. Initializing database...
   ✅ Database initialized at: .../examples/tdb_example

2. Listing available transistors...
   ✅ Found 25 transistor(s):
      - CREE_C3M0016120K
      - CREE_C3M0060065J
      ...

3. Loading transistor: CREE_C3M0016120K...
   ✅ Loaded: CREE_C3M0016120K
      Manufacturer: CREE
      Type: SiC MOSFET
      Max Voltage: 1200 V
      Max Current: 16 A

4. Testing working point calculation...
   ✅ Working point set successfully
      Switch R_channel: 0.1234 Ohm

============================================================
✅ Quick test completed successfully!
============================================================
```

## Troubleshooting

### No transistors found
If you see "No transistors found", you have two options:

1. **Use the example database** (if it exists):
   - The test scripts automatically look for transistors in `transistordatabase/examples/tdb_example/`
   - If this folder exists with JSON files, they will be used

2. **Download from online database**:
   ```python
   from transistordatabase.database_manager import DatabaseManager
   
   db = DatabaseManager()
   db.set_operation_mode_json("your_database_path")
   db.update_from_fileexchange(True)
   ```

### Import errors
If you get import errors, make sure you've installed dependencies:

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

### Plotting issues
If plotting tests fail:
- Set `ENABLE_PLOTTING = False` to skip plotting tests
- Or install matplotlib: `pip install matplotlib`
- On headless systems, matplotlib may need a non-interactive backend

### Export errors
Some export functions may fail if:
- Required simulation software templates are missing
- Data required for export is not available in the transistor
- File permissions prevent writing output files

These are warnings, not critical errors. The test will continue.

## Test Output Files

When `ENABLE_EXPORTS = True`, the comprehensive test creates a `test_outputs/` folder with:
- Virtual datasheet HTML files
- PLECS XML files
- Matlab .mat files
- Simulink model files

## Running Tests in CI/CD

For continuous integration, use:

```bash
python quick_test.py
```

Or with the comprehensive test (no plotting):

```python
# In test_transistor_database.py, set:
ENABLE_PLOTTING = False
ENABLE_EXPORTS = False  # Optional, set to False to skip file I/O
```

## Next Steps

After running the tests successfully:

1. **Explore examples**: Check `transistordatabase/examples/` for usage examples
2. **Read documentation**: See `README.rst` for detailed documentation
3. **Use the GUI**: Launch the graphical interface for visual database management
4. **Create your own**: Use the template system to add your own transistors

## Support

If tests fail:
1. Check the error message for specific issues
2. Verify all dependencies are installed
3. Ensure the database path is correct
4. Check that example JSON files exist in the examples folder

For more help, see the main project documentation or open an issue on GitHub.

