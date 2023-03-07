from Member import MemberModel
from db_config import conn


def addMemberDB(user, member):
    cursor = conn.cursor()
    query = """
    insert
    into members (user_id, name)
    select {}, %s 
    where not exists (select * from members where name = %s and user_id = {})
    """.format(user.chat_id, user.chat_id)

    cursor.execute(query, (member, member,))
    conn.commit()
    cursor.close()
    return


def removeAndGetAll(user) -> []:
    cursor = conn.cursor()
    query = "update members set selected= false where user_id = {} returning *".format(user.chat_id)
    res = []
    cursor.execute(query)
    rs = cursor.fetchall()
    conn.commit()
    cursor.close()
    for rw in rs:
        member = MemberModel(id=rw["id"], name=rw["name"], selected=rw["selected"])
        res.append(member)
    return res


def getMembers(user, refresh=False) -> []:
    cursor = conn.cursor()
    query = ""
    if refresh:
        query = "with updated as (update members set selected = false where user_id = {} returning *) select * from " \
                "updated order by id".format(user.chat_id)
    else:
        query = "select * from members where user_id = {} order by id ".format(user.chat_id)
    res = []
    cursor.execute(query)
    rs = cursor.fetchall()
    conn.commit()
    cursor.close()
    for rw in rs:
        member = MemberModel(id=rw["id"], name=rw["name"], selected=rw["selected"])
        res.append(member)
    return res


def toggleMember(member_id):
    cursor = conn.cursor()
    query = "update members set selected = not selected where id = {}".format(member_id)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return


def removeMember(member_id):
    query = "delete from members where id = {}".format(member_id)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()


def getRandom(user_id):
    query = "select * from members where user_id = {} and selected order by random()".format(user_id)
    cursor = conn.cursor()
    cursor.execute(query)
    rw = cursor.fetchone()
    cursor.close()
    conn.commit()

    return MemberModel(id=rw["id"], name=rw["name"]) if rw is not None else None
