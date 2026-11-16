import typer
from database import transaction
from error import ResourceNotFoundError, ValidationError
from rich.console import Console
from rich.table import Table
from service import resume_service

app = typer.Typer()
console = Console()


@app.command()
def add(resume_type_name: str):
    try:
        with transaction() as conn:
            resume_type = resume_service.create_resume_type(conn, resume_type_name)
    except (ValidationError, RuntimeError) as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    console.print("Successfully created resume type", resume_type.id)


@app.command()
def list():
    try:
        with transaction() as conn:
            resume_types = resume_service.list_resume_types(conn)
    except ResourceNotFoundError as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    table = Table(title="Resume Types")
    table.add_column("ID")
    table.add_column("Name")

    for resume_type in resume_types:
        table.add_row(
            str(resume_type.id),
            resume_type.name,
        )

    console.print(table)


@app.command()
def remove(resume_type_id: str) -> None:
    try:
        with transaction() as conn:
            resume_service.remove_resume_type(conn, int(resume_type_id))
    except ResourceNotFoundError as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    console.print("Successfully removed resume type", resume_type_id)


@app.command()
def update(resume_type_id: str, resume_type_name: str):
    try:
        with transaction() as conn:
            updated_resume_type = resume_service.update_resume_type(
                conn, int(resume_type_id), resume_type_name
            )
    except RuntimeError as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1) from e

    console.print("Successfully updated resume type", updated_resume_type.id)
