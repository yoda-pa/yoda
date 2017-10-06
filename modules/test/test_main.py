from modules.chat import process


def test_chat():
    assert process("how are you") == ("Wonderful as always. Thanks for asking.") or (
        "Lovely, thanks.") or ("Wonderful as always. Thanks for asking.")
