"""Limpieza controlada por reglas explícitas."""

from collections.abc import Mapping

import pandas as pd

from lumina_framework.core.contracts import CleaningChange, CleaningResult
from lumina_framework.core.exceptions import SchemaConfigurationError


class DataCleaner:
    """Aplica únicamente transformaciones solicitadas por configuración."""

    def clean(
        self,
        data: pd.DataFrame,
        *,
        remove_exact_duplicates: bool = False,
        rename_columns: Mapping[str, str] | None = None,
    ) -> CleaningResult:
        """Devuelve una copia y una bitácora de cada cambio aplicado."""
        cleaned = data.copy(deep=True)
        changes: list[CleaningChange] = []

        if rename_columns:
            absent = sorted(set(rename_columns) - set(cleaned.columns))
            if absent:
                raise SchemaConfigurationError(
                    "Las columnas de origen no existen: " + ", ".join(absent)
                )
            cleaned = cleaned.rename(columns=dict(rename_columns))
            changes.append(
                CleaningChange(
                    rule="rename_columns",
                    affected_rows=len(cleaned),
                    details=f"Se renombraron {len(rename_columns)} columnas.",
                )
            )

        if remove_exact_duplicates:
            before = len(cleaned)
            cleaned = cleaned.drop_duplicates().reset_index(drop=True)
            removed = before - len(cleaned)
            changes.append(
                CleaningChange(
                    rule="remove_exact_duplicates",
                    affected_rows=removed,
                    details="Se eliminaron únicamente duplicados exactos.",
                )
            )

        return CleaningResult(data=cleaned, changes=tuple(changes))

