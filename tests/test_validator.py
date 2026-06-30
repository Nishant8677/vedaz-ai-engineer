from checker.validator import validate_chat

def test_valid_chat():
    chat = {
        "messages": [
            {"role": "system", "content": "hello"},
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hey"}
        ]
    }
    assert validate_chat(chat) == True

def test_invalid_chat_missing_system():
    chat = {
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hey"}
        ]
    }
    assert validate_chat(chat) == False

def test_invalid_consecutive_roles():
    chat = {
        "messages": [
            {"role": "system", "content": "hello"},
            {"role": "user", "content": "hi"},
            {"role": "user", "content": "hi again"}
        ]
    }
    assert validate_chat(chat) == False
