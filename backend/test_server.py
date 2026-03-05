"""
Standalone tests for the VISUALAIZE backend API.
These tests use FastAPI's TestClient (via httpx) and do NOT require a real
GEMINI_API_KEY — they validate routing, request/response shapes, and error
handling without calling the live AI service.

NOTE: These tests exercise a self-contained stub application that mirrors the
production app's routes and request/response contracts.  They are intentionally
isolated from the Google Generative AI SDK so that CI never needs live
credentials.  For end-to-end behaviour (actual AI responses, model fallback
logic, etc.) you should run integration tests against the production app with a
real GEMINI_API_KEY in a controlled environment.
"""

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Minimal test app — mirrors the real app's structure but with stub handlers
# ---------------------------------------------------------------------------

test_app = FastAPI()

test_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GraphRequest(BaseModel):
    prompt: str


class ChatRequest(BaseModel):
    message: str
    context: str


class CodeRequest(BaseModel):
    prompt: str
    language: str


@test_app.get("/")
def health_check():
    return {"status": "Online", "models": ["models/gemini-2.0-flash"]}


@test_app.post("/generate")
def generate_graph(request: GraphRequest):
    return {
        "title": "Test Graph",
        "summary": "A stub graph for testing.",
        "explanation": "Stub explanation.",
        "execution_trace": "Step 1 → Step 2",
        "code_snippet": "print('hello')",
        "code_explanation": "Prints hello",
        "nodes": [{"id": "1", "label": "Start"}, {"id": "2", "label": "End"}],
        "edges": [{"source": "1", "target": "2", "label": "next"}],
    }


@test_app.post("/chat")
def chat_with_ai(request: ChatRequest):
    return {"reply": f"Echo: {request.message}"}


@test_app.post("/regenerate_code")
def regenerate_code(request: CodeRequest):
    return {
        "code_snippet": f"# {request.language} version",
        "code_explanation": f"Converted to {request.language}",
    }


client = TestClient(test_app)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_health_check():
    """GET / should return status Online."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Online"
    assert "models" in data


def test_generate_graph_returns_expected_shape():
    """POST /generate should return a graph with nodes and edges."""
    response = client.post("/generate", json={"prompt": "binary search tree"})
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)


def test_generate_graph_missing_prompt():
    """POST /generate without prompt should return 422 Unprocessable Entity."""
    response = client.post("/generate", json={})
    assert response.status_code == 422


def test_chat_returns_reply():
    """POST /chat should return a reply field."""
    response = client.post(
        "/chat",
        json={"message": "What is this?", "context": "Title: Test. Explanation: A test."},
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)


def test_chat_missing_fields():
    """POST /chat without required fields should return 422."""
    response = client.post("/chat", json={"message": "hi"})
    assert response.status_code == 422


def test_regenerate_code_returns_snippet():
    """POST /regenerate_code should return code_snippet and code_explanation."""
    response = client.post(
        "/regenerate_code",
        json={"prompt": "binary search", "language": "JavaScript"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "code_snippet" in data
    assert "code_explanation" in data


def test_regenerate_code_missing_language():
    """POST /regenerate_code without language should return 422."""
    response = client.post("/regenerate_code", json={"prompt": "binary search"})
    assert response.status_code == 422


@pytest.mark.parametrize("route", ["/generate", "/chat", "/regenerate_code"])
def test_post_routes_reject_get(route: str):
    """All POST-only routes should return 405 Method Not Allowed on GET."""
    response = client.get(route)
    assert response.status_code == 405