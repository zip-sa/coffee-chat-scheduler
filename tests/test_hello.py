def test_failed():
    """Simple test to verify pytest is working."""
    assert 1 + 1 == 3


def test_another_example():
    """Another example test."""
    result = "hello".upper()
    assert result == "HELLO"

def add(a, b):
    """Function to add two numbers."""
    return a + b

def test_add():
    """Test the add function."""
    assert add(1, 2) == 3
