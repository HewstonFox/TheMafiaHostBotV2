from typing import TypedDict, Union

_Primitives = Union[str, int, float, bool]
ErrorContextValues = Union[_Primitives, list['ErrorContextValues'], 'ErrorContext']
ErrorContext = dict[str, 'ErrorContextValues']


class Error(TypedDict):
    id: int
    error: str
    trace: list[str]
    context: ErrorContext
