from yodapa.hi import hu, add_numbers


def test_greet():
    assert hu("Alice") == "Hellowww Alice"


def test_add_numbers():
    assert add_numbers(3, 4) == 7
