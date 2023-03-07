class UserModel(object):
    id = 0
    chat_id = 0
    username = ""
    status = 0

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username

    def __init__(self, chat_id, username, status):
        self.chat_id = chat_id
        self.username = username
        self.status = status

    def __init__(self, id, chat_id, username, status):
        self.id = id
        self.chat_id = chat_id
        self.username = username
        self.status = status

    def __str__(self):
        return "id = {},\nchat_id = {},\nusername = {},\nstatus = {}\n".format(self.id, self.chat_id,self.username,self.status)
