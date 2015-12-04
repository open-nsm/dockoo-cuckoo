"""processing column

Revision ID: 070cd314622
Revises: 1070cd314621
Create Date: 2015-12-02 00:57:32.068872

"""

# revision identifiers, used by Alembic.
revision = "1070cd314622"
down_revision = "1070cd314621"

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("tasks", sa.Column("docker_images", sa.String(length=256), nullable=True))

def downgrade():
    op.drop_column("docker_images")