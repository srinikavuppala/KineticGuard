"""add_alert_profile_column

Revision ID: 36f4d08f4e28
Revises: 2f228cc8e777
Create Date: 2026-04-24 21:39:48.516787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '36f4d08f4e28'
down_revision: Union[str, None] = '2f228cc8e777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the enum type
    op.execute(
        "CREATE TYPE gestureprofile AS ENUM ('DEFAULT', 'HEALTHCARE', 'TEACHER', 'DELIVERY', 'CORPORATE', 'ELDERLY')")

    # 2. Add column as NULLABLE first (so existing rows don't crash)
    op.add_column('alerts', sa.Column('gesture_profile',
                                      sa.Enum('DEFAULT', 'HEALTHCARE', 'TEACHER', 'DELIVERY', 'CORPORATE', 'ELDERY',
                                              name='gestureprofile'), nullable=True))

    # 3. Fill existing rows with 'DEFAULT'
    op.execute("UPDATE alerts SET gesture_profile = 'DEFAULT' WHERE gesture_profile IS NULL")

    # 4. NOW make it NOT NULL
    op.alter_column('alerts', 'gesture_profile', nullable=False)

    # 5. Add the new renamed ml_model_version column
    op.add_column('alerts', sa.Column('ml_model_version', sa.String(length=50), nullable=True))

    # 6. Drop the old model_version column
    op.drop_column('alerts', 'model_version')


def downgrade() -> None:
    # 1. Restore the old model_version column
    op.add_column('alerts', sa.Column('model_version', sa.String(length=20), nullable=True))

    # 2. Drop the gesture_profile column
    op.drop_column('alerts', 'gesture_profile')

    # 3. Drop the enum type
    op.execute("DROP TYPE gestureprofile")

    # 4. Drop the renamed ml_model_version column
    op.drop_column('alerts', 'ml_model_version')