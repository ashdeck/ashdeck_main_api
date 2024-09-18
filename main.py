from fastapi import FastAPI
from auth.routes import router as auth
from block_lists.routes import router as block_lists
from sessions.routes import router as sessions
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/", status_code=200)
async def welcome():
    return {"detail": "Welcome to website Blocker"}


app.include_router(auth, prefix="/auth", tags=["Authentication"])
app.include_router(block_lists, prefix="/blocklists", tags=["Block Lists"])
app.include_router(sessions, prefix="/sessions", tags=["Sessions"])


handler = Mangum(app, lifespan="off")
