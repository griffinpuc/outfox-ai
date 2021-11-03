class User:
    def __init__(self, username, id, tags):
        self.username = username
        self.id = id
        self.tags = tags

class Group:
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags

class Resource:
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags