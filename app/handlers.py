from aiohttp import web

from app.utils import check_password, hash_password, generate_jwt, generate_new_password


async def register(request):
	data = await request.json()
	connection = request['connection']

	username = data['username']
	password = hash_password(data['password'])

	query = "INSERT INTO users (username, password) VALUES ($1, $2)"
	await connection.execute(query, username, password)

	return web.json_response(
		{
			"message": "User registered successfully"
		},
		status=201
	)


async def login(request):
	connection = request['connection']
	data = await request.json()

	username = data['username']
	password = data['password']

	user_data = await connection.fetchrow(
		"SELECT * FROM users WHERE username = $1", username
	)

	if (
			not user_data or
			not check_password(password, user_data['password'])
	):
		raise web.HTTPUnauthorized(text="Invalid credentials")
	token = generate_jwt({"user_id": user_data["id"]})

	response = web.json_response({"message": "Login successful"})
	response.set_cookie("token", token)
	return response


async def generate_password(request):
	connection = request['connection']
	user_id = request['user_id']
	data = await request.json()

	password_length = data.get('length')
	label = data.get('label')

	password_exists = await connection.fetchrow(
		"SELECT * FROM passwords WHERE user_id = $1 AND label = $2", user_id, label
	)
	if password_exists:
		raise web.HTTPBadRequest(text="Password with such label already exists")

	if not isinstance(password_length, int):
		raise web.HTTPBadRequest(text="Invalid length")
	if not label:
		raise web.HTTPBadRequest(text="Missing label for password")

	new_password = generate_new_password(length=password_length)
	query = "INSERT INTO passwords (password, label, user_id) VALUES ($1, $2, $3)"

	await connection.execute(
		query, new_password, label, user_id
	)

	return web.json_response(
		{
			"message": "Password generated successfully",
		},
		status=201
	)


async def get_passwords(request):
	connection = request['connection']
	user_id = request['user_id']

	passwords = await connection.fetch(
		"SELECT label, id FROM passwords WHERE user_id = $1", user_id
	)

	return web.json_response(
		{
			"passwords": [dict(password) for password in passwords]
		}
	)


async def delete_password(request):
	connection = request['connection']
	user_id = request['user_id']
	password_id = int(request.match_info['password_id'])

	print(user_id, password_id)
	await connection.execute(
		"DELETE FROM passwords WHERE user_id = $1 AND id = $2", user_id, password_id
	)

	return web.json_response(
		{
			"message": "Password deleted successfully"
		}
	)
