from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from functions import crud
from views import models, schemas
from connection.connection import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Only for redirect when the server is started
@app.get("/", status_code=status.HTTP_200_OK)
def index():
    return RedirectResponse(url="/docs", status_code=status.HTTP_200_OK)


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_200_OK)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    userCreated = crud.create_user(db=db, user=user)
    return userCreated


@app.get("/users/", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    itemCreated = crud.create_user_item(db=db, item=item, user_id=user_id)
    return itemCreated


@app.get("/items/", response_model=list[schemas.Item], status_code=status.HTTP_200_OK)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/items/{user_id}", response_model=list[schemas.Item], status_code=status.HTTP_200_OK)
def read_items_by_user_id(user_id: int, db: Session = Depends(get_db)):
    items = crud.get_item_by_user_id(db, user_id)
    return items


@app.put("/items/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: schemas.ItemModify, db: Session = Depends(get_db)):
    db_item = crud.modify_item(db, item, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.modify_user(db, user, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_201_CREATED)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_deleted = crud.remove_user(db, user_id)
    if not user_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User deleted"})


@app.delete("/items/{item_id}", response_model=None, status_code=status.HTTP_201_CREATED)
def delete_user(item_id: int, db: Session = Depends(get_db)):
    item_deleted = crud.remove_item(db, item_id)
    if not item_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Item deleted"})


@app.post('/login', response_model=None, status_code=status.HTTP_202_ACCEPTED)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    login_check = crud.login(db, user)
    if not login_check:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "User successfully logged"})

