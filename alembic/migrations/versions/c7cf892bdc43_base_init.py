from typing import Sequence, Union, List, Dict, Any
from json import dumps as json_dumps

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, Connection

from src.core.common.encryptor import EncryptorProcessor

revision: str = 'c7cf892bdc43'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('auth_keys',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('hash_key', sa.LargeBinary(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=30), nullable=False),
                    sa.Column('is_active', sa.SmallInteger(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False,
                              comment='Дата создания ключа в UTC'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('organizations',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('activities',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('activity', sa.JSON(), nullable=False),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('organization_id')
                    )
    op.create_table('buildings',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('building', sa.VARCHAR(length=20), nullable=False),
                    sa.Column('address', sa.VARCHAR(length=150), nullable=False),
                    sa.Column('latitude', sa.DOUBLE_PRECISION(), nullable=False),
                    sa.Column('longitude', sa.DOUBLE_PRECISION(), nullable=False),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('organization_id')
                    )
    op.create_table('phones',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('number', sa.VARCHAR(length=25), nullable=False),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('number')
                    )

    conn: Connection = op.get_bind()

    organizations: List[Dict[str, Any]] = [
        {
            "id": 1,
            "name": "organization_1"
        },
        {
            "id": 2,
            "name": "organization_2"
        },
        {
            "id": 3,
            "name": "organization_3"
        }
    ]
    conn.execute(
        statement=text(
            """
                INSERT INTO organizations(id, name)
                VALUES(:id, :name)
            """
        ),
        parameters=organizations
    )

    phones: List[Dict[str, Any]] = [
        {
            "id": 1,
            "organization_id": 1,
            "number": "12345678"
        },
        {
            "id": 2,
            "organization_id": 1,
            "number": "13453463"
        },
        {
            "id": 3,
            "organization_id": 2,
            "number": "9892358263"
        },
        {
            "id": 4,
            "organization_id": 3,
            "number": "987654321"
        },
        {
            "id": 5,
            "organization_id": 3,
            "number": "98765434442"
        }
    ]
    conn.execute(
        statement=text(
            """
                INSERT INTO phones(id, organization_id, number)
                VALUES(:id, :organization_id, :number)
            """
        ),
        parameters=phones
    )

    buildings: List[Dict[str, Any]] = [
        {
            "id": 1,
            "organization_id": 1,
            "building": "блюхера 32/1",
            "address": "москва, 47 съезд, этаж 55",
            "latitude": 44.543634637,
            "longitude": 55.54554555
        },
        {
            "id": 2,
            "organization_id": 2,
            "building": "блюхера 32/1",
            "address": "москва, 47 съезд, этаж 45",
            "latitude": 44.543634637,
            "longitude": 55.54554555
        },
        {
            "id": 3,
            "organization_id": 3,
            "building": "сампсоновский 18",
            "address": "санкт-петербург, пр-т сампсоновский, лестница №4",
            "latitude": 51.543634637,
            "longitude": 11.54554555
        }
    ]
    conn.execute(
        statement=text(
            """
                INSERT INTO buildings(id, organization_id, building, address, latitude, longitude)
                VALUES (:id, :organization_id, :building, :address, :latitude, :longitude)
            """
        ),
        parameters=buildings
    )

    activities: List[Dict[str, Any]] = [
        {
            "id": 1,
            "organization_id": 1,
            "activity": json_dumps(obj={"еда": {}, "автомобили": {}, "хоз. оборудование": {}}, ensure_ascii=False),
        },
        {
            "id": 2,
            "organization_id": 2,
            "activity": json_dumps(
                obj={
                    "еда": {"мясо": {}, "хлебные изделия": {}},
                    "мед. Оборудование": {}
                },
                ensure_ascii=False)
        },
        {
            "id": 3,
            "organization_id": 3,
            "activity": json_dumps(
                obj={
                    "еда": {"мясо": {"свинина": {}, "курица": {}}},
                    "автомобили": {"седаны": {}, "кроссоверы": {}}
                },
                ensure_ascii=False)
        }
    ]
    conn.execute(
        statement=text(
            """
            INSERT INTO activities(id, organization_id, activity)
            VALUES (:id, :organization_id, :activity)
            """
        ),
        parameters=activities
    )

    auth_keys: List[Dict[str, Any]] = [
        {
            "id": 1,
            "hash_key": EncryptorProcessor.encrypt(data="TEST_KEY_1"),
            "name": "TEST_KEY_1",
            "is_active": 1
        },
        {
            "id": 2,
            "hash_key": EncryptorProcessor.encrypt(data="TEST_KEY_2"),
            "name": "TEST_KEY_2",
            "is_active": 1
        }
    ]
    conn.execute(
        statement=text(
            """
                INSERT INTO auth_keys(id, hash_key, name, is_active)
                VALUES (:id, :hash_key, :name, :is_active)
            """
        ),
        parameters=auth_keys
    )


def downgrade() -> None:
    op.drop_table('phones')
    op.drop_table('buildings')
    op.drop_table('activities')
    op.drop_table('organizations')
    op.drop_table('auth_keys')
