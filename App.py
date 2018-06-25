import os
import sqlite3
import shutil

# for start open terminal and print
# py -3 App.py


from os import walk

n = '======================\n'
real_path = os.path.dirname(os.path.realpath(__file__))
input_path = real_path + '\input'
output_path = real_path + '\output'


def main() -> None:
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
                android_flow(file)
            elif file_extension == '.sql':
                pass
            else:
                pass
    else:
        print('', n, "Current directory with files is empty or not exist. Please, check the 'input' directory.")


def make_dirs() -> None:
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


def copy_file(file: str) -> None:
    current_file = input_path + '\\' + file
    new_file = output_path + '\\' + file
    try:
        shutil.copyfile(current_file, new_file)
    except Exception as e:
        print(e)


def android_flow(db: str) -> None:
    db_path = input_path + "\\" + db
    # print(db_path)
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()
    sql = "SELECT file_path FROM upload_files WHERE claim_id = ?"
    cursor.execute(sql, (claim_id,))
    # print(cursor.fetchall())
    tuple_files = cursor.fetchall()

    if tuple_files:

        list_names = []
        for t in tuple_files:
            for v in t:
                list_names.append(v)

        if list_names:
            print('', n, 'For claim_id', claim_id, 'we found', len(list_names), 'file(s)')
            clear_output_directory()
            for name in list_names:
                flow_file = name.split('/')[-1]
                print(flow_file)
                copy_file(flow_file)
    else:
        print('', n, 'Files with claim_id', claim_id, 'not found')

    cursor.close()
    db_connection.close()


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
    db_path = input_path + "\\" + sql
    # print(db_path)
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()
    sql = "SELECT file_path FROM upload_files WHERE claim_id = ?"
    cursor.execute(sql, (claim_id,))


# User input and start work here:
claim_id = input('Please, input claim_id. For example "70820" of "69051" and press enter \n')
if not claim_id:
    print('', n, 'You need to print a right claim_id. Default value is 0\n', n)
    claim_id = '0'
else:
    main()

input('\n ' + n + ' Press Enter to Exit...')
