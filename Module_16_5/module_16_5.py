from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int = None
    username: str
    age: int

users = []


def get_user_id(user_id):
    new_id = 0
    for ind in range(len(users)):
        if users[ind].id == user_id:
            new_id = ind
            break
    if new_id != 0:
        return new_id
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} was not found")


@app.get("/")
async def get_all_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get("/user/{user_id}")
async def get_users(request: Request, user_id: int):
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User {user_id} was not found")


@app.post('/user/{username}/{age}')
async def post_user(username: str, age: int):
    user_id = users[-1].id + 1 if users != [] else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    try:
        user_ind = get_user_id(user_id)
        users[user_ind] = User(id=user_id, username=username, age=age)
        return users[user_id]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User {user_id} was not found")


@app.delete('/user/{user_id}')
async def del_user(user_id: int):
    if user_id == users[user_id - 1].id:
        return users.pop(user_id - 1)
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} was not found")