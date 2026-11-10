"""UI confirmation must be the only path from a model send call to Telegram."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import chat
import providers
import tools
from providers.base import ModelResponse, ToolCall


APP = Path(__file__).resolve().parents[1] / "app.py"
MESSAGE = "Exact Telegram message"


class SendProvider:
    def complete(self, *args, **kwargs):
        return ModelResponse(tool_calls=[ToolCall("send", {"text": MESSAGE})])


@pytest.fixture
def send_ui(monkeypatch):
    calls = []
    monkeypatch.setattr(providers, "make_provider", lambda name: SendProvider())
    monkeypatch.setattr(chat, "write_transcript", lambda path, record: None)

    def fake_send(**kwargs):
        calls.append(kwargs)
        return {"status": "sent"}

    monkeypatch.setitem(tools.TOOL_FUNCTIONS, "send", fake_send)
    at = AppTest.from_file(str(APP)).run(timeout=30)
    assert not at.exception
    at.chat_input[0].set_value("Please send it").run(timeout=30)
    assert not at.exception
    assert at.session_state["turns_display"][-1]["status"] == "waiting_for_confirmation"
    return at, calls


def test_ui_send_cancel_never_calls_tool(send_ui):
    at, calls = send_ui
    assert calls == []
    assert at.session_state["pending_send"]["text"] == MESSAGE
    next(button for button in at.button if button.key == "send_cancel").click().run(timeout=30)
    assert not at.exception
    assert calls == []
    assert at.session_state["pending_send"] is None
    assert at.session_state["turns_display"][-1]["status"] == "cancelled"


def test_ui_send_confirm_calls_tool_with_exact_message(send_ui):
    at, calls = send_ui
    assert calls == []
    next(button for button in at.button if button.key == "send_confirm").click().run(timeout=30)
    assert not at.exception
    assert calls == [{"text": MESSAGE, "confirmed": True}]
    assert at.session_state["turns_display"][-1]["status"] == "answered"
    assert at.session_state["turns_display"][-1]["confirmation"]["approved"] is True
