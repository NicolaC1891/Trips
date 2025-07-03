import hashlib
from datetime import date

from sqlalchemy import select
from database.models import CatPhrase
import random


async def get_today_wisdom(session) -> str:

    # getting all ids from CatPhrase table, get random
    ids = await session.execute(select(CatPhrase.id))
    ids_all = [row[0] for row in ids.all()]
    if not ids_all:
        return "Кот сегодня молчит..."

    ordinal = date.today().toordinal()
    seed = int(hashlib.sha256(str(ordinal).encode()).hexdigest(), 16)
    index = seed % len(ids_all)
    random_id = ids_all[index]
    wisdom_query = select(CatPhrase).where(CatPhrase.id == random_id)
    wisdom_res = await session.execute(wisdom_query)
    wisdom = wisdom_res.scalar_one_or_none()
    return wisdom.phrase if wisdom else "Кот потерял мысль..."