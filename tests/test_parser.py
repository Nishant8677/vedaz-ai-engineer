from generator.parser import parse_generated_json

def test_parse_valid_json():
    text = '{"messages": [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}, {"role": "assistant", "content": "a"}]}'
    data = parse_generated_json(text)
    assert data is not None
    assert len(data["messages"]) == 3

def test_parse_markdown_json():
    text = '```json\n{"messages": [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}, {"role": "assistant", "content": "a"}]}\n```'
    data = parse_generated_json(text)
    assert data is not None

def test_parse_invalid_json():
    text = "Not a json"
    data = parse_generated_json(text)
    assert data is None
