from pydantic import BaseModel

class RoleCreate(BaseModel):
    #id: int #SQL
    id: str #Mongo
    name:str
    isActive:bool