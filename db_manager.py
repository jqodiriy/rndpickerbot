from db_config import conn
from user_model import UserModel


def get_user(chat_id):
    cursor = conn.cursor()
    query = "select * from users where chat_id = " + str(chat_id)
    cursor.execute(query)
    conn.commit()
    rs = cursor.fetchall()
    rw = rs[0] if len(rs) > 0 else None
    user = UserModel(
        id=rw["id"],
        chat_id=rw["chat_id"],
        username=rw["username"],
        status=rw["status"]
    ) if rw is not None else None

    return user


def addUser(user):
    cursor = conn.cursor()
    query = "insert into users (chat_id, username) values ({}, %s) returning id".format(user.chat_id)
    cursor.execute(query, (user.username,))

    conn.commit()
    cursor.close()
    return


def updateStatus(user):
    cursor = conn.cursor()
    query = "update users set status = {} where id = {}".format(user.status, user.id)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return
