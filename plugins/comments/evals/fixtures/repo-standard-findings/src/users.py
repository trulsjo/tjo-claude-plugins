def get_user(user_id):
    """Gets the user.

    :param user_id: the user id
    :returns: the user
    """
    # look up the id in the dict and return the entry
    return _USERS[user_id]


def _normalise_email(email):
    """Normalises the email.

    :param email: the email
    :returns: the normalised email
    """
    # print("normalising", email)
    return email.strip().lower()


_USERS = {}
