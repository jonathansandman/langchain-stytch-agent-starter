from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from config.logging_config import logger

router = APIRouter()


class ExplainRequestBody(BaseModel):
    topic: str


@router.post("/explain")
async def explain(request: ExplainRequestBody):
    logger.info(f"Received request to explain: {request.topic}")
    response = "Explain Like I'm Five Placeholder Response!"
    logger.info("Agent returned response")
    return {"response": response}
