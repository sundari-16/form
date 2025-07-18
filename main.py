import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sql_connect():
    return mysql.connector.connect(
        host="yn061m.h.filess.io",
        user="office_simplestgo",
        password="41e04b4edd462ce603bbece2e3938cfddc607023",
        database="office_simplestgo",
        port=3307
    )

class Item(BaseModel):
    Name: str
    phno: str
    email: str
    password: str

@app.post("/reg")
def user(data: Item):
    mydb = sql_connect()
    mypost = mydb.cursor()
    mypost.execute(
        "insert into user (name, phno, email, password) values ('"
        + data.Name + "', '" + data.phno + "', '" + data.email + "', '" + data.password + "')"
    )
    mydb.commit()
    mydb.close()
    return {"message": "registered successfully"}


class LoginItem(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(data: LoginItem):
    mydb = sql_connect()
    mypost = mydb.cursor()
    mypost.execute(
        "select * from user where email='" + data.email + "' AND password='" + data.password + "'"
    )
    r = mypost.fetchall()
    mydb.close()
    if r:
        return {"message": "Success"}
    else:
        return {"message": "Invalid"}

@app.get("/view")
def view():
    mydb = sql_connect()
    mypost = mydb.cursor(dictionary=True)
    mypost.execute("select * from user")
    r = mypost.fetchall()
    mydb.close()
    return r


class UpdateItem(BaseModel):
    name: str

@app.post("/update/{id}")
def update(data: UpdateItem, id: int):
    mydb = sql_connect()
    mypost = mydb.cursor()
    mypost.execute("update user set name='" + data.name + "' where id=" + str(id))
    mydb.commit()
    mydb.close()
    return {"message": "Updated"}


@app.delete("/del/{id}")
def delete(id: int):
    mydb = sql_connect()
    mypost = mydb.cursor()
    mypost.execute("delete from user where id=" + str(id))
    mydb.commit()
    mydb.close()
    return {"message": "Deleted"}
