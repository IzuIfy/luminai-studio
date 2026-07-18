from ai_os.app import chat, get_available_port, read_root


def test_get_available_port_returns_a_valid_port() -> None:
    port = get_available_port(8000)

    assert isinstance(port, int)
    assert port >= 8000


def test_chat_endpoint_returns_rule_based_reply() -> None:
    response = chat(type("Message", (), {"message": "Hello"})())

    assert response.response.lower().startswith("hello")


def test_home_page_serves_html() -> None:
    response = read_root()

    assert response.status_code == 200
    assert "AI OS Chatbot" in response.body.decode("utf-8")
