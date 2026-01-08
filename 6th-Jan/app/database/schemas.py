def todo_serializer(todo):
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "completed": todo["is_completed"],
        "created_at": todo["created_at"],
        "updated_at": todo["updated_at"]
    }

def todos_serializer(todos):
    return [todo_serializer(todo) for todo in todos]