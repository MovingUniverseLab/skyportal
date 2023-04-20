"""localizatintilepartitions

Revision ID: fdab0cc9eb78
Revises: 47a76ff0f3ce
Create Date: 2023-04-19 09:08:38.281780

"""
from alembic import op
import sqlalchemy as sa
import healpix_alchemy

# revision identifiers, used by Alembic.
revision = 'fdab0cc9eb78'
down_revision = '47a76ff0f3ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'localizationtiles',
        sa.Column(
            'dateobs',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("'2023-01-01'::date"),
        ),
    )

    # add the dateobs to the primary key
    op.execute('ALTER TABLE localizationtiles DROP CONSTRAINT localizationtiles_pkey')
    # rename localizationtiles to localizationtiles_def
    op.execute('ALTER TABLE localizationtiles RENAME TO localizationtiles_def')

    # rename also the indexes
    op.execute(
        'ALTER INDEX ix_localizationtiles_created_at RENAME TO localizationtiles_def_created_at_idx'
    )
    op.execute(
        'ALTER INDEX ix_localizationtiles_probdensity RENAME TO localizationtiles_def_probdensity_idx'
    )
    op.execute(
        'ALTER INDEX ix_localizationtiles_healpix RENAME TO localizationtiles_def_healpix_idx'
    )
    op.execute(
        'ALTER INDEX ix_localizationtiles_localization_id RENAME TO localizationtiles_def_localization_id_idx'
    )
    # drop it now
    op.execute('DROP INDEX localizationtile_id_healpix_index')
    op.create_index(
        'localizationtiles_def_id_dateobs_healpix_idx',
        'localizationtiles_def',
        ['id', 'dateobs', 'healpix'],
        unique=True,
    )
    # edit the foreign key constraint
    op.execute(
        'ALTER TABLE localizationtiles_def DROP CONSTRAINT localizationtiles_localization_id_fkey'
    )
    op.execute(
        'ALTER TABLE localizationtiles_def ADD CONSTRAINT localizationtiles_def_localization_id_fkey FOREIGN KEY (localization_id) REFERENCES localizations (id) ON DELETE CASCADE'
    )
    op.execute(
        'ALTER TABLE localizationtiles_def ADD PRIMARY KEY (id, localization_id, dateobs, healpix)'
    )
    # edit the sequence
    op.execute(
        'ALTER SEQUENCE localizationtiles_id_seq RENAME TO localizationtiles_def_id_seq'
    )

    # create localizationtiles partition table
    op.execute(
        'CREATE SEQUENCE localizationtiles_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        '''CREATE TABLE localizationtiles (
            id INTEGER NOT NULL DEFAULT nextval('localizationtiles_id_seq'::regclass),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            localization_id INTEGER NOT NULL,
            probdensity FLOAT NOT NULL,
            dateobs TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT '2023-01-01'::DATE
            ) PARTITION BY RANGE (dateobs)
            '''
    )
    op.execute('ALTER SEQUENCE localizationtiles_id_seq OWNED BY localizationtiles.id')

    # add the healpix column to the partition table
    op.add_column(
        'localizationtiles',
        sa.Column('healpix', healpix_alchemy.types.Tile(), nullable=False),
    )

    # add foreign key constraint on localization_id
    op.execute(
        'ALTER TABLE localizationtiles ADD CONSTRAINT localizationtiles_localization_id_fkey FOREIGN KEY (localization_id) REFERENCES localizations (id) ON DELETE CASCADE'
    )

    # add index on created_at
    op.create_index(
        'localizationtiles_created_at_idx',
        'localizationtiles',
        ['created_at'],
        unique=False,
    )
    # add index on probdensity
    op.create_index(
        'localizationtiles_probdensity_idx',
        'localizationtiles',
        ['probdensity'],
        unique=False,
    )
    # add index on localization_id
    op.create_index(
        'localizationtiles_localization_id_idx',
        'localizationtiles',
        ['localization_id'],
        unique=False,
    )
    # add index on healpix
    op.create_index(
        'localizationtiles_healpix_idx',
        'localizationtiles',
        ['healpix'],
        unique=False,
        postgresql_using='spgist',
    )
    # add an index on id, dateobs and healpix
    op.create_index(
        'localizationtiles_id_dateobs_healpix_idx',
        'localizationtiles',
        ['id', 'dateobs', 'healpix'],
        unique=True,
    )

    # primary key on id, localization_id, dateobs, healpix
    op.execute(
        'ALTER TABLE localizationtiles ADD PRIMARY KEY (id, localization_id, dateobs, healpix)'
    )

    # attach the default partition (default range, when outside of all other ranges)
    op.execute(
        "ALTER TABLE localizationtiles ATTACH PARTITION localizationtiles_def DEFAULT"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_04 PARTITION OF localizationtiles FOR VALUES FROM ('2023-04-01') TO ('2023-05-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_05 PARTITION OF localizationtiles FOR VALUES FROM ('2023-05-01') TO ('2023-06-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_06 PARTITION OF localizationtiles FOR VALUES FROM ('2023-06-01') TO ('2023-07-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_07 PARTITION OF localizationtiles FOR VALUES FROM ('2023-07-01') TO ('2023-08-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_08 PARTITION OF localizationtiles FOR VALUES FROM ('2023-08-01') TO ('2023-09-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_09 PARTITION OF localizationtiles FOR VALUES FROM ('2023-09-01') TO ('2023-10-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_10 PARTITION OF localizationtiles FOR VALUES FROM ('2023-10-01') TO ('2023-11-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_11 PARTITION OF localizationtiles FOR VALUES FROM ('2023-11-01') TO ('2023-12-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2023_12 PARTITION OF localizationtiles FOR VALUES FROM ('2023-12-01') TO ('2024-01-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_01 PARTITION OF localizationtiles FOR VALUES FROM ('2024-01-01') TO ('2024-02-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_02 PARTITION OF localizationtiles FOR VALUES FROM ('2024-02-01') TO ('2024-03-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_03 PARTITION OF localizationtiles FOR VALUES FROM ('2024-03-01') TO ('2024-04-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_04 PARTITION OF localizationtiles FOR VALUES FROM ('2024-04-01') TO ('2024-05-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_05 PARTITION OF localizationtiles FOR VALUES FROM ('2024-05-01') TO ('2024-06-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_06 PARTITION OF localizationtiles FOR VALUES FROM ('2024-06-01') TO ('2024-07-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_07 PARTITION OF localizationtiles FOR VALUES FROM ('2024-07-01') TO ('2024-08-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_08 PARTITION OF localizationtiles FOR VALUES FROM ('2024-08-01') TO ('2024-09-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_09 PARTITION OF localizationtiles FOR VALUES FROM ('2024-09-01') TO ('2024-10-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_10 PARTITION OF localizationtiles FOR VALUES FROM ('2024-10-01') TO ('2024-11-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_11 PARTITION OF localizationtiles FOR VALUES FROM ('2024-11-01') TO ('2024-12-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2024_12 PARTITION OF localizationtiles FOR VALUES FROM ('2024-12-01') TO ('2025-01-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2025_01 PARTITION OF localizationtiles FOR VALUES FROM ('2025-01-01') TO ('2025-02-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2025_02 PARTITION OF localizationtiles FOR VALUES FROM ('2025-02-01') TO ('2025-03-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2025_03 PARTITION OF localizationtiles FOR VALUES FROM ('2025-03-01') TO ('2025-04-01')"
    )
    op.execute(
        "CREATE TABLE localizationtiles_2025_04 PARTITION OF localizationtiles FOR VALUES FROM ('2025-04-01') TO ('2025-05-01')"
    )

    # rename foreign key from localizationtiles_localization_id_fkey to localizationtiles_2023_04_localization_id_fkey
    op.execute(
        "ALTER TABLE localizationtiles_2023_04 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_04_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_05 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_05_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_06 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_06_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_07 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_07_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_08 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_08_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_09 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_09_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_10 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_10_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_11 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_11_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2023_12 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2023_12_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_01 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_01_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_02 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_02_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_03 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_03_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_04 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_04_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_05 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_05_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_06 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_06_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_07 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_07_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_08 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_08_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_09 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_09_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_10 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_10_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_11 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_11_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2024_12 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2024_12_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2025_01 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2025_01_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2025_02 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2025_02_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2025_03 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2025_03_localization_id_fkey"
    )
    op.execute(
        "ALTER TABLE localizationtiles_2025_04 RENAME CONSTRAINT localizationtiles_localization_id_fkey TO localizationtiles_2025_04_localization_id_fkey"
    )

    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_04_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_05_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_06_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_07_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_08_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_09_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_10_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_11_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2023_12_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_01_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_02_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_03_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_04_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_05_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_06_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_07_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_08_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_09_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_10_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_11_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2024_12_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2025_01_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2025_02_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2025_03_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )
    op.execute(
        'CREATE SEQUENCE localizationtiles_2025_04_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1'
    )

    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_04_id_seq OWNED BY localizationtiles_2023_04.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_05_id_seq OWNED BY localizationtiles_2023_05.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_06_id_seq OWNED BY localizationtiles_2023_06.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_07_id_seq OWNED BY localizationtiles_2023_07.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_08_id_seq OWNED BY localizationtiles_2023_08.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_09_id_seq OWNED BY localizationtiles_2023_09.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_10_id_seq OWNED BY localizationtiles_2023_10.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_11_id_seq OWNED BY localizationtiles_2023_11.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2023_12_id_seq OWNED BY localizationtiles_2023_12.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_01_id_seq OWNED BY localizationtiles_2024_01.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_02_id_seq OWNED BY localizationtiles_2024_02.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_03_id_seq OWNED BY localizationtiles_2024_03.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_04_id_seq OWNED BY localizationtiles_2024_04.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_05_id_seq OWNED BY localizationtiles_2024_05.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_06_id_seq OWNED BY localizationtiles_2024_06.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_07_id_seq OWNED BY localizationtiles_2024_07.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_08_id_seq OWNED BY localizationtiles_2024_08.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_09_id_seq OWNED BY localizationtiles_2024_09.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_10_id_seq OWNED BY localizationtiles_2024_10.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_11_id_seq OWNED BY localizationtiles_2024_11.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2024_12_id_seq OWNED BY localizationtiles_2024_12.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2025_01_id_seq OWNED BY localizationtiles_2025_01.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2025_02_id_seq OWNED BY localizationtiles_2025_02.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2025_03_id_seq OWNED BY localizationtiles_2025_03.id'
    )
    op.execute(
        'ALTER SEQUENCE localizationtiles_2025_04_id_seq OWNED BY localizationtiles_2025_04.id'
    )


def downgrade():

    # then we want to ingest the data of all the partitions into the default table
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_04'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_05'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_06'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_07'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_08'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_09'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_10'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_11'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2023_12'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_01'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_02'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_03'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_04'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_05'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_06'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_07'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_08'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_09'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_10'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_11'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2024_12'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2025_01'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2025_02'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2025_03'
    )
    op.execute(
        'INSERT INTO localizationtiles_def(localization_id, probdensity, healpix, created_at, modified, dateobs) SELECT localization_id, probdensity, healpix, created_at, modified, dateobs FROM localizationtiles_2025_04'
    )

    # then we want to drop the partitions
    op.execute('DROP TABLE localizationtiles_2023_04')
    op.execute('DROP TABLE localizationtiles_2023_05')
    op.execute('DROP TABLE localizationtiles_2023_06')
    op.execute('DROP TABLE localizationtiles_2023_07')
    op.execute('DROP TABLE localizationtiles_2023_08')
    op.execute('DROP TABLE localizationtiles_2023_09')
    op.execute('DROP TABLE localizationtiles_2023_10')
    op.execute('DROP TABLE localizationtiles_2023_11')
    op.execute('DROP TABLE localizationtiles_2023_12')
    op.execute('DROP TABLE localizationtiles_2024_01')
    op.execute('DROP TABLE localizationtiles_2024_02')
    op.execute('DROP TABLE localizationtiles_2024_03')
    op.execute('DROP TABLE localizationtiles_2024_04')
    op.execute('DROP TABLE localizationtiles_2024_05')
    op.execute('DROP TABLE localizationtiles_2024_06')
    op.execute('DROP TABLE localizationtiles_2024_07')
    op.execute('DROP TABLE localizationtiles_2024_08')
    op.execute('DROP TABLE localizationtiles_2024_09')
    op.execute('DROP TABLE localizationtiles_2024_10')
    op.execute('DROP TABLE localizationtiles_2024_11')
    op.execute('DROP TABLE localizationtiles_2024_12')
    op.execute('DROP TABLE localizationtiles_2025_01')
    op.execute('DROP TABLE localizationtiles_2025_02')
    op.execute('DROP TABLE localizationtiles_2025_03')
    op.execute('DROP TABLE localizationtiles_2025_04')

    # then we detach the partition from the parent table
    op.execute('ALTER TABLE localizationtiles DETACH PARTITION localizationtiles_def')

    # we remove the index on the partitioned table
    op.drop_index('localizationtiles_created_at_idx', table_name='localizationtiles')
    op.drop_index('localizationtiles_probdensity_idx', table_name='localizationtiles')
    op.drop_index(
        'localizationtiles_localization_id_idx', table_name='localizationtiles'
    )
    op.drop_index('localizationtiles_healpix_idx', table_name='localizationtiles')
    op.drop_index(
        'localizationtiles_id_dateobs_healpix_idx', table_name='localizationtiles'
    )

    # then we drop the partitioned table
    op.execute('DROP TABLE localizationtiles')

    # then we rename the default table to the original name
    op.execute('ALTER TABLE localizationtiles_def RENAME TO localizationtiles')

    # we rename the index on the default table to the original name
    op.execute(
        'ALTER INDEX localizationtiles_def_created_at_idx RENAME TO ix_localizationtiles_created_at'
    )
    op.execute(
        'ALTER INDEX localizationtiles_def_probdensity_idx RENAME TO ix_localizationtiles_probdensity'
    )
    op.execute(
        'ALTER INDEX localizationtiles_def_localization_id_idx RENAME TO ix_localizationtiles_localization_id'
    )
    op.execute(
        'ALTER INDEX localizationtiles_def_healpix_idx RENAME TO ix_localizationtiles_healpix'
    )
    op.execute(
        'ALTER INDEX localizationtiles_def_id_dateobs_healpix_idx RENAME TO ix_localizationtiles_id_dateobs_healpix'
    )

    # rename the old constraint foreign key
    op.execute(
        'ALTER TABLE localizationtiles RENAME CONSTRAINT localizationtiles_def_localization_id_fkey TO localizationtiles_localization_id_fkey'
    )

    # do the same for the primary key
    op.execute(
        'ALTER INDEX localizationtiles_def_pkey RENAME TO localizationtiles_pkey'
    )

    # we drop the index localizationtiles_id_dateobs_healpix_idx
    op.drop_index(
        'ix_localizationtiles_id_dateobs_healpix', table_name='localizationtiles'
    )

    # we drop the primary key
    op.drop_constraint('localizationtiles_pkey', 'localizationtiles', type_='primary')

    # we drop the dateobs column
    op.drop_column('localizationtiles', 'dateobs')

    # we recreate the index localizationtiles_id_healpix_idx
    op.create_index(
        'localizationtile_id_healpix_index',
        'localizationtiles',
        ['id', 'healpix'],
        unique=True,
    )

    # we recreate the primary key
    op.create_primary_key(
        'localizationtiles_pkey',
        'localizationtiles',
        ['id', 'localization_id', 'healpix'],
    )

    # rename the sequence
    op.execute(
        'ALTER SEQUENCE localizationtiles_def_id_seq RENAME TO localizationtiles_id_seq'
    )

    # change the default value of the id column
    op.alter_column(
        'localizationtiles',
        'id',
        existing_type=sa.INTEGER(),
        server_default=sa.text('nextval(\'localizationtiles_id_seq\'::regclass)'),
    )
