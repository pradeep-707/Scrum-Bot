# Contains all helper functions, which is used to parse input and output
import enum


def ResponseModel(data, message="Success"):
    """    Standard template for a response returned by the server.

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


def ErrorResponseModel(error, code=500, message="Error"):
    """Standard template for a error returned by the server.

	Args:
		error (error): Helpful error message send to the user
		message (str): Any additional message you want to send to the user. Defaults to "Error"
		code (int, optional): Status Code of the error Message. Defaults to 500.

	Returns:
		[dict]: A dict containing {error, code, message}
	"""
    print("The error is  : ", error)
    return {"error": error, "code": code, "message": message}


def parseControllerResponse(data, statuscode, error, message):
    class Statuscode(enum.Enum):
        Success = 200
        BadRequest = 400  # wrong data
        Unauthorized = 401  # unauthenticated users
        Forbidden = 403  # authenticated, but not authorized to view the page
        NotFound = 404
        InternalServerError = 500
        DuplicateKey = 11000  # Mongo throws a 11000 error when there is a duplicate key

    resp = {
        "data": data,
        "statusCode": statuscode,
        "success": statuscode == 200,
        "statusMessage": (Statuscode(statuscode)).name,
        "error": (error),  # TODO: Add generic message in production
        "message": message
    }

    # set duplicate key error status code to 400
    if resp["statusCode"] == 11000:
        resp["statusCode"] = 400

    return resp
