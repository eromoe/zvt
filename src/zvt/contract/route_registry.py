# -*- coding: utf-8 -*-
"""
Route registry: maps (provider, db_name) -> storage_id.
Phase 1: uses deterministic rule storage_id = "{provider}_{db_name}".
Later: can be extended to read from config.
"""
from typing import Optional, Type

from sqlalchemy.ext.declarative import DeclarativeMeta


def _get_db_name_from_context(data_schema) -> Optional[str]:
    """Resolve db_name for a schema from zvt_context.dbname_map_base."""
    from zvt.contract import zvt_context
    for db_name, base in zvt_context.dbname_map_base.items():
        if issubclass(data_schema, base):
            return db_name
    return None


class RouteRegistry:
    """
    Maps (provider, db_name) or (provider, data_schema) to storage_id.
    Phase 1: storage_id = "{provider}_{db_name}".
    """

    def get_storage_id(self, provider: str, db_name: str) -> str:
        """
        Get storage_id for (provider, db_name).
        Current rule: storage_id = "{provider}_{db_name}".
        """
        return f"{provider}_{db_name}"

    def get_storage_id_for_schema(
        self, provider: str, data_schema: Type = None, db_name: str = None
    ) -> str:
        """
        Get storage_id for (provider, data_schema) or (provider, db_name).
        :param provider: Data provider name.
        :param data_schema: Schema class (used to resolve db_name if db_name is None).
        :param db_name: DB name. If provided, data_schema is ignored.
        :return: storage_id string.
        """
        if db_name is None:
            db_name = _get_db_name_from_context(data_schema)
        if db_name is None:
            raise ValueError(f"Cannot resolve db_name for schema {data_schema}")
        return self.get_storage_id(provider, db_name)


# Default instance; can be replaced for custom routing
_default_route_registry: Optional[RouteRegistry] = None


def get_route_registry() -> RouteRegistry:
    """Get the default route registry."""
    global _default_route_registry
    if _default_route_registry is None:
        _default_route_registry = RouteRegistry()
    return _default_route_registry


def set_route_registry(registry: RouteRegistry):
    """Replace default route registry. Useful for tests."""
    global _default_route_registry
    _default_route_registry = registry


__all__ = [
    "RouteRegistry",
    "get_route_registry",
    "set_route_registry",
]
