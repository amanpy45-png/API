from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

jobs = [
    {"id": 1, "company": "Celebal Tech", "role": "Data Engineer"},
    {"id": 2, "company": "Juspay", "role": "Backend Developer"},
    {"id": 3, "company": "Infosys", "role": "System Engineer"},
]

@app.get("/jobs")
def get_jobs():
    return jobs


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    for job in jobs:
        if job['id'] == job_id:
            return job
    return {'message': 'Job not found'}


class Job(BaseModel):
    id : int
    company : str
    role : str

@app.post("/jobs")
def create_job(job : Job):
    jobs.append(job.model_dump())
    return job


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    for index, job in enumerate(jobs):
        if job['id'] == job_id:
            deleted_job = jobs.pop(index)
            return {"message": f"Job deleted: {deleted_job['company']}"}

    return {'message': "Job not found"}


class JobUpdate(BaseModel):
    company: str
    role: str


@app.put("/jobs/{job_id}")
def update_job(job_id: int, updated_data: JobUpdate):
    for job in jobs:
        if job['id'] == job_id:
            job['company'] = updated_data.company
            job['role'] = updated_data.role

            return {
                'message': 'Job updated successfully',
                'job': job
            }
    return {"message": "Job not found"}

    
