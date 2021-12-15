import sqlite3
import sys


def menu():
    print('Что необходимо сделать? \n')
    print('(1)  Отображение определенной таблицы БД')
    print('(2)  Составить и отобразить на экране перечень полных наименований вузов, имеющих выбранный статус и у которых в БД отсутствуют ФИО ректора и справочный телефон вуза')
    print('(3)  Рассчитать и представить в виде таблицы распределения процента преподавателей, имеющих ученые степени кандидата и доктора наук')
    print('(4)  Завершение программы')
    return input('Выберите действие : ')


def tn_choice(table_name_kart, table_name_stat):
    choice = input('Какую таблицу вывести? \n\n (1) <Картотека вузов> \n\n (2) <Статистика вузов> \n\n Выбор : ')
    if choice == '1':
        return table_name_kart
    elif choice == '2':
        return table_name_stat


def table_bd(db_name, table_name):
    """

    Отображение текущего содержимого БД на экране в виде таблицы

    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    sql = 'SELECT * FROM {}'.format(table_name)
    with con:
        data = cur.execute(sql).fetchall()

    print('\n \nТаблица: ', table_name, ' из БД', db_name, '\n')

    col_width = [0] * len(data[0])

    for x in data:
        for k, y in enumerate(x):
            if len(str(y).strip()) > col_width[k]:
                col_width[k] = len(str(y).strip())

    for x in col_width:
        if x < max(col_width):
            x = max(col_width)

    for line in data:
        for i, x in enumerate(line):
            sys.stdout.write('{0}{1}'.format(str(x).strip(), ((col_width[i] - len(str(x).strip())) * ' ' + '  ')))
        print('')

    cur.close()
    con.close()


def select_Status():
    print('Выберите статус вуза')
    print(' (1) Университет')
    print(' (2) Академия')
    print(' (3) Институт')
    choice = input('Выбор : ')

    if choice == '1':
        return 'Университет'
    elif choice == '2':
        return 'Академия'
    elif choice == '3':
        return 'Институт'
    else:
        print('\n\n Ошибка ввода')
        input('\n Завершение работы с программой \n\n Нажмите на любую клавишу, чтобы выйти')
        sys.exit()


def vuz_without_FIO_tel(bd_name, table_name_kart, selected_status):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    sql = 'SELECT TRIM(z1) FROM {0} WHERE TRIM(status) = "{1}" AND TRIM(z15) = "" AND TRIM(z9) = ""  '.format(
        table_name_kart, selected_status)
    cur.execute(sql)
    data = []
    while True:
        next_row = cur.fetchone()
        if next_row:
            data.append(next_row[0])
        else:
            break
    return data


def raspred_Proc_Prep(bd_name, table_name_kart, table_name_stat):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    sql = 'SELECT TRIM({0}.z1) , {1}.pps , {1}.dn + {1}.kn , ({1}.dn + {1}.kn) * 100/{1}.pps FROM {0},{1} WHERE {0}.codvuz = {1}.codvuz AND TRIM({0}.status) = "Университет"'.format(
        table_name_kart, table_name_stat)
    data = cur.execute(sql).fetchall()

    col_width = [0] * len(data[0])
    i = 0
    while i < 2:
        i += 1
        for x in data:
            for k, y in enumerate(x):
                if len(str(y).strip()) > col_width[k]:
                    col_width[k] = len(str(y).strip())

    col_width[1] = 25
    col_width[2] = 25

    sum_prep = 0
    sem_prep_step = 0
    for line in data:
        sum_prep += line[1]
        sem_prep_step += line[2]

    print(' N          ' + 'Университет' + (
                col_width[0] - len('Университет') - 10) * ' ' + 2 * ' ' + 'Кол-во преподавателей' + (
                      col_width[2] - len('Кол-во преподавателей')) * ' ' + 2 * ' ' + 'Степенные преподавателили' + (
                      col_width[3] - len('Степенные преподавателили')) * ' ' + 2 * ' ' + '% степенных' + (
                      col_width[3] - len('% степенных')) * ' ')
    for k, line in enumerate(data):
        sys.stdout.write(' {0}{1}   '.format(k, (len(str(len(data))) - len(str(k))) * ' '))
        for i, x in enumerate(line):
            sys.stdout.write('{0}{1}'.format(str(x).strip(), ((col_width[i] - len(str(x).strip())) * ' ' + '  ')))
        print('')
    print(
        '--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('       Сумма' + 125 * ' ' + str(sum_prep) + 22 * ' ' + str(sem_prep_step) + 22 * ' ' + str(
        int(sem_prep_step * 100 / sum_prep)))
