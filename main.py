from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

# Create the FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create /api/register POST endpoint for user registration
@app.post("/api/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create /api/login POST endpoint for user authentication
@app.post("/api/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user and db_user.verify_password(user.password):
            return {"message": "Login successful"}
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create /api/posts GET endpoint to retrieve all published posts
@app.get("/api/posts")
async def get_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(models.Post).filter(models.Post.published == True).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```python