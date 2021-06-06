# Contains all helper functions, which is used to parse input and output


def ResponseModel(data, message="Success"):
	"""Standard template for a response returned by the server.

	Args:
		data (any): any data which is to be returned by the server.
		message (str, optional): Any additional message you want to send to the user.Defaults to "Success".

	Returns:
		[dict]: a dict containting {data, code:200, message}
	"""
	return {
		"data": [data],
		"code": 200,
		"message": message,
	}


def ErrorResponseModel(error,  code=500, message="Error"):
	"""Standard template for a error returned by the server.

	Args:
		error (error): Helpful error message send to the user
		message (str): Any additional message you want to send to the user. Defaults to "Error"
		code (int, optional): Status Code of the error Message. Defaults to 500.

	Returns:
		[dict]: A dict containing {error, code, message}
	"""
	return {"error": error, "code": code, "message": message}