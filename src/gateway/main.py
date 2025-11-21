from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Mock authentication for initial implementation
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "testuser"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get(f"{settings.API_V1_STR}/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are authenticated", "user": current_user}
