from typing import List, NewType, Any

from pydantic import BaseModel


Process = NewType("Process", Any)


class ProcessResult(BaseModel):
    action: bool
    processes: List[Process]


__all__ = ["Process", "ProcessResult"]
