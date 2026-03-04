from pydantic import BaseModel

class Private(BaseModel):
    user_id:int
    receiver_id:int
    message:str