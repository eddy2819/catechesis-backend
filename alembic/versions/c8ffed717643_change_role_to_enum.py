"""change role to enum"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c8ffed717643'
down_revision: Union[str, Sequence[str], None] = '34d14c346846'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Definir ENUM explícitamente
userrole_enum = sa.Enum(
    'admin',
    'parroco',
    'catequista',
    'secretario',
    'auxiliar',
    name='userrole'
)


def upgrade() -> None:
    # 1️⃣ Crear tipo ENUM en PostgreSQL
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Convertir columna usando CAST
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::userrole"
    )


def downgrade() -> None:
    # 1️⃣ Volver a VARCHAR
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(20)"
    )

    # 2️⃣ Eliminar tipo ENUM
    userrole_enum.drop(op.get_bind(), checkfirst=True)