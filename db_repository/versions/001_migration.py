from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
gs_repository_accessed = Table('gs_repository_accessed', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('url', VARCHAR(length=64)),
    Column('date', DATETIME),
)

gs_repository_accessed = Table('gs_repository_accessed', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=64)),
    Column('acessDate', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gs_repository_accessed'].columns['date'].drop()
    post_meta.tables['gs_repository_accessed'].columns['acessDate'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gs_repository_accessed'].columns['date'].create()
    post_meta.tables['gs_repository_accessed'].columns['acessDate'].drop()
