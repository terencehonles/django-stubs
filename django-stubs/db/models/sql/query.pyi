import collections
from collections import namedtuple
from collections.abc import Iterable, Iterator, Sequence
from typing import Any, Literal

from django.db.backends.utils import CursorWrapper
from django.db.models import Field, FilteredRelation, Model, Q
from django.db.models.expressions import BaseExpression, Combinable, Expression, OrderBy
from django.db.models.lookups import Lookup, Transform
from django.db.models.options import Options
from django.db.models.query_utils import PathInfo
from django.db.models.sql.datastructures import BaseTable, Join
from django.db.models.sql.where import WhereNode
from django.utils.functional import cached_property

JoinInfo = namedtuple("JoinInfo", ("final_field", "targets", "opts", "joins", "path", "transform_function"))

class RawQuery:
    high_mark: int | None
    low_mark: int | None
    params: Any
    sql: str
    using: str
    extra_select: dict[Any, Any]
    annotation_select: dict[Any, Any]
    cursor: CursorWrapper | None
    def __init__(self, sql: str, using: str, params: Any = ()) -> None: ...
    def chain(self, using: str) -> RawQuery: ...
    def clone(self, using: str) -> RawQuery: ...
    def get_columns(self) -> list[str]: ...
    def __iter__(self) -> Iterator[Any]: ...
    @property
    def params_type(self) -> type[dict | tuple] | None: ...

