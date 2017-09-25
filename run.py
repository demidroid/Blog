import click
from app import create_app


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    app = create_app('development')
    app.run(
        debug=True
    )


@cli.command()
def create_table():
    from peewee_async import PooledPostgresqlDatabase
    from app.models import database, tables

    app = create_app('development')
    database.initialize(PooledPostgresqlDatabase(**app.config.DATABASE))
    database.drop_tables(tables, safe=True)
    database.create_tables(tables, safe=True)


if __name__ == '__main__':
    cli()
