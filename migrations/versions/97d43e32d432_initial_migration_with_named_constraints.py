"""Initial migration with named constraints

Revision ID: 2b5446ec2296
Revises:
Create Date: 2025-07-22 08:50:00.123456
"""

from alembic import op
import sqlalchemy as sa

revision = '2b5446ec2296'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'rol_usuario',
        sa.Column('id_rol', sa.Integer(), nullable=False),
        sa.Column('nombre_rol', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id_rol', name='pk_rol_usuario')
    )
    op.create_table(
        'usuario',
        sa.Column('id_usuario', sa.Integer(), nullable=False),
        sa.Column('nombres', sa.String(length=100), nullable=False),
        sa.Column('apellidos', sa.String(length=100), nullable=False),
        sa.Column('documento', sa.String(length=20), nullable=False),
        sa.Column('correo', sa.String(length=120), nullable=False),
        sa.Column('telefono', sa.String(length=20), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('id_rol', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id_usuario', name='pk_usuario'),
        sa.UniqueConstraint('documento', name='uq_usuario_documento'),
        sa.UniqueConstraint('correo', name='uq_usuario_correo'),
        sa.ForeignKeyConstraint(['id_rol'], ['rol_usuario.id_rol'], name='fk_usuario_rol')
    )

def downgrade():
    op.drop_table('usuario')
    op.drop_table('rol_usuario')