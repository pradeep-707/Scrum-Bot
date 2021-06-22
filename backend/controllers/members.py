from models.members import Member
from schema.members import MemberInDBSchema, memberHelper

def getMemberFromDiscordHandle(discordHandle : str):
    """Finds and returns the user with the given discord handle, if 
        such a user doesn't exist, return None"""
    try:
        member_ = Member.objects(discordHandle=discordHandle).first()
        assert member_
        member = MemberInDBSchema(**memberHelper(member_))
        return member
    except AssertionError as _:
        # if the member is not found, raise a ValueError
        return None
    except Exception as e:
        raise Exception("Couldn't find a user with the discord handle \
            {}, due to {}".format(discordHandle, e))