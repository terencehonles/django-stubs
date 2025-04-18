import datetime
from decimal import Decimal
from typing import Any, Literal, TypeGuard, TypeVar, overload

from django.utils.functional import Promise

class DjangoUnicodeDecodeError(UnicodeDecodeError):
    obj: bytes
    def __init__(self, obj: bytes, *args: Any) -> None: ...

_P = TypeVar("_P", bound=Promise)
_S = TypeVar("_S", bound=str)
_B = TypeVar("_B", bound=bytes)
_PT = TypeVar("_PT", None, int, float, Decimal, datetime.datetime, datetime.date, datetime.time)

@overload
def smart_str(s: _P, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> _P: ...
@overload
def smart_str(s: _S, encoding: str = "utf-8", *, errors: str = "strict") -> _S: ...
@overload
def smart_str(s: Any, encoding: str = "utf-8", *, errors: str = "strict") -> str: ...
@overload
def smart_str(s: _PT, encoding: str = "utf-8", strings_only: Literal[True] = True, errors: str = "strict") -> _PT: ...
@overload
def smart_str(s: _S, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> _S: ...
@overload
def smart_str(s: Any, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> str: ...
def is_protected_type(obj: Any) -> TypeGuard[_PT]: ...
@overload
def force_str(s: _S, encoding: str = "utf-8", *, errors: str = "strict") -> _S: ...
@overload
def force_str(s: Any, encoding: str = "utf-8", *, errors: str = "strict") -> str: ...
@overload
def force_str(s: _PT, encoding: str = "utf-8", strings_only: Literal[True] = True, errors: str = "strict") -> _PT: ...
@overload
def force_str(s: _S, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> _S: ...
@overload
def force_str(s: Any, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> str: ...
@overload
def smart_bytes(s: _P, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> _P: ...
@overload
def smart_bytes(s: _B, encoding: Literal["utf-8"] = "utf-8", *, errors: str = "strict") -> _B: ...
@overload
def smart_bytes(s: Any, encoding: str = "utf-8", *, errors: str = "strict") -> bytes: ...
@overload
def smart_bytes(s: _PT, encoding: str = "utf-8", strings_only: Literal[True] = True, errors: str = "strict") -> _PT: ...
@overload
def smart_bytes(s: Any, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> bytes: ...
@overload
def force_bytes(s: _B, encoding: Literal["utf-8"] = "utf-8", *, errors: str = "strict") -> _B: ...
@overload
def force_bytes(s: Any, encoding: str = "utf-8", *, errors: str = "strict") -> bytes: ...
@overload
def force_bytes(s: _PT, encoding: str = "utf-8", strings_only: Literal[True] = True, errors: str = "strict") -> _PT: ...
@overload
def force_bytes(s: Any, encoding: str = "utf-8", strings_only: bool = False, errors: str = "strict") -> bytes: ...
@overload
def iri_to_uri(iri: None) -> None: ...
@overload
def iri_to_uri(iri: str | Promise) -> str: ...
@overload
def uri_to_iri(uri: None) -> None: ...
@overload
def uri_to_iri(uri: Any) -> str: ...
def escape_uri_path(path: str) -> str: ...
def punycode(domain: str) -> str: ...
def repercent_broken_unicode(path: bytes) -> bytes: ...
@overload
def filepath_to_uri(path: None) -> None: ...
@overload
def filepath_to_uri(path: str) -> str: ...
def get_system_encoding() -> str: ...

DEFAULT_LOCALE_ENCODING: str
