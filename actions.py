
async def create_account(users, id: str, first_name: str) -> bool:
	result = users.create(
    user_id = str(id),
    email = f"{id}@gmail.com",
    name = first_name # optional
	)

	return result
