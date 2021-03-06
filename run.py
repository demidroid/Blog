import click
import os
from app import create_app


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    app = create_app('development')
    app.run(debug=True, host="0.0.0.0", port=os.environ.get('PORT', 5000))


@cli.command()
def create_table():
    from peewee_async import PooledPostgresqlDatabase
    from app.models import database, tables

    app = create_app('testing')
    database.initialize(PooledPostgresqlDatabase(**app.config.DATABASE))
    database.drop_tables(tables, safe=True)
    database.create_tables(tables, safe=True)


@cli.command()
def local():
    app = create_app('testing')
    app.run(debug=True)


if __name__ == '__main__':
    cli()
