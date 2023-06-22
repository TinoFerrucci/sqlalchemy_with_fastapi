from sqlalchemy.orm import Session
from views import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_by_user_id(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def modify_item(db: Session, item: schemas.ItemModify, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db_item.title = item.title
    db_item.description = item.description
    db_item.owner_id = item.owner_id
    db.commit()
    db.refresh(db_item)
    return db_item


def modify_user(db: Session, user: schemas.UserBase, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        return False
    user.delete()
    db.commit()
    return True


def remove_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id)
    if not item.first():
        return False
    item.delete()
    db.commit()
    return True
