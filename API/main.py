from fastapi import FastAPI, Depends
from router import auth, post, comment, favorite, files


app = FastAPI(title="NEWS API")


app.include_router(router=auth.router)
app.include_router(router=post.router)
app.include_router(router=comment.router)
app.include_router(router=favorite.router)
app.include_router(router=files.router)


