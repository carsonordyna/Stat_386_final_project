import pytest
import sys
from pathlib import Path
import pandas as pd

@pytest.fixture(scope="module")
def package_imports():
    """Import package, handling both installed and local development scenarios"""
    try:
        from utah_housing_stat386 import run_demo, load_demo_data, get_cleaned_data
    except ModuleNotFoundError:
        # Allow running this test file directly from the repo without installing the package.
        # Project layout uses a "src/" directory, so we add it to sys.path.
        project_root = Path(__file__).resolve().parents[1]
        src_dir = project_root / "src"
        if src_dir.exists():
            sys.path.insert(0, str(src_dir))

        from utah_housing_stat386 import run_demo, load_demo_data, get_cleaned_data

    return {
        'run_demo': run_demo,
        'load_demo_data': load_demo_data,
        'get_cleaned_data': get_cleaned_data
    }


def test_imports(package_imports):
    """Test that all required functions can be imported"""
    assert 'run_demo' in package_imports
    assert 'load_demo_data' in package_imports
    assert 'get_cleaned_data' in package_imports
    assert callable(package_imports['run_demo'])
    assert callable(package_imports['load_demo_data'])
    assert callable(package_imports['get_cleaned_data'])


def test_load_demo_data(package_imports):
    """Test that demo data loads successfully"""
    load_demo_data = package_imports['load_demo_data']

    df = load_demo_data()

    # Check that data loaded
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0, "Demo data should not be empty"

    # Check expected columns exist
    expected_columns = ['mls', 'price', 'address', 'beds', 'baths', 'sqft']
    for col in expected_columns:
        assert col in df.columns, f"Column '{col}' should be in demo data"

    print(f"\n✓ Demo data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    print(f"✓ Columns: {list(df.columns)}")


def test_load_demo_data_content(package_imports):
    """Test that demo data has valid content"""
    load_demo_data = package_imports['load_demo_data']

    df = load_demo_data()

    # Check data types and content
    assert df['mls'].notna().any(), "MLS column should have data"
    assert df['price'].notna().any(), "Price column should have data"
    assert df['address'].notna().any(), "Address column should have data"

    print(f"\n✓ Demo data content validated")
    print("\nFirst few rows:")
    print(df.head())


def test_run_demo(package_imports, capsys):
    """Test that run_demo executes without errors"""
    run_demo = package_imports['run_demo']

    # Run the demo (should not raise any exceptions)
    run_demo()

    # Capture output
    captured = capsys.readouterr()

    # Check that demo produced some output
    assert len(captured.out) > 0, "Demo should produce output"
    assert "DEMO" in captured.out.upper() or "DATA" in captured.out.upper(), \
        "Demo output should mention data or demo"

    print(f"\n✓ run_demo() executed successfully")


def test_get_cleaned_data_import(package_imports):
    """Test that get_cleaned_data is available and callable"""
    get_cleaned_data = package_imports['get_cleaned_data']

    assert get_cleaned_data is not None
    assert callable(get_cleaned_data)

    print(f"\n✓ get_cleaned_data() is available")


# Optional: Test actual data cleaning (commented out because it requires scraping)
# Uncomment if you want to test with actual data scraping
"""
def test_get_cleaned_data_execution(package_imports):
    '''Test that get_cleaned_data can execute (with small dataset)'''
    get_cleaned_data = package_imports['get_cleaned_data']

    # Test with minimal data to avoid long scraping
    df_cleaned = get_cleaned_data(max_listings=2, cities=['provo'])

    assert df_cleaned is not None
    assert isinstance(df_cleaned, pd.DataFrame)

    print(f"\\n✓ get_cleaned_data() executed: {len(df_cleaned)} rows")
"""

if __name__ == "__main__":
    # Allow running this file directly
    pytest.main([__file__, "-v", "-s"])