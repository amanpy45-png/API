from fastapi import FastAPI

app = FastAPI()

# path parameter
@app.get('/square/{number}')
def output(number : int):
    res = number ** 2
    return {'message': number,
            'square' : res}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


# query parameter
@app.get("/jobs")
def get_jobs(company: str, location: str):
    return {
        "company": company,
        "location": location
    }

# can use default if user doesn't provide company
@app.get("/jobs")
def get_jobs(company: str = "all"):
    return {"company": company}


@app.get('/user')
def get_user(name : str, age : int = 18):
    return{
        'name' : name,
        'age' : age
    }


