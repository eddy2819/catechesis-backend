from alembic import op
import sqlalchemy as sa


revision = '60f0aa73cb5e'
down_revision = 'bdd9fede2331'
branch_labels = None
depends_on = None


def upgrade():
    # 1) Crear ENUM para PostgreSQL
    catechistrole = sa.Enum(
        'coordinador', 'catequista', 'secretario', 'auxiliar',
        name='catechistrole'
    )
    catechistrole.create(op.get_bind(), checkfirst=True)

    # 2) Agregar columna usando el ENUM recién creado
    op.add_column(
        'catechists',
        sa.Column('role', catechistrole, nullable=False, server_default='catequista')
    )

    # 3) Remover el default temporal
    op.alter_column('catechists', 'role', server_default=None)


def downgrade():
    op.drop_column('catechists', 'role')

    # Borrar ENUM
    catechistrole = sa.Enum(
        'coordinador', 'catequista', 'secretario', 'auxiliar',
        name='catechistrole'
    )
    catechistrole.drop(op.get_bind(), checkfirst=True)
