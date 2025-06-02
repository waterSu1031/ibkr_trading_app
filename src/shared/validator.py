from typing import Type, Optional, Union
from pydantic import BaseModel, ValidationError

def parse_to_model(data: Union[dict, BaseModel], model_class: Type[BaseModel]) -> Optional[BaseModel]:
    if isinstance(data, model_class):
        return data
    if isinstance(data, dict):
        try:
            return model_class(**data)
        except (ValidationError, TypeError) as e:
            print(f"[Pydantic] 모델 파싱 실패: {e}")
            return None
    print(f"[Pydantic] 지원하지 않는 타입: {type(data)}")
    return None