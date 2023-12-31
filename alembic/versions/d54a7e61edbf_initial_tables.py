"""initial tables

Revision ID: d54a7e61edbf
Revises: 
Create Date: 2023-11-16 16:10:36.476132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd54a7e61edbf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('faces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('v0', sa.Float(), nullable=False),
    sa.Column('v1', sa.Float(), nullable=False),
    sa.Column('v2', sa.Float(), nullable=False),
    sa.Column('v3', sa.Float(), nullable=False),
    sa.Column('v4', sa.Float(), nullable=False),
    sa.Column('v5', sa.Float(), nullable=False),
    sa.Column('v6', sa.Float(), nullable=False),
    sa.Column('v7', sa.Float(), nullable=False),
    sa.Column('v8', sa.Float(), nullable=False),
    sa.Column('v9', sa.Float(), nullable=False),
    sa.Column('v10', sa.Float(), nullable=False),
    sa.Column('v11', sa.Float(), nullable=False),
    sa.Column('v12', sa.Float(), nullable=False),
    sa.Column('v13', sa.Float(), nullable=False),
    sa.Column('v14', sa.Float(), nullable=False),
    sa.Column('v15', sa.Float(), nullable=False),
    sa.Column('v16', sa.Float(), nullable=False),
    sa.Column('v17', sa.Float(), nullable=False),
    sa.Column('v18', sa.Float(), nullable=False),
    sa.Column('v19', sa.Float(), nullable=False),
    sa.Column('v20', sa.Float(), nullable=False),
    sa.Column('v21', sa.Float(), nullable=False),
    sa.Column('v22', sa.Float(), nullable=False),
    sa.Column('v23', sa.Float(), nullable=False),
    sa.Column('v24', sa.Float(), nullable=False),
    sa.Column('v25', sa.Float(), nullable=False),
    sa.Column('v26', sa.Float(), nullable=False),
    sa.Column('v27', sa.Float(), nullable=False),
    sa.Column('v28', sa.Float(), nullable=False),
    sa.Column('v29', sa.Float(), nullable=False),
    sa.Column('v30', sa.Float(), nullable=False),
    sa.Column('v31', sa.Float(), nullable=False),
    sa.Column('v32', sa.Float(), nullable=False),
    sa.Column('v33', sa.Float(), nullable=False),
    sa.Column('v34', sa.Float(), nullable=False),
    sa.Column('v35', sa.Float(), nullable=False),
    sa.Column('v36', sa.Float(), nullable=False),
    sa.Column('v37', sa.Float(), nullable=False),
    sa.Column('v38', sa.Float(), nullable=False),
    sa.Column('v39', sa.Float(), nullable=False),
    sa.Column('v40', sa.Float(), nullable=False),
    sa.Column('v41', sa.Float(), nullable=False),
    sa.Column('v42', sa.Float(), nullable=False),
    sa.Column('v43', sa.Float(), nullable=False),
    sa.Column('v44', sa.Float(), nullable=False),
    sa.Column('v45', sa.Float(), nullable=False),
    sa.Column('v46', sa.Float(), nullable=False),
    sa.Column('v47', sa.Float(), nullable=False),
    sa.Column('v48', sa.Float(), nullable=False),
    sa.Column('v49', sa.Float(), nullable=False),
    sa.Column('v50', sa.Float(), nullable=False),
    sa.Column('v51', sa.Float(), nullable=False),
    sa.Column('v52', sa.Float(), nullable=False),
    sa.Column('v53', sa.Float(), nullable=False),
    sa.Column('v54', sa.Float(), nullable=False),
    sa.Column('v55', sa.Float(), nullable=False),
    sa.Column('v56', sa.Float(), nullable=False),
    sa.Column('v57', sa.Float(), nullable=False),
    sa.Column('v58', sa.Float(), nullable=False),
    sa.Column('v59', sa.Float(), nullable=False),
    sa.Column('v60', sa.Float(), nullable=False),
    sa.Column('v61', sa.Float(), nullable=False),
    sa.Column('v62', sa.Float(), nullable=False),
    sa.Column('v63', sa.Float(), nullable=False),
    sa.Column('v64', sa.Float(), nullable=False),
    sa.Column('v65', sa.Float(), nullable=False),
    sa.Column('v66', sa.Float(), nullable=False),
    sa.Column('v67', sa.Float(), nullable=False),
    sa.Column('v68', sa.Float(), nullable=False),
    sa.Column('v69', sa.Float(), nullable=False),
    sa.Column('v70', sa.Float(), nullable=False),
    sa.Column('v71', sa.Float(), nullable=False),
    sa.Column('v72', sa.Float(), nullable=False),
    sa.Column('v73', sa.Float(), nullable=False),
    sa.Column('v74', sa.Float(), nullable=False),
    sa.Column('v75', sa.Float(), nullable=False),
    sa.Column('v76', sa.Float(), nullable=False),
    sa.Column('v77', sa.Float(), nullable=False),
    sa.Column('v78', sa.Float(), nullable=False),
    sa.Column('v79', sa.Float(), nullable=False),
    sa.Column('v80', sa.Float(), nullable=False),
    sa.Column('v81', sa.Float(), nullable=False),
    sa.Column('v82', sa.Float(), nullable=False),
    sa.Column('v83', sa.Float(), nullable=False),
    sa.Column('v84', sa.Float(), nullable=False),
    sa.Column('v85', sa.Float(), nullable=False),
    sa.Column('v86', sa.Float(), nullable=False),
    sa.Column('v87', sa.Float(), nullable=False),
    sa.Column('v88', sa.Float(), nullable=False),
    sa.Column('v89', sa.Float(), nullable=False),
    sa.Column('v90', sa.Float(), nullable=False),
    sa.Column('v91', sa.Float(), nullable=False),
    sa.Column('v92', sa.Float(), nullable=False),
    sa.Column('v93', sa.Float(), nullable=False),
    sa.Column('v94', sa.Float(), nullable=False),
    sa.Column('v95', sa.Float(), nullable=False),
    sa.Column('v96', sa.Float(), nullable=False),
    sa.Column('v97', sa.Float(), nullable=False),
    sa.Column('v98', sa.Float(), nullable=False),
    sa.Column('v99', sa.Float(), nullable=False),
    sa.Column('v100', sa.Float(), nullable=False),
    sa.Column('v101', sa.Float(), nullable=False),
    sa.Column('v102', sa.Float(), nullable=False),
    sa.Column('v103', sa.Float(), nullable=False),
    sa.Column('v104', sa.Float(), nullable=False),
    sa.Column('v105', sa.Float(), nullable=False),
    sa.Column('v106', sa.Float(), nullable=False),
    sa.Column('v107', sa.Float(), nullable=False),
    sa.Column('v108', sa.Float(), nullable=False),
    sa.Column('v109', sa.Float(), nullable=False),
    sa.Column('v110', sa.Float(), nullable=False),
    sa.Column('v111', sa.Float(), nullable=False),
    sa.Column('v112', sa.Float(), nullable=False),
    sa.Column('v113', sa.Float(), nullable=False),
    sa.Column('v114', sa.Float(), nullable=False),
    sa.Column('v115', sa.Float(), nullable=False),
    sa.Column('v116', sa.Float(), nullable=False),
    sa.Column('v117', sa.Float(), nullable=False),
    sa.Column('v118', sa.Float(), nullable=False),
    sa.Column('v119', sa.Float(), nullable=False),
    sa.Column('v120', sa.Float(), nullable=False),
    sa.Column('v121', sa.Float(), nullable=False),
    sa.Column('v122', sa.Float(), nullable=False),
    sa.Column('v123', sa.Float(), nullable=False),
    sa.Column('v124', sa.Float(), nullable=False),
    sa.Column('v125', sa.Float(), nullable=False),
    sa.Column('v126', sa.Float(), nullable=False),
    sa.Column('v127', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_vector_components', 'faces', ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', 'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'v27', 'v28', 'v29', 'v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39', 'v40', 'v41', 'v42', 'v43', 'v44', 'v45', 'v46', 'v47', 'v48', 'v49', 'v50', 'v51', 'v52', 'v53', 'v54', 'v55', 'v56', 'v57', 'v58', 'v59', 'v60', 'v61', 'v62', 'v63', 'v64', 'v65', 'v66', 'v67', 'v68', 'v69', 'v70', 'v71', 'v72', 'v73', 'v74', 'v75', 'v76', 'v77', 'v78', 'v79', 'v80', 'v81', 'v82', 'v83', 'v84', 'v85', 'v86', 'v87', 'v88', 'v89', 'v90', 'v91', 'v92', 'v93', 'v94', 'v95', 'v96', 'v97', 'v98', 'v99', 'v100', 'v101', 'v102', 'v103', 'v104', 'v105', 'v106', 'v107', 'v108', 'v109', 'v110', 'v111', 'v112', 'v113', 'v114', 'v115', 'v116', 'v117', 'v118', 'v119', 'v120', 'v121', 'v122', 'v123', 'v124', 'v125', 'v126', 'v127'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_vector_components', table_name='faces')
    op.drop_table('faces')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
