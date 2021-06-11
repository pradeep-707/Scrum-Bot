from mongoengine.errors import ValidationError, NotUniqueError
from models.members import User, verifyPassword
from app.helper import parseControllerResponse
from app.utils import generateJwt


# Add users to database
def register(user):
    try:
        print("Creating a new user")
        newUser = User(rollno=user["rollno"])
        newUser.name = user["name"]
        newUser.password = user["password"]
        newUser.batch = user["batch"]
        newUser.discordHandle = user["discordHandle"]
        newUser.password = user["password"]

        newUser.save(force_insert=False, validate=True)

        return parseControllerResponse("Success", 200, None,
                                       "Successfully created a user")
    except ValidationError as err:
        print("Something went wrong", err)
        return parseControllerResponse(400, err, "Data entered is incorrect")

    except NotUniqueError as err:
        # There is no way to create user friendly message
        # So converting it into a string and checking if the rollno is there in the sub string
        if "rollno" in err.__str__():
            return parseControllerResponse(
                "Failure", 11000,
                'A user already exists with the rollno "{}"'.format(
                    user["rollno"]),
                "A document with the given data already exists")
        return parseControllerResponse(
            "Failure", 11000,
            'A user already exists with the Discord Handle "{}"'.format(
                user["discordHandle"]),
            "A document with the given data already exists")

    except Exception as e:
        print("Couldn't create document for ", user["rollno"], ". Due to ", e)
        return parseControllerResponse(
            "Failure", 500, e, "Something went wrong, try again later.")


def login(rollnumber, password):
    try:
        error_message = "The rollno password combination is incorrect"
        user = User.objects(rollno=rollnumber)
        # user not found
        if len(user) == 0:
            return parseControllerResponse("Failure", 400, error_message,
                                           error_message)
        doesPasswordMatch = verifyPassword(user[0]["password"], password)
        if (doesPasswordMatch):
            # Create session and return a 200

            token = generateJwt({
                "id": str(user[0]["id"]),
                "rollno": user[0]["rollno"]
            })
            return parseControllerResponse({token: "token"}, 200, None,
                                           "User successfully authenticated")

        else:
            return parseControllerResponse("Failure", 400, error_message,
                                           error_message)

    except Exception as err:
        print("Couldn't authenticate  ", rollnumber, ". Due to ", err)
        return parseControllerResponse(
            "Failure", 500, err, "Something went wrong, try again later.")
