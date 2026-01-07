import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from bson import ObjectId

# Test Data
TEST_TODO = {"title": "Test Task", "description": "Test Description"}
UPDATE_TODO = {"title": "Updated", "description": "Updated", "is_completed": True}

@pytest.mark.asyncio
async def test_get_todos():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/", json=TEST_TODO)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        return data["id"]

@pytest.mark.asyncio
async def test_update_todo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create
        create_res = await client.post("/", json=TEST_TODO)
        todo_id = create_res.json()["id"]
        # Update
        update_res = await client.put(f"/{todo_id}", json=UPDATE_TODO)
        assert update_res.status_code == 200
        assert update_res.json()["message"] == "Task Updated Successfully"

@pytest.mark.asyncio
async def test_delete_todo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create
        create_res = await client.post("/", json=TEST_TODO)
        todo_id = create_res.json()["id"]
        # Delete
        delete_res = await client.delete(f"/{todo_id}")
        assert delete_res.status_code == 200
        assert delete_res.json()["message"] == "Task Deleted Successfully"

# Run all tests
if __name__ == "__main__":
    import asyncio
    async def main():
        await test_get_todos()
        await test_create_todo()
        await test_update_todo()
        await test_delete_todo()
        print("✅ All tests passed!")
    asyncio.run(main())