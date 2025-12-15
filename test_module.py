#!/usr/bin/env python3
"""
Test script to debug the cggtts module loading issue
"""

import sys
import traceback

def test_module_loading():
    print("Testing cggtts module loading...")
    
    # Test 1: Direct import
    print("\n1. Testing direct import...")
    try:
        import cggtts
        print("   ✓ Module imported successfully")
        print(f"   Module: {cggtts}")
        print(f"   Module type: {type(cggtts)}")
    except ImportError as e:
        print(f"   ✗ Import failed: {e}")
        traceback.print_exc()
        return
    
    # Test 2: Check for functions
    print("\n2. Checking for functions...")
    try:
        # List all attributes
        attrs = [attr for attr in dir(cggtts) if not attr.startswith('_')]
        print(f"   Non-private attributes: {attrs}")
        
        # Check specifically for parse_cggtts
        has_func = hasattr(cggtts, 'parse_cggtts')
        print(f"   Has parse_cggtts: {has_func}")
        
        if has_func:
            func = getattr(cggtts, 'parse_cggtts')
            print(f"   parse_cggtts: {func} (type: {type(func)})")
        
    except Exception as e:
        print(f"   ✗ Error checking functions: {e}")
        traceback.print_exc()
    
    # Test 3: Try to access the underlying .so module
    print("\n3. Testing underlying module access...")
    try:
        # Import the actual extension module
        from cggtts import cggtts as ext_module
        print(f"   ✓ Extension module imported: {ext_module}")
        print(f"   Extension module type: {type(ext_module)}")
        
        # Check its attributes
        ext_attrs = [attr for attr in dir(ext_module) if not attr.startswith('_')]
        print(f"   Extension module non-private attributes: {ext_attrs}")
        
    except ImportError as e:
        print(f"   ✗ Could not import extension module: {e}")
    except Exception as e:
        print(f"   ✗ Error accessing extension module: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_module_loading()
