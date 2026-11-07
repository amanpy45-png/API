from fastapi import FastAPI

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn Python", "completed": True},
    {"id": 2, "title": "Learn FastAPI", "completed": False},
    {"id": 3, "title": "Build a project", "completed": False}
]

# path parameter
@app.get("/tasks/{task_id}")
def get_task(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return {"message": "Task not found"}



# query parameter
@app.get("/tasks/filter")
def filter_tasks(completed: bool):
    res = []

    for task in tasks:
        if task["completed"] == completed:
            res.append(task)
    return res



# optional query parameter
@app.get("/tasks/filter")
def filter_tasks(completed: bool | None = None):
    if completed is None:
        return tasks

    result = []

    for task in tasks:
        if task["completed"] == completed:
            result.append(task)

    return result



# Multiple query parameters

@app.get("/tasks")
def get_tasks(completed: bool | None = None, limit: int = 10):

    result = tasks

    if completed is not None:
        result = [
            task for task in result
            if task["completed"] == completed
        ]

    return result[:limit]
