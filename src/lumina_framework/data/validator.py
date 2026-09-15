"""Validación de datos contra un contrato confirmado."""

import pandas as pd

from lumina_framework.core.contracts import DatasetContract, ValidationResult


class DataValidator:
    """Observa incumplimientos estructurales sin corregirlos."""

    def validate(
        self,
        data: pd.DataFrame,
        contract: DatasetContract,
    ) -> ValidationResult:
        """Compara columnas, llave y fecha con el contrato declarado."""
        available = set(data.columns)
        missing = tuple(column for column in contract.columns if column not in available)
        exact_duplicates = int(data.duplicated().sum())

        key_duplicates: int | None = None
        if contract.identifier_columns and all(
            column in available for column in contract.identifier_columns
        ):
            key_duplicates = int(
                data.duplicated(subset=list(contract.identifier_columns)).sum()
            )

        invalid_dates: int | None = None
        if contract.date_column and contract.date_column in available:
            converted = pd.to_datetime(data[contract.date_column], errors="coerce")
            invalid_dates = int(converted.isna().sum())

        valid = not missing and (invalid_dates in (None, 0))
        return ValidationResult(
            valid=valid,
            missing_columns=missing,
            exact_duplicates=exact_duplicates,
            key_duplicates=key_duplicates,
            invalid_dates=invalid_dates,
        )

