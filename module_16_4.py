from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int

users = []

@app.get("/users")
async def get_users():
    return users

@app.post('/user/{username}/{age}')
async def post_user(username: str, age: int):
    new_user = User(id=len(users) + 1, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    try:
        users[user_id - 1] = User(id=user_id, username=username, age=age)
        return users[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}')
async def del_user(user_id: int):
    if user_id == users[user_id - 1].id:
        return users.pop(user_id - 1)
    else:
        raise HTTPException(status_code=404, detail="User was not found")