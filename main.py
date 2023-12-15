from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, StreamingResponse
import io
from models import User, Image
from database import SessionLocal, Base, engine

metadata = MetaData()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/register', tags=['User_registration'])
async def register_user(file: UploadFile = File(...), name: str = Form(...), email: str = Form(...),
                        password: str = Form(...),
                        phone: str = Form(...), db: Session = Depends(get_db)):
    new_user = User(name=name, email=email, password=password, phone=phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    contents = await file.read()
    image = Image(data=contents, filename=file.filename, user_id=new_user.id)
    db.add(image)
    db.commit()
    db.refresh(image)


@app.get("/registered_details/{user_id}", response_class=JSONResponse)
def get_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        return f'Name:{user.name}, Email:{user.email}, Phone_number:{user.phone}'


@app.get("/get_image/{user_id}", response_class=JSONResponse)
def get_image(user_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.user_id == user_id).first()

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    content_type = f"image/{image.filename.split('.')[-1]}"
    image_stream = io.BytesIO(image.data)

    return StreamingResponse(image_stream, media_type=content_type)
