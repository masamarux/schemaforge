from pathlib import Path

import typer

from schemaforge.generator import generate_pydantic_schemas
from schemaforge.schema import SchemaParseError, parse_schema

app = typer.Typer(help="SchemaForge CLI", invoke_without_command=False)

SCHEMA_PATH = Path("schemaforge.schema")
CONFIG_PATH = Path("schemaforge.toml")
GENERATED_DIR = Path("app/db/generated")
SCHEMAS_PATH = GENERATED_DIR / "schemas.py"

DEFAULT_SCHEMA = """model User {
  id UUID @id @default(uuid())
  email String @unique
  name String
  bio Text?
  created_at DateTime @default(now())
}
"""

DEFAULT_CONFIG = """[schemaforge]
schema = "schemaforge.schema"
output = "app/db/generated"
"""


@app.command()
def hello() -> None:
    """Smoke test command."""
    typer.echo("SchemaForge is alive")


@app.command()
def version() -> None:
    """Show SchemaForge version."""
    typer.echo("0.1.0")


@app.command()
def init(force: bool = typer.Option(False, "--force", help="Overwrite existing SchemaForge files.")) -> None:
    """Initialize SchemaForge files in the current project."""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Ensured directory: {GENERATED_DIR.as_posix()}")

    for path, content in ((SCHEMA_PATH, DEFAULT_SCHEMA), (CONFIG_PATH, DEFAULT_CONFIG)):
        if path.exists() and not force:
            typer.echo(f"Skipped existing file: {path} (use --force to overwrite)")
            continue

        action = "Overwrote" if path.exists() else "Created"
        path.write_text(content, encoding="utf-8")
        typer.echo(f"{action} file: {path}")

    typer.echo("SchemaForge project initialized.")


@app.command()
def generate() -> None:
    """Generate Pydantic schemas from schemaforge.schema."""
    if not SCHEMA_PATH.exists():
        typer.echo("Missing schemaforge.schema. Run 'schemaforge init' first.", err=True)
        raise typer.Exit(1)

    try:
        models = parse_schema(SCHEMA_PATH.read_text(encoding="utf-8"))
    except SchemaParseError as exc:
        typer.echo(f"Invalid schema: {exc}", err=True)
        raise typer.Exit(1) from exc

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMAS_PATH.write_text(generate_pydantic_schemas(models), encoding="utf-8")
    typer.echo(f"Generated Pydantic schemas: {SCHEMAS_PATH.as_posix()}")
