# SchemaForge

A schema-first database toolkit for FastAPI, inspired by Prisma-like developer experience.

SchemaForge is experimental. The current version includes:

- `schemaforge init`
- minimal schema parsing
- Pydantic v2 schema generation

It is not a full ORM yet.

## Installation

### With uv

    uv add git+https://github.com/masamarux/schemaforge.git

### With pip

    python -m pip install git+https://github.com/masamarux/schemaforge.git

## Quickstart

    uv run schemaforge init
    uv run schemaforge generate

If you are not using `uv`, run:

    schemaforge init
    schemaforge generate

## Example schema

    model User {
      id UUID @id @default(uuid())
      email String @unique
      name String
      bio Text?
      created_at DateTime @default(now())
    }

## Generated output

SchemaForge generates Pydantic v2 models in:

    app/db/generated/schemas.py

The current generator creates:

- `ModelCreate`
- `ModelUpdate`
- `ModelRead`

## Current scope

- Initializes a `schemaforge.schema` file
- Initializes a `schemaforge.toml` file
- Parses minimal `model` blocks
- Supports scalar fields:
  - `String`
  - `Text`
  - `Int`
  - `Boolean`
  - `UUID`
  - `DateTime`
- Supports optional fields with `?`
- Supports basic attributes:
  - `@id`
  - `@unique`
  - `@default(uuid())`
  - `@default(now())`
- Generates Pydantic v2 schemas

## Out of scope for now

- database client
- migrations
- relationships
- SQLAlchemy/Alembic integration
- FastAPI dependency injection
- query builder
- database connections

## Status

SchemaForge is an early prototype. The goal is to explore a cleaner, schema-first database workflow for Python backends.
