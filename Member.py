class MemberModel:
    id = 0
    name = ""
    selected = False

    def __init__(self,  name, selected=0):
        self.id = id
        self.name = name
        self.selected = selected

    # def __init__(self, name, selected=False):
    #     self.id = id
    #     self.name = name
    #     self.selected = selected

    def __str__(self):
        return "(name: {} , selected:{} )".format(self.name.strip(), self.selected)
