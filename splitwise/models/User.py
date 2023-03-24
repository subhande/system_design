class User:
    def __init__(self, _id: str, firstName: str, lastName: str, bio: str, imageUrl: str):
        self._id = _id
        self.firstName = firstName
        self.lastName = lastName
        self.bio = bio
        self.imageUrl = imageUrl