import typer

app = typer.Typer()


@app.command()
def add(company: str, role: str, source: str = "other"):
    print("Adding application", company, role, source)


@app.command()
def list():
    print("Listing applications")


@app.command()
def remove(application_id: str):
    print("Removing application", application_id)


@app.command()
def update(application_id: str):
    print("Updating application", application_id)
