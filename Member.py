class MemberModel:
    id = 0
    name = ""
    selected = False

    def __init__(self, id, name, selected=False):
        self.id = id
        self.name = name
        self.selected = selected

    # def __init__(self, name, selected=False):
    #     self.id = id
    #     self.name = name
    #     self.selected = selected
