from __future__ import annotations

import csv
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence
from xml.etree.ElementTree import Element, SubElement, ElementTree

from pydantic import BaseModel


class ModelToFile:
    BASE_DIR = Path("output")

    @staticmethod
    def _ensure_base_dir() -> None:
        ModelToFile.BASE_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _build_path(extension: str) -> Path:
        ModelToFile._ensure_base_dir()
        filename = f"{ModelToFile._timestamp()}.{extension}"
        return ModelToFile.BASE_DIR / filename

    @staticmethod
    def _serialize(obj: Any) -> dict[str, Any]:
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json")

        if is_dataclass(obj):
            return asdict(obj)

        raise TypeError(
            f"Unsupported type: {type(obj).__name__}. "
            "Expected a Pydantic BaseModel or a dataclass instance."
        )

    @staticmethod
    def _rows(models: Sequence[Any]) -> list[dict[str, Any]]:
        return [ModelToFile._serialize(model) for model in models]

    @staticmethod
    def to_json(models: Sequence[Any]) -> Path:
        path = ModelToFile._build_path("json")
        rows = ModelToFile._rows(models)

        with path.open("w", encoding="utf-8") as file:
            json.dump(rows, file, indent=4, ensure_ascii=False)

        return path

    @staticmethod
    def to_csv(models: Sequence[Any]) -> Path:
        if not models:
            raise ValueError("models não pode ser vazio")

        path = ModelToFile._build_path("csv")
        rows = ModelToFile._rows(models)

        normalized_rows = []
        headers = set()

        for row in rows:
            normalized = {}
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    normalized[key] = json.dumps(value, ensure_ascii=False)
                else:
                    normalized[key] = value
            normalized_rows.append(normalized)
            headers.update(normalized.keys())

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(headers))
            writer.writeheader()
            writer.writerows(normalized_rows)

        return path

    @staticmethod
    def to_xml(models: Sequence[Any]) -> Path:
        path = ModelToFile._build_path("xml")
        rows = ModelToFile._rows(models)

        root = Element("items")

        for row in rows:
            item = SubElement(root, "item")
            for key, value in row.items():
                child = SubElement(item, key)
                child.text = "" if value is None else str(value)

        tree = ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)

        return path