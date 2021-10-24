"""revision_name

Revision ID: c26e704cd5ae
Revises: f31c7d486f1f
Create Date: 2021-10-23 10:22:40.576469

"""
from alembic import op
from sqlalchemy.dialects import postgresql as pgsql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e26e704cd5ae'
down_revision = 'f31c7d486f1f'
branch_labels = ('qm9_v1',)
depends_on = None


def upgrade():
    op.create_table(
        "molecule",
        sa.Column("molecule_id", pgsql.UUID, primary_key=True, nullable=False),
        sa.Column("created_on", sa.DateTime, nullable=False),
        sa.Column("updated_on", sa.DateTime, nullable=False),
        sa.Column("homo", sa.Float, nullable=True),
        sa.Column("lumo", sa.Float, nullable=True),
        sa.Column("cv", sa.Float, nullable=True),
        sa.Column("u0_atom", sa.Float, nullable=True),
        schema="public",
    )


def downgrade():
    op.drop_table("molecule")
