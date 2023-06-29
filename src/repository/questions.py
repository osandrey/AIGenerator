from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from sqlalchemy import and_
from src.database.db import get_db
from src.database.models import Question, User
from src.schemas import QuestionModel, QuestionResponse


async def get_questions(skip: int, limit: int, user: User, db: Session) -> List[Question]:
    return db.query(Question).filter(Question.user_id==user.id).offset(skip).limit(limit).all()




# async def find_contacts_bday(days, user: User, db: Session) -> List[Question]:
#     date_now = datetime.now().date()
#     delta = days
#     end_date = date_now + timedelta(days=delta)
#     bdays_list = []
#     all_contacts = db.query(Question).filter(Question.user_id==user.id).all()
#     for contact in all_contacts:
#         contact_bday_this_year = contact.date_of_birth.replace(year=date_now.year)
#         # print(date_now, contact_bday_this_year, end_date, sep='\n')
#         if date_now <= contact_bday_this_year <= end_date:
#             bdays_list.append(contact)
#     return bdays_list


# async def find_questions(
#         db: Session,
#         user: User,
#         # firstname: str = None,
#         # lastname: str = None,
#         # email: str = None,
#
# ) -> List[Question]:
#     query = db.query(Question).filter(Question.user_id==user.id)
#
#     # if firstname:
#     #     query = query.filter(Question.firstname.ilike(f"%{firstname}%"))
#     # if lastname:
#     #     query = query.filter(Question.lastname.ilike(f"%{lastname}%"))
#     # if email:
#     #     query = query.filter(Question.email.ilike(f"%{email}%"))
#
#     contact = query.all()
#     return contact


async def get_question(question_id: int, user: User, db: Session) -> Type[Question] | None:
    return db.query(Question).filter(and_(Question.id == question_id, Question.user_id == user.id)).first()


async def create_question(body: QuestionResponse, user: User, db: Session):
    question = QuestionResponse(
        answer=body.response,
        question=body.question,
        user_id=user.id
        )

    db.add(question)
    db.commit()
    db.refresh(question)
    return question


async def remove_question(question_id: int, user: User, db: Session) -> Question | None:
    question = db.query(Question).filter(and_(Question.id == question_id, Question.user_id==user.id)).first()
    if question:
        db.delete(question)
        db.commit()
    return question
#
#
# async def update_contact(contact_id: int, user: User, body: ContactUpdate, db: Session) -> Contact | None:
#     contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id==user.id)).first()
#     if contact:
#         contact.firstname = body.firstname
#         contact.lastname = body.lastname
#         contact.phone_number = body.phone_number
#         contact.email = body.email
#         contact.date_of_birth = body.date_of_birth
#         contact.description = body.description
#
#         db.commit()
#     return contact