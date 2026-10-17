from fastapi import APIRouter, HTTPException

from api.schemas import ChatRequest, ChatResponse
from core.providers.gemini import (
    GeminiProvider,
    GeminiRequestError,
)

from config import GEMINI_API_KEY, MODEL_NAME
from logs.logging_config import logger
from utils import load_system_prompt


router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest) -> ChatResponse:

    try:
        provider = GeminiProvider(
            api_key=GEMINI_API_KEY,
            model_name=MODEL_NAME,
            system_prompt=load_system_prompt(),
        )

        answer = provider.ask(
            prompt=request.message,
        )

        return ChatResponse(answer=answer)

    except GeminiRequestError as error:
        logger.error("Chat request failed: %s", error)

        raise HTTPException(
            status_code=502,
            detail="AI provider is unavailable",
        ) from error