import os
import sqlite3
import shutil

# for start open terminal and print
# win: py -3 App.py
# macOs: python3 App.py

from os import walk

n = '======================\n'
real_path = os.path.dirname(os.path.realpath(__file__))
separator = "\\"
input_path = real_path + separator + 'input'
output_path = real_path + separator + 'output'


def main(autosearch: bool) -> None:
    make_dirs()

    files_list = []
    for (dir_path, dir_name, file_name) in walk(input_path):
        files_list.extend(file_name)
        break

    if files_list:
        for file in files_list:
            # Split a path in root and extension.
            file_extension = os.path.splitext(file)[1]
            if file_extension == '.db':
                if autosearch:
                    android_flow(file, True)
                else:
                    android_flow(file, False)
            elif file_extension == '.sqlite':
                if autosearch:
                    pass
                else:
                    ios_flow(file)
            else:
                pass
    else:
        print('', n, "Current directory with files is empty or not exist. Please, check the 'input' directory.")


def make_dirs() -> None:

    # check path separator: macOS it's '/', and win it's '\\'
    if '\\' not in real_path and '/' in real_path:
        global separator, input_path, output_path
        separator = '/'
        input_path = real_path + separator + 'input'
        output_path = real_path + separator + 'output'

    # be sure it exist (input_path)
    if not os.path.exists(input_path):
        os.makedirs(input_path)

    # be sure it exist (output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def clear_output_directory() -> None:
    make_dirs()

    # clear
    for the_file in os.listdir(output_path):
        file_path = os.path.join(output_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def copy_file(arg_file: str, arg_claim_id: str) -> None:
    current_file = input_path + separator + arg_file
    new_file = output_path + separator + arg_file
    if arg_claim_id:
        claim_path = output_path + separator + arg_claim_id
        if not os.path.exists(claim_path):
            os.makedirs(claim_path)
        new_file = claim_path + separator + arg_file
    try:
        shutil.copyfile(current_file, new_file)
    except Exception as e:
        print(e)


def android_flow(db: str, autosearch) -> None:
    db_path = input_path + separator + db
    # print(db_path)
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    # print(cursor.fetchall())

    if autosearch:
        sql = "SELECT claim_id, file_path FROM upload_files"
        cursor.execute(sql)
        tuple_items = cursor.fetchall()
        if tuple_items:
            for array in tuple_items:
                # print(array[0], array[1])
                array_claim_id = str(array[0])
                array_file_path = array[1].split('/')[-1]
                copy_file(array_file_path, array_claim_id)
        cursor.close()
    else:
        sql = "SELECT file_path FROM upload_files WHERE claim_id = ?"
        cursor.execute(sql, (claim_id,))
        tuple_files = cursor.fetchall()

        if tuple_files:
            result = [item for array in tuple_files for item in array]

            if result:
                print('', n, 'For claim_id', claim_id, 'we found', len(result), 'file(s)')
                clear_output_directory()
                for name in result:
                    flow_file = name.split('/')[-1]
                    print(flow_file)
                    copy_file(flow_file)
        else:
            print('', n, 'Files with claim_id', claim_id, 'not found')
        cursor.close()

    db_connection.close()


def get_ios_files_by_cursor(arg_cursor, arg_sql, arg):
    result = set()

    argument = (arg,)
    if isinstance(arg, list):
        argument = arg

    arg_cursor.execute(arg_sql, argument)
    tuple_files = arg_cursor.fetchall()
    if tuple_files:
        items = [item for array in tuple_files for item in array]
        if items:
            for item in items:
                if not item == 'None':
                    result.add(item)
    return result


def check_if_exist(filtered_list):
    return [item for item in filtered_list if os.path.exists(input_path + separator + item)]


def ios_flow(sql: str) -> None:
    """
    Поиск данных в иос:
    1. Например, мы ищем данные для таски 29607 - photo, video, attachments.
    2. Сначала открываем таблицу tickets и в поле id ищем 29607. В ответе смотрим поле local_id = 33
    3. Идём в attachments и выбираем все файлы по local_ticket_id с 33
    4. Затем идём в photos и выбираем все файлы по local_ticket_id с 33.
    5. Так как у контента может не быть local_ticket_id, но есть демонстрация, нужно сделать сверку по демонстрации.
    Идём в таблицу demonstrations в поле local_ticket_id ищем 33, получаем список демонстраций для этого тикета.
    В нашем случае это 1,2,3,4.
    6. Возвращаемся в таблицу photos и выгребаем все данные для local_demonstration_id по очереди 1,2,3,4.
    Смотрим, чтобы имена не совпадали с именами из пункта 4.
    7. Повторяем пункты 4,5,6 для таблицы videos.
    """
    all_files = set()

    db_path = input_path + separator + sql
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()
    sql = "SELECT local_id FROM tickets WHERE id = ?"
    cursor.execute(sql, (claim_id,))

    # In the start case we will open the Tickets table and will find id
    tuple_files = cursor.fetchall()
    if not tuple_files or not tuple_files[0] or not tuple_files[0][0]:
        print('', n, 'For claim_id', claim_id, 'we found', 0, 'file(s)')
        return
    local_ticket_id = tuple_files[0][0]
    print('We going to search files for claim_id =', claim_id, ', where local_ticket_id =', local_ticket_id)

    # get attachments where we are have local_ticket_id
    sql = "SELECT local_file_name FROM attachments WHERE local_ticket_id = ?"
    files = get_ios_files_by_cursor(cursor, sql, local_ticket_id)
    if files:
        for file in files:
            all_files.add(file)

    # get photos where we are have local_ticket_id
    sql = "SELECT local_file_name FROM photos WHERE local_ticket_id = ?"
    files = get_ios_files_by_cursor(cursor, sql, local_ticket_id)
    if files:
        for file in files:
            all_files.add(file)

    # get videos where we are have local_ticket_id
    sql = "SELECT local_file_name FROM videos WHERE local_ticket_id = ?"
    files = get_ios_files_by_cursor(cursor, sql, local_ticket_id)
    if files:
        for file in files:
            all_files.add(file)

    # check demonstrations for photos and videos
    sql = "SELECT local_id FROM demonstrations WHERE local_ticket_id = ?"
    cursor.execute(sql, (local_ticket_id,))
    tuple_files = cursor.fetchall()
    if tuple_files:
        items = [item for array in tuple_files for item in array]
        if items:
            placeholder = '?'
            placeholders = ', '.join(placeholder for _ in items)
            sql = "SELECT local_file_name FROM photos WHERE local_demonstration_id IN (%s)" % placeholders
            files = get_ios_files_by_cursor(cursor, sql, items)
            if files:
                for file in files:
                    all_files.add(file)
            sql = "SELECT local_file_name FROM videos WHERE local_demonstration_id IN (%s)" % placeholders
            files = get_ios_files_by_cursor(cursor, sql, items)
            if files:
                for file in files:
                    all_files.add(file)

    cursor.close()
    db_connection.close()

    # remove None
    filtered_list = list(filter(None, all_files))
    # copy files, if exist
    if filtered_list:
        clear_output_directory()

        exists = check_if_exist(filtered_list)
        if exists:
            print('', n, 'For claim_id', claim_id, 'we found', len(exists), 'file(s)')
            for name in exists:
                print(str(name))
                copy_file(str(name))
        else:
            print('', n, 'For claim_id', claim_id, 'we found 0 files that exist here')


# User input and start work here:
claim_id = input('Please, press ENTER for AUTOSEARCH or input claim_id (for example 34652).\n')

if not claim_id:
    claim_id = '0'
    main(True)
else:
    main(False)

input('\n ' + n + ' Press Enter to Exit...')
