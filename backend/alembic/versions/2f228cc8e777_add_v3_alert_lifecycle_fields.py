"""add_v3_alert_lifecycle_fields

Revision ID: 2f228cc8e777
Revises: 9076cb380459
Create Date: 2026-04-24 01:35:25.263573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2f228cc8e777'
down_revision: Union[str, None] = '9076cb380459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add nullable columns first
    op.add_column('alerts', sa.Column('location_accuracy', sa.Float(), nullable=True))
    op.add_column('alerts', sa.Column('location_method', sa.String(length=10), nullable=True))
    op.add_column('alerts', sa.Column('resolution_notes', sa.Text(), nullable=True))
    op.add_column('alerts', sa.Column('resolved_by', sa.UUID(), nullable=True))

    # 2. Add updated_at as NULLABLE to prevent crash on existing rows
    op.add_column('alerts', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

    op.add_column('alerts', sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('alerts', sa.Column('expired_at', sa.DateTime(timezone=True), nullable=True))

    # 3. Backfill existing rows with the current timestamp
    op.execute("UPDATE alerts SET updated_at = NOW() WHERE updated_at IS NULL")

    # 4. NOW make it NOT NULL safely
    op.alter_column('alerts', 'updated_at', nullable=False)

    # 5. Add Foreign Key and drop old notes column
    op.create_foreign_key('fk_alerts_resolved_by', 'alerts', 'users', ['resolved_by'], ['id'])
    op.drop_column('alerts', 'notes')


def downgrade() -> None:
    op.add_column('alerts', sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_alerts_resolved_by', 'alerts', type_='foreignkey')
    op.drop_column('alerts', 'expired_at')
    op.drop_column('alerts', 'resolved_at')
    op.drop_column('alerts', 'updated_at')
    op.drop_column('alerts', 'resolved_by')
    op.drop_column('alerts', 'resolution_notes')
    op.drop_column('alerts', 'location_method')
    op.drop_column('alerts', 'location_accuracy')