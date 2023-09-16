import requests
import datetime as dt
data = {
    'request' : 'TransactionLogs',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ikhrc2FnOEZqLVU5cTB0MUJmIiwidGVtcCI6IlRydWUifQ.cvz1Okg8Rlnv2r0dte8-Vxazf5yBH0B--dMYognmKwU'
}
data2 = {
    'request' : 'ConnectionToken',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6InNUWm5zMkI1LVBhcjBMNThLIn0.mKjR1ytj95aPUxxRflawaykRpc4PeXX7_pmDgixwsmw'
}
data3 = {
    'request' : 'ConnectionId',
    'user' : 'harrfdgsoldg',
    'password' : '123456789'
}
data4 = {
    'request' : 'Creation',
    'name' : 'Harold',
    'surname' : 'Gerard',
    'civility' : 'H',
    'email' : 'hargdgold@gmail.com',
    'user' : 'harrfdgsoldg',
    'password' : '123456789'
}
data5 = {
    'request' : 'CreditDepot',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ikhrc2FnOEZqLVU5cTB0MUJmIiwidGVtcCI6IlRydWUifQ.cvz1Okg8Rlnv2r0dte8-Vxazf5yBH0B--dMYognmKwU',
    'amount' : '300'
}
data6 = {
    'request' : 'CreditDepot',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ikhrc2FnOEZqLVU5cTB0MUJmIiwidGVtcCI6IlRydWUifQ.cvz1Okg8Rlnv2r0dte8-Vxazf5yBH0B--dMYognmKwU',
    'amount' : '-100'
}
data7 = {
    'request' : 'Transaction',
    'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ikhrc2FnOEZqLVU5cTB0MUJmIiwidGVtcCI6IlRydWUifQ.cvz1Okg8Rlnv2r0dte8-Vxazf5yBH0B--dMYognmKwU',
    'amount' : '100',
    'direction' : 'harold@gmail.com'
    
}

url = 'http://exebank.cf:2555'

try:
    r = requests.post(url, data=data3)
    print(r)
    print(r.text)
except requests.exceptions.ConnectionError:
    print("Site not rechable", url)