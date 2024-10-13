from yodapa.yoda import hello


def test_hello(capsys):
    hello("Yoda")
    actual_response = capsys.readouterr()
    assert "Hello Yoda!\n" == actual_response.out
