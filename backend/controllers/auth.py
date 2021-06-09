from mongoengine.errors import ValidationError, NotUniqueError
from ..models.members import User
from ..app.helper import parseControllerResponse


# Add users to database
def register(user):
    try:
        newUser = User(rollno=user["rollno"])
        newUser.name = user["name"]
        newUser.password = user["password"]
        newUser.batch = user["batch"]
        newUser.discordHandle = user["discordHandle"]
        newUser.password = user["password"]

        newUser.save(force_insert=False, validate=True)

        return parseControllerResponse(200, None,
                                       "Successfully created a user")
    except ValidationError as err:
        print("Something went wrong", err)
        return parseControllerResponse(400, err, "Data entered is incorrect")
    except NotUniqueError as err:
        print(11000, err, "A document with the given data already exists")
    except Exception as e:
        print("Couldn't create document for ", user["rollno"], ". Due to ", e)
        return (500, e, "Something went wrong, try again later.")
