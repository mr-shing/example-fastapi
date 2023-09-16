from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, post, auth, vote

# Auto Generate tables from models, but I have alembic installed now
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {"Message": "Hello World"}
