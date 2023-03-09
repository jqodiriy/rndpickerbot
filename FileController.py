from Member import MemberModel


def getStatus():
    read_file = open("status.txt", 'r')
    lines = read_file.readlines()

    try:
        return int(lines[0])
    except:
        setStatus(0)
        return 0


def setStatus(status):
    f = open("status.txt", "r")
    contents = f.readlines()
    contents.clear()
    f = open("status.txt", "w")
    contents = str(status)
    f.write(contents)
    f.close()
    return


def addMember(name):
    f = open("members.txt", "r+")
    contents = f.readlines()
    for line in contents:
        try:
            [member, selected] = line.split(' & ')
            if member == name.strip():
                return
        except:
            continue
    f.write("{} & 0\n".format(name))


def removeMember(name):
    with open(r"members.txt", 'r+') as f:
        contents = f.readlines()
        f.seek(0)
        f.truncate()

        for number, line in enumerate(contents):
            try:
                [member, selected] = line.split(' & ')
                if member.strip() != name.strip():
                    f.write(line)
            except:
                continue
        f.close()


def getMembers():
    f = open("members.txt", 'r')
    contents = f.readlines()
    members = []
    for line in contents:
        try:
            [member, selected] = line.split(' & ')
            members.append(
                MemberModel(member, int(selected.strip()))
            )
        except:
            continue
    return members


def refreshSelects():
    members = []
    with open(r"members.txt", 'r+') as f:
        contents = f.readlines()
        f.seek(0)
        f.truncate()

        for number, line in enumerate(contents):
            try:
                [member, selected] = line.split(' & ')
                f.write(member + " & 0\n")
                members.append(
                    MemberModel(
                        member, selected
                    )
                )
            except:
                continue
        f.close()

    return members


def updateMember(name):
    with open(r"members.txt", 'r+') as f:
        contents = f.readlines()
        f.seek(0)
        f.truncate()

        for number, line in enumerate(contents):
            try:
                [member, selected] = line.split(' & ')
                if member != name:
                    f.write(member + " & {}\n".format(selected.strip()))
                else:
                    f.write(member + " & {}\n".format(1 - int(selected.strip())))
            except:
                continue
        f.close()
# addMember("AF")
# addMember("F")
# addMember("rr")
updateMember("AF")
updateMember("F")
refreshSelects()


x = getMembers()
for m in x:
    print(m)

