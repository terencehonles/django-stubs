from typing import Any

class OGRGeomType:
    wkb25bit: int = ...
    num: Any = ...
    def __init__(self, type_input: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    @property
    def name(self): ...
    @property
    def django(self): ...
    def to_multi(self) -> None: ...
