import mysql.connector

current_folder_Id = -1
# cursor ,conn
tuple_sub_folders = ()


def connect():
    global conn, cursor
    conn = mysql.connector.connect(host="localhost", user="admin", password="admin", database='db_dirbot')
    cursor = conn.cursor()


def add_tbl_dirs(name, chat_Id, parent_Id, message_Id, IsFile):
    statement = """INSERT INTO tbl_dirs (name, chat_Id, parent_Id, message_Id, IsFile) 
                    values (%s, %s, %s, %s, %s)"""
    vars = (name, chat_Id, parent_Id, message_Id, IsFile)
    cursor.execute(statement, vars)
    conn.commit()
    return cursor.lastrowid


def delete_tbl_dirs(Id):
    statement = """DELETE FROM tbl_dirs WHERE Id = %s"""
    vars = (Id, )
    cursor.execute(statement, vars)
    conn.commit()


def get_all_tbl_dirs():
    statement = """SELECT * FROM tbl_dirs """
    cursor.execute(statement)
    return cursor.fetchall()


def add_new_file(name, chat_id, message_id):
    check_for_no_folder(chat_id)
    add_tbl_dirs(name, chat_id, current_folder_Id, message_id, True)


def find_by_id(id):
    statement = """SELECT * from tbl_dirs where Id = {s_id}""".format(s_id=id)
    cursor.execute(statement)
    return cursor.fetchone()


def add_new_folder(name, chat_id):
    check_for_no_folder(chat_id)
    add_tbl_dirs(name, chat_id, current_folder_Id, -1, False)
    open_folder(current_folder_Id)  # refreshing list


def add_new_file(name, chat_id, message_id):
    check_for_no_folder(chat_id)
    add_tbl_dirs(name, chat_id, current_folder_Id, message_id, True)
    open_folder(current_folder_Id)  # refreshing list



def list_of_sub_folders(parent_id):
    statement = """SELECT Id, name FROM tbl_dirs where parent_Id = %s"""
    cursor.execute(statement, (parent_id, ))
    return cursor.fetchall()


def check_for_no_folder(chat_id):
    statement = """SELECT count(*) FROM tbl_dirs where chat_Id = %s"""
    cursor.execute(statement, (chat_id, ))
    (count,) = cursor.fetchone()
    if count == 0:
        global current_folder_Id
        current_folder_Id = add_tbl_dirs('root', chat_id, None, None, False)


def open_folder(folder_id):
    statement = """SELECT Id, name FROM tbl_dirs where parent_Id = {f_id}""".format(f_id=folder_id)
    cursor.execute(statement)
    global current_folder_Id
    current_folder_Id = folder_id
    res = cursor.fetchall()
    global tuple_sub_folders
    tuple_sub_folders = res
    return res


def back_folder():
    statement = """SELECT * FROM tbl_dirs where  Id = {current_folder}""".format(current_folder=current_folder_Id)
    cursor.execute(statement)
    par_id = cursor.fetchone()[3]  # parent column
    return open_folder(par_id)


def format_for_user(sub_folders):
    ind = 1
    str_filenames = ''
    for sub in sub_folders:
        str_filenames += "/{i}. ".format(i=ind) + str(sub[1]) + '\r\n'
        ind += 1
    return str_filenames


def press_sub_folder(message):
    num = message[1:]
    num = int(num)
    selected_id = tuple_sub_folders[num - 1][0]
    row = find_by_id(selected_id)
    isfile = row[5]
    if isfile:
        return False
    else:
        open_folder(selected_id)
        return True

def main():
    global currnet_chat_id, current_folder_Id
    currnet_chat_id = 911002
    connect()
    current_folder_Id = 6
    #add_new_folder('myDoc2', '911002')
    a = list_of_sub_folders(current_folder_Id)
    # print(a)
    # print(a[1][0])
    b = open_folder(a[1][0])
    # print(tuple_sub_folders)
    # print(b)
    # c = back_folder()
    # print(tuple_sub_folders)
    # print(c)
    #add_new_folder('pc3', currnet_chat_id)
    #print(list_of_sub_folders(a[1][0]))
    print(format_for_user(tuple_sub_folders))
    print(press_sub_folder("/2"))
    # print(tuple_sub_folders)
    # add_new_folder('mma4', currnet_chat_id)
    print(format_for_user(tuple_sub_folders))
    back_folder()
    print(format_for_user(tuple_sub_folders))
    add_new_file('grow.pdf', currnet_chat_id, '124')
    print(format_for_user(tuple_sub_folders))




if __name__ == "__main__":
    main()
