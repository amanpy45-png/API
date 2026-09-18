from fastapi import FastAPI, HTTPException
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


# @app.get("/jobs/{job_id}")
# def get_job(job_id: int):
#     for job in jobs:
#         if job['id'] == job_id:
#             return job
#     raise HTTPException(
#         status_code = 404,
#         detail = 'Job not found'
#     )

class JobResponse(BaseModel):
    id: int
    company: str
    role : str


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    for job in jobs:
        if job['id'] == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )


class Job(BaseModel):
    id : int
    company : str
    role : str

@app.post("/jobs", status_code=201)
def create_job(job : Job):
    # Convert Pydantic model to dict and append to the list
    jobs.append(job.model_dump())
    return job


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    for index, job in enumerate(jobs):
        if job['id'] == job_id:
            deleted_job = jobs.pop(index)
            return {"message": f"Job deleted: {deleted_job['company']}"}

    raise HTTPException(
        status_code = 404,
        detail = 'Job not found'
    )



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
    raise HTTPException(status_code=404, detail="Job not found")
