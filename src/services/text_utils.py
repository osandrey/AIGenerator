
from typing import List, Type

import openai  # for using GPT and getting embeddings
from deep_translator import GoogleTranslator

from dotenv import dotenv_values
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User, Question
from src.schemas import QuestionUpdate, QuestionResponse


config = dotenv_values(".env")
openai.api_key = config.get("GTPAPIKEY")
GPT_MODEL = "gpt-3.5-turbo"


async def get_questions(skip: int, limit: int, user: User, db: Session) -> List[Question]:
    return db.query(Question).filter(Question.user_id==user.id).offset(skip).limit(limit).all()



async def get_question(question_id: int, user: User, db: Session) -> Type[Question] | None:
    return db.query(Question).filter(and_(Question.id == question_id, Question.user_id == user.id)).first()




async def create_question(body: QuestionResponse, user: User, db: Session):
    # translate(data, language)

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


async def update_question(contact_id: int, user: User, body: QuestionUpdate, db: Session) -> Question | None:
    question = db.query(Question).filter(and_(Question.id == contact_id, Question.user_id==user.id)).first()
    if question:
        question.question = body.question
        question.response = body.response
        question.user_id = body.user_id
        db.commit()
    return question


def translate(data, language):
    translated = GoogleTranslator(source='auto', target=language).translate(data)
    return translated


async def create_answer(question: str, language: str, user: User, db: Session) -> str|None:
    print(config.get("GTPAPIKEY"))
    print(language)

    try:
        completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are famous comic!"},
                {"role": "user", "content": question},
            ],
            temperature=0.8,
        )
        text = completion.choices[0].message.content
        tranlated_text = translate(text, language)
        question_db = Question(
            response=tranlated_text,
            question=question,
            user_id=user.id
        )
        db.add(question_db)
        db.commit()
        db.refresh(question_db)
    except ValueError as er:
        print(er)
        text = "ERROR"
    print(tranlated_text)
    return tranlated_text



async def create_say_answer(question: str, language: str) -> str|None:
    print(config.get("GTPAPIKEY"))
    print(language)
    try:
        completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are famous comic!"},
                {"role": "user", "content": question},
            ],
            temperature=0.8,
        )
        text = completion.choices[0].message.content
        tranlated_text = translate(text, language)
    except ValueError as er:
        print(er)
        tranlated_text = "ERROR"
    print(tranlated_text)
    return tranlated_text

# if __name__ == '__main__':
#     asyncio.run(create_answer('Who is Putin?'))