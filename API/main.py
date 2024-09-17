from router.news import comment, favorite, files, post
from fastapi import FastAPI
from router import auth


app = FastAPI(title="NEWS API")


app.include_router(router=auth.router)
app.include_router(router=post.router)
app.include_router(router=comment.router)
app.include_router(router=favorite.router)
app.include_router(router=files.router)


