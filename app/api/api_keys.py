from fastapi import APIRouter
from pydantic import BaseModel
from app.core.api_key_manager import generate_api_key
from app.core.api_key_manager import revoke_api_key


router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"]
)


class APIKeyRequest(BaseModel):
    company_name: str


@router.post("/generate")
def create_api_key(request: APIKeyRequest):
    api_key = generate_api_key(request.company_name)

    return {
        "company_name": request.company_name,
        "api_key": api_key
    }

@router.delete("/revoke/{api_key}")
def delete_api_key(api_key: str):
    revoke_api_key(api_key)

    return {
        "message": "API key revoked successfully",
        "api_key": api_key
    }
