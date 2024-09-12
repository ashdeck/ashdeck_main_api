from fastapi import FastAPI
from auth.routes import router as auth
from block_lists.routes import router as block_lists


app = FastAPI()


@app.get("/", status_code=200)
async def welcome():
    return {"detail": "Welcome to website Blocker"}


app.include_router(auth, prefix="/auth", tags=["Authentication"])
app.include_router(block_lists, prefix="/block_lists", tags=["Block Lists"])
