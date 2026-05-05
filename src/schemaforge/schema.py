from __future__ import annotations

from dataclasses import dataclass
import re


SCALAR_TYPES = {"String", "Text", "Int", "Boolean", "UUID", "DateTime"}
ATTRIBUTES = {"@id", "@unique", "@default(uuid())", "@default(now())"}


class SchemaParseError(ValueError):
    """Raised when a schemaforge.schema file cannot be parsed."""


@dataclass(frozen=True)
class Field:
    name: str
    type_name: str
    optional: bool
    attributes: tuple[str, ...]

    @property
    def has_default(self) -> bool:
        return any(attribute.startswith("@default(") for attribute in self.attributes)


@dataclass(frozen=True)
class Model:
    name: str
    fields: tuple[Field, ...]


_MODEL_START_RE = re.compile(r"^model\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$")
_FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z][A-Za-z0-9_]*)(\?)?(?:\s+(.*))?$")


def parse_schema(source: str) -> tuple[Model, ...]:
    lines = _strip_comments(source)
    models: list[Model] = []
    model_names: set[str] = set()
    index = 0

    while index < len(lines):
        line_number, line = lines[index]
        if not line:
            index += 1
            continue

        match = _MODEL_START_RE.match(line)
        if match is None:
            raise SchemaParseError(f"Line {line_number}: expected 'model Name {{'.")

        model_name = match.group(1)
        if model_name in model_names:
            raise SchemaParseError(f"Line {line_number}: duplicate model '{model_name}'.")

        index += 1
        fields: list[Field] = []
        field_names: set[str] = set()

        while index < len(lines):
            field_line_number, field_line = lines[index]
            index += 1

            if not field_line:
                continue
            if field_line == "}":
                break

            field = _parse_field(field_line_number, field_line)
            if field.name in field_names:
                raise SchemaParseError(
                    f"Line {field_line_number}: duplicate field '{field.name}' in model '{model_name}'."
                )
            fields.append(field)
            field_names.add(field.name)
        else:
            raise SchemaParseError(f"Line {line_number}: model '{model_name}' is missing a closing brace.")

        if not fields:
            raise SchemaParseError(f"Line {line_number}: model '{model_name}' must contain at least one field.")

        models.append(Model(name=model_name, fields=tuple(fields)))
        model_names.add(model_name)

    if not models:
        raise SchemaParseError("Schema must contain at least one model.")

    return tuple(models)


def _strip_comments(source: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.split("//", 1)[0].split("#", 1)[0].strip()
        lines.append((line_number, line))
    return lines


def _parse_field(line_number: int, line: str) -> Field:
    match = _FIELD_RE.match(line)
    if match is None:
        raise SchemaParseError(f"Line {line_number}: invalid field syntax.")

    name, type_name, optional_marker, attributes_source = match.groups()
    if type_name not in SCALAR_TYPES:
        raise SchemaParseError(f"Line {line_number}: unsupported field type '{type_name}'.")

    attributes = tuple(attributes_source.split()) if attributes_source else ()
    for attribute in attributes:
        if attribute not in ATTRIBUTES:
            raise SchemaParseError(f"Line {line_number}: unsupported attribute '{attribute}'.")

    if len(set(attributes)) != len(attributes):
        raise SchemaParseError(f"Line {line_number}: duplicate attributes are not allowed.")

    return Field(
        name=name,
        type_name=type_name,
        optional=optional_marker == "?",
        attributes=attributes,
    )
