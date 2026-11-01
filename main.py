from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="TaskAPI")


class TaskCreate(BaseModel):
    title: str


tasks: dict[int, dict] = {}
next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title}
    tasks[next_id] = new_task
    next_id += 1
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]