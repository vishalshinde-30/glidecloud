from fastapi import FastAPI, APIRouter, HTTPException
from app.configrations import collection
from app.database.schemas import all_tasks
from app.database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI(title="Todo API", version="1.0.0")
router = APIRouter()

@router.get("/", response_model=list)
async def get_todos():
    return all_tasks(collection.find({"is_deleted": False}))

@router.post("/")
async def create_todo(task: Todo):
    try:
        result = collection.insert_one(task.dict())
        return {"status": 200, "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(500, f"Error: {e}")

@router.put("/{id}")
async def update_todo(id: str, task: Todo):
    try:
        obj_id = ObjectId(id)
        if not collection.find_one({"_id": obj_id, "is_deleted": False}):
            raise HTTPException(404, "Todo not found")
        task.updated_at = int(datetime.now().timestamp())
        collection.update_one({"_id": obj_id}, {"$set": task.dict()})
        return {"status": 200, "message": "Updated"}
    except Exception as e:
        raise HTTPException(500, f"Error: {e}")

@router.delete("/{id}")
async def delete_todo(id: str):
    try:
        obj_id = ObjectId(id)
        if not collection.find_one({"_id": obj_id, "is_deleted": False}):
            raise HTTPException(404, "Todo not found")
        collection.update_one({"_id": obj_id}, {"$set": {"is_deleted": True}})
        return {"status": 200, "message": "Deleted"}
    except Exception as e:
        raise HTTPException(500, f"Error: {e}")

app.include_router(router)