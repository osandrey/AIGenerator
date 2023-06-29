from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.services.text_utils import create_answer
from src.database.models import User
from src.schemas import QuestionResponse, QuestionModel, QuestionUpdate
#from src.schemas import QuestionResponseModel
from src.services import text_utils as repository_questions
from src.services.auth import auth_service


router = APIRouter(prefix='/text', tags=["Ai-generator"])

@router.get("/", response_model=List[QuestionResponse])
async def read_all_requests(skip: int = 0, limit: int = 100, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_questions.get_questions(skip, limit, user, db)
    return contacts


@router.post("/", response_model=QuestionResponse)
async def generate_answer(question: QuestionModel,
                          user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    response = await create_answer(question.response, user, db)

    return {"response": response, "question": question.response, "user_id": user.id}



# @router.post("/", response_model=QuestionResponseModel)
# async def generate_answer(question: QuestionModel,
#                           user: User = Depends(auth_service.get_current_user),
#                           db: Session = Depends(get_db)):
#     response = await create_answer(question.response, user, db)
#
#     return {"response": response}



@router.get("/{question_id}", response_model=QuestionResponse)
async def find_answer(question_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_questions.get_question(question_id, user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact



@router.put("/{question_id}", response_model=QuestionResponse)
async def update_contact(body: QuestionUpdate, question_id: int, user: User = Depends(auth_service.get_current_user),db: Session = Depends(get_db)):
    question = await repository_questions.update_question(question_id,user, body, db)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@router.delete("/{question_id}", response_model=QuestionResponse)
async def remove_contact(question_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    question = await repository_questions.remove_question(question_id, user, db)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return question