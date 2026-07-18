import socket
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ai_os.chatbot import SimpleChatbot
from ai_os.providers import ApiModelProvider, RuleBasedProvider

app = FastAPI(title="AI OS Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = SimpleChatbot(provider=ApiModelProvider())


def get_available_port(start_port: int = 8000) -> int:
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def read_root() -> FileResponse:
    return FileResponse(Path(__file__).resolve().parents[2] / "templates" / "index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(message: ChatMessage) -> ChatResponse:
    response = bot.chat(message.message)
    return ChatResponse(response=response)
