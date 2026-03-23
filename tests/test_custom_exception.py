import sys
import os

# Add the project root to sys.path to allow importing from src
sys.path.append(os.getcwd())

from src.common.custom_exception import CustomException

def test_exception_inside_except():
    print("Testing CustomException inside except block...")
    try:
        1 / 0
    except Exception as e:
        ce = CustomException("Divided by zero", e)
        print(f"Caught expected exception: {ce}")
        assert "File Name" in str(ce)
        assert "Line Number" in str(ce)
        assert "Divided by zero" in str(ce)

def test_exception_outside_except():
    print("\nTesting CustomException outside except block (should no longer crash)...")
    try:
        raise CustomException("Generic error")
    except CustomException as ce:
        print(f"Caught expected exception: {ce}")
        assert "File Name" not in str(ce)
        assert "Generic error" in str(ce)

if __name__ == "__main__":
    try:
        test_exception_inside_except()
        test_exception_outside_except()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
