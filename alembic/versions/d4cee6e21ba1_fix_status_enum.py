"""fix status enum

Revision ID: d4cee6e21ba1
Revises: 60f0aa73cb5e
Create Date: 2025-11-15 16:00:32.315186
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4cee6e21ba1'
down_revision: Union[str, Sequence[str], None] = '60f0aa73cb5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Crear ENUM correctamente antes de usarlo
    catechist_status_enum = sa.Enum(
        'activo',
        'inactivo',
        'retirado',
        name='catechiststatus'
    )
    catechist_status_enum.create(op.get_bind(), checkfirst=True)

    # Agregar columna usando el ENUM
    op.add_column(
        'catechists',
        sa.Column(
            'status',
            catechist_status_enum,
            nullable=False,
            server_default='activo'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar columna
    op.drop_column('catechists', 'status')

    # Eliminar ENUM
    catechist_status_enum = sa.Enum(
        name='catechiststatus'
    )
    catechist_status_enum.drop(op.get_bind(), checkfirst=True)