class Query(BaseExpression):
    related_ids: list[int] | None
    related_updates: dict[type[Model], list[tuple[Field, None, int | str]]]
    values: list[Any]
    alias_prefix: str
    subq_aliases: frozenset[Any]
    compiler: str
    base_table_class: type[BaseTable]
    model: type[Model] | None
    alias_refcount: dict[str, int]
    alias_map: dict[str, BaseTable | Join]
    external_aliases: dict[str, bool]
    table_map: dict[str, list[str]]
    default_cols: bool
    default_ordering: bool
    standard_ordering: bool
    used_aliases: set[str]
    where: WhereNode
    filter_is_sticky: bool
    subquery: bool
    group_by: None | Sequence[Combinable] | Sequence[str] | Literal[True]
    order_by: Sequence[Any]
    distinct: bool
    distinct_fields: tuple[str, ...]
    select: Sequence[BaseExpression]
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_skip_locked: bool
    select_for_update_of: tuple
    select_for_no_key_update: bool
    select_related: dict[str, Any] | bool
    max_depth: int
    join_class: type[Join]
    values_select: tuple
    selected: dict[str, int | str | Expression] | None
    annotation_select_mask: list[str] | None
    combinator: str | None
    combinator_all: bool
    combined_queries: tuple
    extra_select_mask: set[str] | None
    extra_tables: tuple
    extra_order_by: Sequence[Any]
    deferred_loading: tuple[set[str] | frozenset[str], bool]
    explain_query: bool
    explain_format: str | None
    explain_options: dict[str, int]
    high_mark: int | None
    low_mark: int
    extra: dict[str, Any]
    annotations: dict[str, Expression]
    empty_result_set_value: Any | None
    explain_info: Any | None
    def __init__(self, model: type[Model] | None, alias_cols: bool = True) -> None: ...
    @property
    def output_field(self) -> Field: ...
    @property
    def has_select_fields(self) -> bool: ...
    @cached_property
    def base_table(self) -> str: ...
    def add_annotation(self, annotation: Any, alias: str, select: bool = True) -> None: ...
    def sql_with_params(self) -> tuple[str, tuple]: ...
    def __deepcopy__(self, memo: dict[int, Any]) -> Query: ...
    def get_compiler(
        self, using: str | None = None, connection: Any | None = None, elide_empty: bool = True
    ) -> Any: ...
    def join_parent_model(self, opts: Any, model: Any | None, alias: str, seen: dict[Any, str]) -> str: ...
    def names_to_path(
        self, names: list[str], opts: Any, allow_many: bool = True, fail_on_missing: bool = False
    ) -> tuple[list[Any], Any, tuple[Any, ...], list[str]]: ...
    def get_meta(self) -> Options: ...
    def clone(self) -> Query: ...
    def chain(self, klass: type[Query] | None = None) -> Query: ...
    def get_count(self, using: str) -> int: ...
    def get_group_by_cols(self, wrapper: Any | None = None) -> list[Any]: ...
    def has_filters(self) -> WhereNode: ...
    def get_external_cols(self) -> list[Any]: ...
    def exists(self, limit: bool = True) -> Any: ...
    def has_results(self, using: str) -> bool: ...
    def explain(self, using: str, format: str | None = None, **options: Any) -> str: ...
    def combine(self, rhs: Query, connector: str) -> None: ...
    def ref_alias(self, alias: str) -> None: ...
    def unref_alias(self, alias: str, amount: int = 1) -> None: ...
    def promote_joins(self, aliases: Iterable[str]) -> None: ...
    def demote_joins(self, aliases: Iterable[str]) -> None: ...
    def reset_refcounts(self, to_counts: dict[str, int]) -> None: ...
    def check_alias(self, alias: str) -> None: ...
    def check_related_objects(self, field: Any, value: Any, opts: Any) -> None: ...
    def check_query_object_type(self, value: Any, opts: Any, field: Any) -> None: ...
    def change_aliases(self, change_map: dict[str | None, str]) -> None: ...
    def bump_prefix(self, other_query: Query, exclude: Any | None = None) -> None: ...
    def get_initial_alias(self) -> str: ...
    def count_active_tables(self) -> int: ...
    def resolve_expression(self, query: Query, *args: Any, **kwargs: Any) -> Query: ...  # type: ignore[override]
    def resolve_lookup_value(
        self, value: Any, can_reuse: set[str] | None, allow_joins: bool, summarize: bool = False
    ) -> Any: ...
    def solve_lookup_type(
        self, lookup: str, summarize: bool = False
    ) -> tuple[Sequence[str], Sequence[str], Expression | Literal[False]]: ...
    def table_alias(
        self, table_name: str, create: bool = False, filtered_relation: Any | None = None
    ) -> tuple[str, bool]: ...
    def get_aggregation(self, using: Any, aggregate_exprs: dict[str, Any]) -> dict[str, Any]: ...
    def build_filter(
        self,
        filter_expr: Q | Expression | dict[str, str] | tuple[str, Any],
        branch_negated: bool = False,
        current_negated: bool = False,
        can_reuse: set[str] | None = None,
        allow_joins: bool = True,
        split_subq: bool = True,
        check_filterable: bool = True,
        summarize: bool = False,
        update_join_types: bool = True,
    ) -> tuple[WhereNode, Iterable[str]]: ...
    def add_select_col(self, col: Any, name: str) -> None: ...
    def add_filter(self, filter_lhs: tuple[str, Any], filter_rhs: tuple[str, Any]) -> None: ...
    def add_q(self, q_object: Q, reuse_all: bool = False) -> None: ...
    def build_where(self, filter_expr: Q | Expression | dict[str, str] | tuple[str, Any]) -> WhereNode: ...
    def add_filtered_relation(self, filtered_relation: FilteredRelation, alias: str) -> None: ...
    def setup_joins(
        self,
        names: Sequence[str],
        opts: Any,
        alias: str,
        can_reuse: set[str] | None = None,
        allow_many: bool = True,
    ) -> JoinInfo: ...
    def trim_joins(
        self, targets: tuple[Field, ...], joins: list[str], path: list[PathInfo]
    ) -> tuple[tuple[Field, ...], str, list[str]]: ...
    def resolve_ref(
        self, name: str, allow_joins: bool = True, reuse: set[str] | None = None, summarize: bool = False
    ) -> Expression: ...
    def split_exclude(
        self,
        filter_expr: tuple[str, Any],
        can_reuse: set[str],
        names_with_path: list[tuple[str, list[PathInfo]]],
    ) -> tuple[WhereNode, Iterable[str]]: ...
    def set_empty(self) -> None: ...
    def is_empty(self) -> bool: ...
    def set_limits(self, low: int | None = None, high: int | None = None) -> None: ...
    def clear_limits(self) -> None: ...
    @property
    def is_sliced(self) -> bool: ...
    def has_limit_one(self) -> bool: ...
    def can_filter(self) -> bool: ...
    def clear_select_clause(self) -> None: ...
    def clear_select_fields(self) -> None: ...
    def set_select(self, cols: list[Expression]) -> None: ...
    def add_distinct_fields(self, *field_names: Any) -> None: ...
    def add_fields(self, field_names: Iterable[str], allow_m2m: bool = True) -> None: ...
    def add_ordering(self, *ordering: str | OrderBy) -> None: ...
    def clear_where(self) -> None: ...
    def clear_ordering(self, force: bool = False, clear_default: bool = True) -> None: ...
    def set_group_by(self, allow_aliases: bool = True) -> None: ...
    def add_select_related(self, fields: Iterable[str]) -> None: ...
    def add_extra(
        self,
        select: dict[str, Any] | None,
        select_params: Iterable[Any] | None,
        where: Sequence[str] | None,
        params: Sequence[str] | None,
        tables: Sequence[str] | None,
        order_by: Sequence[str] | None,
    ) -> None: ...
    def clear_deferred_loading(self) -> None: ...
    def add_deferred_loading(self, field_names: Iterable[str]) -> None: ...
    def add_immediate_loading(self, field_names: Iterable[str]) -> None: ...
    def get_select_mask(self) -> dict[str, Any]: ...
    def set_annotation_mask(self, names: Iterable[str] | None) -> None: ...
    def append_annotation_mask(self, names: Iterable[str]) -> None: ...
    def set_extra_mask(self, names: Iterable[str] | None) -> None: ...
    def set_values(self, fields: Iterable[str] | None) -> None: ...
    @property
    def annotation_select(self) -> dict[str, Any]: ...
    @property
    def extra_select(self) -> dict[str, Any]: ...
    def trim_start(self, names_with_path: list[tuple[str, list[PathInfo]]]) -> tuple[str, bool]: ...
    def is_nullable(self, field: Field) -> bool: ...
    def check_filterable(self, expression: Any) -> None: ...
    def build_lookup(self, lookups: Sequence[str], lhs: Expression | Query, rhs: Any) -> Lookup: ...
    def try_transform(self, lhs: Expression | Query, name: str, lookups: Sequence[str] | None = ...) -> Transform: ...
    def join(
        self,
        join: BaseTable | Join,
        reuse: str | None = None,
    ) -> str: ...

class JoinPromoter:
    connector: str
    negated: bool
    effective_connector: str
    num_children: int
    votes: collections.Counter
    def __init__(self, connector: str, num_children: int, negated: bool) -> None: ...
    def add_votes(self, votes: Iterable[str]) -> None: ...
    def update_join_types(self, query: Query) -> set[str]: ...
