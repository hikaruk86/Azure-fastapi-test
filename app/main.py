from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番ではワイルドカードは避ける
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBセッションを自動クローズするDependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)
