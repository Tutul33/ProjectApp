from pydantic import BaseModel
from typing import List, Type, TypeVar

T = TypeVar("T", bound=BaseModel)

# ----------------------------
# DTO Mapping
# ----------------------------
def map_to_dto(dto_class: Type[T], entity: object) -> T:
    """Map single entity → DTO"""
    return dto_class.model_validate(entity.__dict__)

def map_list_to_dto(dto_class: Type[T], entities: List[object]) -> List[T]:
    """Map list of entities → list of DTOs"""
    return [dto_class.model_validate(e.__dict__) for e in entities]

# ----------------------------
# Entity Mapping
# ----------------------------
def map_to_entity(entity_class: type, dto: BaseModel) -> object:
    """Map single DTO → Entity"""
    return entity_class(**dto.model_dump())

def map_list_to_entity(entity_class: type, dtos: List[BaseModel]) -> List[object]:
    """Map list of DTOs → list of Entities"""
    return [entity_class(**d.model_dump()) for d in dtos]
