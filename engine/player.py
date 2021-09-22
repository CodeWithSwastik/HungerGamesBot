class Tribute:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    @classmethod
    def from_member(cls, member):
        return cls(member.name, member.id)