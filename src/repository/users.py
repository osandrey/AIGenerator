from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.services.avatar_generator import generate_avatar



async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()





async def create_user(body: UserModel, db: Session) -> User:
    print(body)
    avatar = None
    try:
        ai_avatar = generate_avatar(body)
        if ai_avatar:
            avatar = ai_avatar
        else:
            g = Gravatar(body.email)
            avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()