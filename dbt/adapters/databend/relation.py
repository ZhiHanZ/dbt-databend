from dataclasses import dataclass
from typing import Optional

import dbt.exceptions
from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.contracts.relation import (
    Path
)

@dataclass
class DatabendQuotePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass
class DatabendIncludePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class DatabendRelation(BaseRelation):
    quote_policy: DatabendQuotePolicy = DatabendQuotePolicy()
    include_policy: DatabendIncludePolicy = DatabendIncludePolicy()
    quote_character: str = ""

    def __post_init__(self):
        if self.database != self.schema and self.database:
            raise dbt.exceptions.RuntimeException(
                f"Cannot set database {self.database} in databend!"
            )

    def render(self):
        if self.include_policy.database and self.include_policy.schema:
            raise dbt.exceptions.RuntimeException(
                "Got a databend relation with schema and database set to "
                "include, but only one can be set"
            )
        return super().render()
    @classmethod
    def get_path(cls, relation: BaseRelation, information_schema_view: Optional[str]) -> Path:
        return Path(
            database=relation.schema,
            schema=relation.schema,
            identifier="INFORMATION_SCHEMA",
        )