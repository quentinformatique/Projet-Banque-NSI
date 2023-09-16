import jwt
import datetime as dt
from DataManager import File
from random import choice


def do_request(data, ip):
    """


    :param data: Any
    :param ip: str
    :return:
    """
    request = data.getvalue('request')
    if request == 'ConnectionId':
        return connection_id(data, ip)
    elif request == 'Creation':
        return create_account(data.getvalue('name'), data.getvalue('surname'), data.getvalue('civility'),
                              data.getvalue('email'), data.getvalue('user'), data.getvalue('password'), ip)
    else:
        token, user_id = decode_token(data)
        if token is None:
            return [False, 'Authentification invalide']
        elif request == 'TransactionLogs':
            return transaction_logs(user_id)
        elif request == 'ConnectionToken':
            return connection_token(token, user_id, ip)
        elif request == 'CreditDepot':
            return depot_credit(data, ip, user_id)
        elif request == 'Transaction':
            return transaction(data, ip, user_id)
        else:
            return [False, 'Invalid request']


def decode_token(data):
    try:
        token = data.getvalue('token')
        token_infos = jwt.decode(token, 'secret', algorithms=["HS256"])
        user = token_infos.get('id')
        return token, user
    except None:
        print('Token Error')
        return None, None


def get_token(user_id, date):
    token = jwt.encode({'id': user_id}, 'secret', algorithm="HS256")
    token_file = File('Token.csv', path='./Data/Account/')
    if token_file.get_data(column='token').count(token) != 0:
        token_file.set_data(str(add_time(date, 7)), 'expiration', token, column_id='token')
    else:
        token_file.add_line(line=[token, str(add_time(date, 7))])
    return token


def get_days_in_month(month, year):
    if month == 2:
        if year % 4 == 0:
            return 29
        return 28
    elif [1, 3, 5, 7, 8, 10, 12].count(month) == 1:
        return 31
    return 30


def add_time(time, time_add):
    month = time.month
    year = time.year
    while True:
        try:
            time = time.replace(day=time.day + time_add)
        except ValueError:
            time_add = time_add - get_days_in_month(month, year)
            month = month + 1
            if month == 13:
                year = year + 1
                month = 1
            time = time.replace(month=month, year=year)
        else:
            break
    return time


def get_connection_info(user, ip, request_type, date):
    identifier_file = File('ConnectionIdentifier.csv', path='./Data/Account/')
    infos = [True] + File('BankAccounts.csv', path='./Data/Account/').get_data(line=user)[1:] + identifier_file.get_data(
        line=user)[1:3] + identifier_file.get_data(line=user)[4:-1]
    identifier_file.set_data(date, 'lastLogin', user)
    identifier_file.set_data(ip, 'lastIpLogin', user)

    File('ConnectionLogs.csv', path='./Data/Logs/Global/').add_line([user, request_type, ip, date])
    File(user + '.csv', path='./Data/Logs/Users/').add_line([ip, request_type, date, '', ''])
    return infos


def transaction_logs(user_id):
    file = open('./Data/Logs/Users/' + user_id + '.csv', 'r')
    content = [line.replace('\n', '').split(',') for line in file.readlines()]
    file.close()
    labels = ['Credit', 'Depot', 'Transaction', 'Receive']
    final = []
    for line in content:
        if line[1] in labels:
            final.append(line[1:])
    return content


def connection_token(token, user, ip):
    token_file = File('Token.csv', path='./Data/Account/')
    if token not in token_file.get_data(column='token'):
        return [False]

    expiration_date = dt.datetime.fromisoformat(token_file.get_data(line=token, column='expiration', column_id='token'))
    now = dt.datetime.now()
    if expiration_date < now:
        return [False]
    token_file.set_data(add_time(now, 7), 'expiration', token, column_id='token')
    return get_connection_info(user, ip, 'ConnectionToken', now)


def connection_id(data, ip):
    user = data.getvalue('user')
    mdp = data.getvalue('password')
    identifier_file = File('ConnectionIdentifier.csv', path='./Data/Account/')
    if user in identifier_file.get_data(column='identifier'):
        if identifier_file.get_data(column='password', line=user, column_id='identifier') == mdp:
            user_id = identifier_file.get_data(column='id', line=user, column_id='identifier')
            date = dt.datetime.now()
            return get_connection_info(user_id, ip, 'ConnectionId', date) + [
                get_token(user_id, add_time(date, 7))]
    return [False]


