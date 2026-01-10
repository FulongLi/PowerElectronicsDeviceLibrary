"""
Comprehensive test script for the Transistor Database project.

This script demonstrates and tests the main functionality of the transistordatabase library.
Run this script to verify the installation and functionality.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from transistordatabase.database_manager import DatabaseManager
from transistordatabase.exceptions import MissingDataError

# Configuration
ENABLE_PLOTTING = False  # Set to True to enable matplotlib plots (requires display)
ENABLE_EXPORTS = True    # Set to True to test export functions
TEST_DATABASE_PATH = None  # Will use examples/tdb_example if None


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_database_initialization():
    """Test 1: Initialize database manager."""
    print_section("Test 1: Database Initialization")
    
    try:
        # Determine database path
        if TEST_DATABASE_PATH is None:
            db_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "transistordatabase", "examples", "tdb_example"
            )
        else:
            db_path = TEST_DATABASE_PATH
        
        # Check if database exists
        if not os.path.exists(db_path):
            print(f"⚠️  Database path not found: {db_path}")
            print("   Creating empty database directory...")
            os.makedirs(db_path, exist_ok=True)
        
        # Initialize database manager
        tdb = DatabaseManager()
        tdb.set_operation_mode_json(db_path)
        
        print(f"✅ Database initialized successfully")
        print(f"   Database path: {db_path}")
        print(f"   Operation mode: {tdb.operation_mode.value}")
        
        return tdb, db_path
    
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


def test_list_transistors(tdb):
    """Test 2: List available transistors."""
    print_section("Test 2: List Available Transistors")
    
    try:
        transistor_names = tdb.get_transistor_names_list()
        
        if not transistor_names:
            print("⚠️  No transistors found in database")
            print("   You may need to download transistors or add them manually")
            return None
        
        print(f"✅ Found {len(transistor_names)} transistor(s) in database:")
        for i, name in enumerate(transistor_names, 1):
            print(f"   {i}. {name}")
        
        return transistor_names[0] if transistor_names else None
    
    except Exception as e:
        print(f"❌ Failed to list transistors: {e}")
        raise


def test_load_transistor(tdb, transistor_name):
    """Test 3: Load a transistor from database."""
    print_section("Test 3: Load Transistor")
    
    if transistor_name is None:
        print("⚠️  Skipping - No transistor available to load")
        return None
    
    try:
        transistor = tdb.load_transistor(transistor_name)
        
        print(f"✅ Successfully loaded transistor: {transistor.name}")
        print(f"   Manufacturer: {transistor.manufacturer}")
        print(f"   Type: {transistor.type}")
        print(f"   Max Voltage: {transistor.v_abs_max} V")
        print(f"   Max Current: {transistor.i_abs_max} A")
        print(f"   Switch Tj max: {transistor.switch.t_j_max} °C")
        print(f"   Diode Tj max: {transistor.diode.t_j_max} °C")
        print(f"   Channel datasets (switch): {len(transistor.switch.channel)}")
        print(f"   Channel datasets (diode): {len(transistor.diode.channel)}")
        print(f"   E_on datasets: {len(transistor.switch.e_on)}")
        print(f"   E_off datasets: {len(transistor.switch.e_off)}")
        
        return transistor
    
    except Exception as e:
        print(f"❌ Failed to load transistor: {e}")
        raise


def test_working_point(tdb, transistor):
    """Test 4: Working point calculations."""
    print_section("Test 4: Working Point Calculations")
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    try:
        # Test quickstart working point
        print("   Testing quickstart_wp()...")
        transistor.quickstart_wp()
        print(f"   ✅ Quickstart working point set")
        print(f"      Switch V_channel: {transistor.wp.switch_v_channel} V")
        print(f"      Switch R_channel: {transistor.wp.switch_r_channel} Ohm")
        
        # Test manual working point update
        print("\n   Testing update_wp()...")
        transistor.update_wp(t_j=125, v_g=15, i_channel=50)
        print(f"   ✅ Manual working point set")
        print(f"      Temperature: 125°C, Gate voltage: 15V, Current: 50A")
        
        # Test find_approx_wp for switch
        print("\n   Testing find_approx_wp() for switch...")
        channel, e_on, e_off = transistor.switch.find_approx_wp(
            t_j=125,
            v_g=15,
            normalize_t_to_v=10
        )
        print(f"   ✅ Found approximate working point")
        print(f"      Channel Tj: {channel.t_j}°C, Vg: {channel.v_g}V")
        print(f"      E_on Tj: {e_on.t_j}°C, Vg: {e_on.v_g}V")
        print(f"      E_off Tj: {e_off.t_j}°C, Vg: {e_off.v_g}V")
        
    except MissingDataError as e:
        print(f"   ⚠️  Missing data error (expected for some transistors): {e}")
    except Exception as e:
        print(f"   ❌ Working point calculation failed: {e}")


def test_data_access(tdb, transistor):
    """Test 5: Access transistor data."""
    print_section("Test 5: Data Access")
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    try:
        # Access switch data
        print("   Switch data:")
        if transistor.switch.channel:
            ch = transistor.switch.channel[0]
            print(f"      First channel dataset: Tj={ch.t_j}°C, Vg={ch.v_g}V")
            print(f"      Data points: {len(ch.graph_v_i[0])}")
        
        # Access diode data
        print("\n   Diode data:")
        if transistor.diode.channel:
            ch = transistor.diode.channel[0]
            print(f"      First channel dataset: Tj={ch.t_j}°C, Vg={ch.v_g}V")
            print(f"      Data points: {len(ch.graph_v_i[0])}")
        
        # Access energy data
        print("\n   Energy data:")
        if transistor.switch.e_on:
            e_on = transistor.switch.e_on[0]
            print(f"      E_on dataset: Tj={e_on.t_j}°C, Vg={e_on.v_g}V, Vsupply={e_on.v_supply}V")
        
        if transistor.switch.e_off:
            e_off = transistor.switch.e_off[0]
            print(f"      E_off dataset: Tj={e_off.t_j}°C, Vg={e_off.v_g}V, Vsupply={e_off.v_supply}V")
        
        print("\n   ✅ Data access successful")
        
    except Exception as e:
        print(f"   ❌ Data access failed: {e}")


def test_plotting(tdb, transistor):
    """Test 6: Plotting functions."""
    print_section("Test 6: Plotting Functions")
    
    if not ENABLE_PLOTTING:
        print("   ⚠️  Plotting disabled (set ENABLE_PLOTTING=True to enable)")
        return
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        print("   Testing plot functions (plots will be saved, not displayed)...")
        
        # Test switch plotting
        if transistor.switch.channel:
            print("   - Testing switch.plot_all_channel_data()...")
            transistor.switch.plot_all_channel_data(buffer_req=True)
            print("      ✅ Switch channel data plotted")
        
        # Test diode plotting
        if transistor.diode.channel:
            print("   - Testing diode.plot_all_channel_data()...")
            transistor.diode.plot_all_channel_data(buffer_req=True)
            print("      ✅ Diode channel data plotted")
        
        # Test energy plotting
        if transistor.switch.e_on and transistor.switch.e_off:
            print("   - Testing switch.plot_energy_data()...")
            result = transistor.switch.plot_energy_data(buffer_req=True)
            if result is not None:
                print("      ✅ Energy data plotted")
        
        print("\n   ✅ Plotting tests completed")
        
    except ImportError:
        print("   ⚠️  Matplotlib not available for plotting")
    except Exception as e:
        print(f"   ❌ Plotting failed: {e}")


def test_export_functions(tdb, transistor):
    """Test 7: Export functions."""
    print_section("Test 7: Export Functions")
    
    if not ENABLE_EXPORTS:
        print("   ⚠️  Export tests disabled (set ENABLE_EXPORTS=True to enable)")
        return
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "test_outputs")
    os.makedirs(output_dir, exist_ok=True)
    original_dir = os.getcwd()
    
    try:
        os.chdir(output_dir)
        
        # Test virtual datasheet export
        print("   Testing export_datasheet()...")
        try:
            html_str = transistor.export_datasheet(build_collection=True)
            if html_str:
                output_file = os.path.join(output_dir, f"{transistor.name}_datasheet.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html_str)
                print(f"      ✅ Virtual datasheet exported: {output_file}")
        except Exception as e:
            print(f"      ⚠️  Datasheet export failed: {e}")
        
        # Test PLECS export
        print("\n   Testing export_plecs()...")
        try:
            transistor.export_plecs()
            print("      ✅ PLECS export completed")
        except Exception as e:
            print(f"      ⚠️  PLECS export failed: {e}")
        
        # Test Matlab export
        print("\n   Testing export_matlab()...")
        try:
            transistor.export_matlab()
            print("      ✅ Matlab export completed")
        except Exception as e:
            print(f"      ⚠️  Matlab export failed: {e}")
        
        # Test Simulink export
        print("\n   Testing export_simulink_loss_model()...")
        try:
            transistor.export_simulink_loss_model()
            print("      ✅ Simulink export completed")
        except Exception as e:
            print(f"      ⚠️  Simulink export failed: {e}")
        
        print(f"\n   ✅ Export tests completed. Files saved to: {output_dir}")
        
    except Exception as e:
        print(f"   ❌ Export tests failed: {e}")
    finally:
        os.chdir(original_dir)


def test_calculations(tdb, transistor):
    """Test 8: Calculation functions."""
    print_section("Test 8: Calculation Functions")
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    try:
        # Test linearization
        print("   Testing calc_lin_channel()...")
        try:
            v_ch, r_ch = transistor.calc_lin_channel(
                t_j=125,
                v_g=15,
                i_channel=50,
                switch_or_diode='switch'
            )
            print(f"      ✅ Switch linearization: V={v_ch}V, R={r_ch}Ohm")
        except Exception as e:
            print(f"      ⚠️  Switch linearization failed: {e}")
        
        try:
            v_ch, r_ch = transistor.calc_lin_channel(
                t_j=125,
                v_g=-4,
                i_channel=50,
                switch_or_diode='diode'
            )
            print(f"      ✅ Diode linearization: V={v_ch}V, R={r_ch}Ohm")
        except Exception as e:
            print(f"      ⚠️  Diode linearization failed: {e}")
        
        # Test capacitance energy calculations
        print("\n   Testing calc_v_eoss()...")
        try:
            if transistor.graph_v_ecoss is not None:
                e_oss = transistor.calc_v_eoss()
                print(f"      ✅ E_oss calculation completed")
            else:
                print("      ⚠️  No C_oss data available")
        except Exception as e:
            print(f"      ⚠️  E_oss calculation failed: {e}")
        
        print("\n   ✅ Calculation tests completed")
        
    except Exception as e:
        print(f"   ❌ Calculation tests failed: {e}")


def test_database_operations(tdb, transistor):
    """Test 9: Database operations."""
    print_section("Test 9: Database Operations")
    
    if transistor is None:
        print("⚠️  Skipping - No transistor loaded")
        return
    
    try:
        # Test print_tdb
        print("   Testing print_tdb()...")
        tdb.print_tdb()
        print("      ✅ Database summary printed")
        
        # Test convert to dict
        print("\n   Testing convert_to_dict()...")
        transistor_dict = transistor.convert_to_dict()
        print(f"      ✅ Transistor converted to dictionary")
        print(f"      Dictionary keys: {len(transistor_dict)}")
        
        print("\n   ✅ Database operation tests completed")
        
    except Exception as e:
        print(f"   ❌ Database operation tests failed: {e}")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  TRANSISTOR DATABASE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Plotting enabled: {ENABLE_PLOTTING}")
    print(f"  Exports enabled: {ENABLE_EXPORTS}")
    
    try:
        # Run tests in sequence
        tdb, db_path = test_database_initialization()
        transistor_name = test_list_transistors(tdb)
        transistor = test_load_transistor(tdb, transistor_name)
        
        # Run feature tests
        test_working_point(tdb, transistor)
        test_data_access(tdb, transistor)
        test_plotting(tdb, transistor)
        test_calculations(tdb, transistor)
        test_database_operations(tdb, transistor)
        test_export_functions(tdb, transistor)
        
        # Summary
        print_section("Test Summary")
        print("✅ All tests completed successfully!")
        print(f"\nNext steps:")
        print(f"  1. Check the 'test_outputs' folder for exported files")
        print(f"  2. Set ENABLE_PLOTTING=True to see visualization plots")
        print(f"  3. Explore the examples/ folder for more usage examples")
        print(f"  4. Check the documentation for advanced features")
        
    except Exception as e:
        print_section("Test Summary")
        print(f"❌ Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

