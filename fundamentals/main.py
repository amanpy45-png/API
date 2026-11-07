from fastapi import FastAPI

app = FastAPI()

tasks = [
    {"project": "TaskFlow", "developer": "Aman", "version": "1.0"}
]

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/about")
def about():
    return {
        "project": "TaskFlow",
        "developer": "Aman",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks/count")
def total_tasks():
    return {"total_tasks": len(tasks)}