def generate_alpha_id():
    user_id = ''
    alphabet = [chr(i) for i in range(48, 123) if i <= 57 or (65 <= i <= 90) or (i >= 97)]
    for i in range(2):
        if user_id != '':
            user_id += '-'
        for j in range(8):
            user_id += choice(alphabet)
    return user_id


def generate_num_id(n):
    user_id = ''
    number = [chr(i) for i in range(48, 57)]
    for j in range(n):
        user_id += choice(number)
    return user_id


def create_account(name, surname, civility, email, user, mdp, ip):
    identifier_file = File('ConnectionIdentifier.csv', path='./Data/Account/')
    bank_accounts_file = File('BankAccounts.csv', path='./Data/Account/')

    if email in identifier_file.get_data(column='email'):
        return [False, 'Email Already Exist']
    elif user in identifier_file.get_data(column='identifier'):
        return [False, 'Identifier Already Exist']

    date = dt.datetime.now()
    user_id = generate_alpha_id()
    cb = generate_num_id(16)
    cvv = generate_num_id(3)

    m = str(date.month)

    if len(m) == 1:
        m = '0' + m

    expiration = m + '/' + str(date.year + 4)[-2:]

    bank_accounts_file.add_line(line=[user_id, cb, cvv, civility, name, surname, expiration, date, 0])
    identifier_file.add_line(line=[user_id, email, user, mdp, date, ip])

    File(user_id + '.csv', path='./Data/Logs/Users/').add_line(
        lines=[['ip', 'type', 'date', 'amount', 'idDirection'], [ip, 'Creation', str(date)]])
    File('ConnectionLogs.csv', path='./Data/Logs/Global/').add_line(line=[user_id, 'Creation', ip, str(date)])

    return [True, cb, cvv, expiration, str(date), get_token(user_id, date)]


def depot_credit(data, ip, user_id):
    amount = data.getvalue('amount')
    date = dt.datetime.now()

    try:
        amount = float(amount)
    except None:
        return [False, 'Value Error, not int or float']

    bank_accounts_file = File('BankAccounts.csv', path='./Data/Account/')
    user_file = File(user_id + '.csv', path='./Data/Logs/Users/')
    sold = float(bank_accounts_file.get_data(column='solde', line=user_id))

    if amount < 0:
        request_type = 'Credit'
        if sold < amount * -1:
            return [False, 'Value Error, not enough money on account']
        user_file.add_line(line=[ip, request_type, str(date), amount, user_id])
    elif amount > 0:
        request_type = 'Depot'
        user_file.add_line(line=[ip, request_type, str(date), '+' + str(amount), user_id])
    else:
        return [False, 'Value Error, amount = 0']
    bank_accounts_file.set_data(str(amount + sold), 'solde', user_id)
    File('TransactionLogs.csv', path='./Data/Logs/Global/').add_line(
        line=[user_id, ip, request_type, date, amount, user_id])
    return [True, sold + amount]


def transaction(data, ip, user_id):
    amount = data.getvalue('amount')
    try:
        amount = float(amount)
    except None:
        return [False, 'Value Error, not int or float']
    if amount <= 0:
        return [False, 'Value Error, negative amount']

    account_path = './Data/Account/'
    user_logs_path = './Data/Logs/Users/'

    mail_dir = data.getvalue('direction')
    id_dir = File('ConnectionIdentifier.csv', path=account_path).get_data(column='id', line=mail_dir, column_id='email')
    date = dt.datetime.now()
    request_type = 'Transaction'

    bankFile = File('BankAccounts.csv', path=account_path)
    userFile = File(user_id + '.csv', path=user_logs_path)
    sold = float(bankFile.get_data(column='solde', line=user_id))
    if sold < amount:
        return [False, 'Value Error, not enough money on account']
    userFile.add_line(line=[ip, request_type, str(date), '-' + str(amount), id_dir])
    dir_sold = float(bankFile.get_data(column='solde', line=id_dir))

    dirUserFile = File(id_dir + '.csv', path=user_logs_path)
    dirUserFile.add_line(line=['None', 'Recive', str(date), '+' + str(amount), user_id])

    bankFile.set_data(str(sold - amount), 'solde', user_id)
    bankFile.set_data(str(dir_sold + amount), 'solde', id_dir)
    File('TransactionLogs.csv', path='./Data/Logs/Global/').add_line(
        line=[user_id, ip, request_type, date, str(amount), id_dir])
    return [True, str(sold - amount)]
