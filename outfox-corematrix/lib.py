class User:
    def __init__(self, username, id, tags):
        self.username = username
        self.id = id
        self.tags = tags

class Group:
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags

class GroupData:
    def __init__(self, groupA, groupB, groupC):
        self.groupA = groupA
        self.groupB = groupB
        self.groupC = groupC