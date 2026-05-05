# SchemaForge

A schema-first database toolkit for FastAPI, inspired by Prisma-like developer experience.

SchemaForge is experimental. The current version only includes:

- `schemaforge init`
- minimal schema parsing
- Pydantic v2 schema generation

It is not a full ORM yet.

## Quickstart

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

## Current scope

- Generates `ModelCreate`
- Generates `ModelUpdate`
- Generates `ModelRead`

## Out of scope for now

- database client
- migrations
- relationships
- SQLAlchemy/Alembic integration
