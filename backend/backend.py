
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

app = FastAPI()
FILE = "todos.json"

class Todo(BaseModel):
    title: str
    completed: bool = False

class UpdateTodo(BaseModel):
    title: str | None = None
    completed: bool | None = None

def load_todos():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)
    with open(FILE, "r") as f:
        return json.load(f)

def save_todos(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)

@app.get("/todos")
def get_todos():
    return {"success": True, "data": load_todos()}

@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    todos = load_todos()
    new = {
        "id": str(len(todos) + 1),
        "title": todo.title,
        "completed": todo.completed
    }
    todos.append(new)
    save_todos(todos)
    return {"success": True, "data": new}

@app.put("/todos/{todo_id}")
def update(todo_id: str, update: UpdateTodo):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            if update.title is not None:
                todo["title"] = update.title
            if update.completed is not None:
                todo["completed"] = update.completed
            save_todos(todos)
            return {"success": True, "data": todo}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete(todo_id: str):
    todos = load_todos()
    new_list = [t for t in todos if t["id"] != todo_id]
    if len(new_list) == len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    save_todos(new_list)
    return {"success": True, "message": "Todo deleted"}
