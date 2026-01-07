# FastAPI CRUD Application with MongoDB

A backend RESTful API developed using FastAPI and MongoDB.  
It demonstrates how to perform basic CRUD (Create, Read, Update, Delete) operations using an asynchronous Python framework.

---

## Key Highlights
- REST API built with FastAPI
- CRUD operations for managing data
- Asynchronous database interaction using MongoDB
- Input validation using Pydantic models
- Clean and modular project structure

---

## Technologies Used
- Python
- FastAPI
- MongoDB
- Motor (Async MongoDB Client)
- Pydantic
- MongoDB Compass

---

## API Validation & Testing
- All API endpoints were tested using **Postman**
- MongoDB Compass was used to verify database records
- API documentation is auto-generated using Swagger UI

---

## Getting Started

### Prerequisites
- Python 3.9+
- MongoDB installed and running

---

### Steps to Run the Project

1. **Start MongoDB service**
   - net start MongoDB
2. **Install libraries**
   - pip install -r requirements.txt
3. **Run the server**
   - uvicorn app.main:app --reload
4. **Access API documentation**
   - http://127.0.0.1:8000/docs
