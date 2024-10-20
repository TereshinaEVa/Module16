from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main_page():
    return {'Главная страница'}


@app.get("/user/admin")
async def admin_page():
    return {"Вы вошли как администратор"}


@app.get("/user/{user_id}")
async def user_id_page():
    return {'Вы вошли как пользователь {user_id}'}

@app.get("/user")
async def user_name_age(username: str, age: int):
    return {f'Информация о пользователе. Имя: {username}, Возраст {age}'}