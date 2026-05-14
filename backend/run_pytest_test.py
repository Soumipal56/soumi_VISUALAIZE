from unittest.mock import patch
import main

@patch("main.get_smart_response")
def test_mock(mock_get):
    mock_get.return_value = "MOCKED"
    from fastapi.testclient import TestClient
    client = TestClient(main.app)
    resp = client.post("/chat", json={"message": "hi", "context": "ctx"})
    print(resp.json())

if __name__ == "__main__":
    test_mock()
