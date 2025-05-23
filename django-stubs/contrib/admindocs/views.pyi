from collections.abc import Callable, Iterable
from re import Pattern
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db.models.fields import Field
from django.db.models.options import Options
from django.urls import _AnyURL
from django.views.generic import TemplateView

MODEL_METHODS_EXCLUDE: Any

class BaseAdminDocsView(TemplateView): ...
class BookmarkletsView(BaseAdminDocsView): ...
class TemplateTagIndexView(BaseAdminDocsView): ...
class TemplateFilterIndexView(BaseAdminDocsView): ...
class ViewIndexView(BaseAdminDocsView): ...
class ViewDetailView(BaseAdminDocsView): ...

def user_has_model_view_permission(user: AbstractBaseUser | AnonymousUser, opts: Options) -> bool: ...

class ModelIndexView(BaseAdminDocsView): ...
class ModelDetailView(BaseAdminDocsView): ...
class TemplateDetailView(BaseAdminDocsView): ...

def get_return_data_type(func_name: Any) -> str: ...
def get_readable_field_data_type(field: Field | str) -> str: ...
def extract_views_from_urlpatterns(
    urlpatterns: Iterable[_AnyURL], base: str = ..., namespace: str | None = ...
) -> list[tuple[Callable, Pattern[str], str | None, str | None]]: ...
def simplify_regex(pattern: str) -> str: ...
