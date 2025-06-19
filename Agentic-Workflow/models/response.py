from pydantic import BaseModel

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str
