from math_solver import solve_equation

def test_simple_arithmetic():
    assert solve_equation("2+3*4") == 14
    """
    Test solve_equation with a simple arithmetic expression.

    """
if __name__ == "__main__":
    test_simple_arithmetic()
    print("Basic arithmetic test done")
