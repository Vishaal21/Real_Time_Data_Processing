async def save_data(db, data):
    db.add(data)
    await db.commit()
    await db.refresh(data)
