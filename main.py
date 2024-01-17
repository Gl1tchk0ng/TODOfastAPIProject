from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from typing import Optional
from starlette.requests import Request
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)
redis = get_redis_connection(
    host = 'redis-10637.c305.ap-south-1-1.ec2.cloud.redislabs.com',
    port =10637,
    password='5zK2ypxy5s5eST2aTlHgcY90rCAoCGlP',
    decode_responses=True
)


class Task(HashModel):
    name: str
    complete: Optional[bool] = 0

    class Meta:
        database= redis

@app.get("/tasks")
async def all():
    return [format(pk) for pk in Task.all_pks()]

def format(pk: str):
    task = Task.get(pk)

    return{
        'id': task.pk,
        'name': task.name,
        'complete': task.complete
    }
 

@app.post("/tasks")
async def create(task: Task):
    return task.save()


@app.put("/tasks/{pk}")
async def update(pk: str, request: Request):
    task = Task.get(pk)
    body = await request.json()
    task.complete = int(body['complete'])
    return task.save()


@app.delete("/tasks/{pk}")
async def delete(pk: str):
    task = Task.get(pk)
    return task.delete(pk)