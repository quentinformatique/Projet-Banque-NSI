from tkinter import *
import requests


def convert_request(data):
    return data[1:-1].replace(" '", '').replace("'", '').split(",")


class BankApp:
    def __init__(self):
        self.url = 'http://exebank.cf:2555'
        self.window = Tk()
        self.background = PhotoImage(file="background.png")
        self.ico = "logo_ico.ico"

    def do_request(self, data):
        try:
            r = requests.post(self.url, data=data)
            print(r)
            return convert_request(r.text)
        except requests.exceptions.ConnectionError:
            print("Site not rechable", self.url)
            return [False]

    def create_cache_account(self, data, add_data=[]):
        infos = self.do_request(data) + add_data
        if infos[0] == 'True':
            self.cb = infos[1]
            self.crypto = infos[2]
            self.civility = infos[3]
            self.name = infos[4]
            self.surname = infos[5]
            self.expiration = infos[6]
            self.last_connection_date = infos[7]
            self.sold = infos[8]
            self.mail = infos[9]
            self.user = infos[10]
            self.connection_date = infos[11]
            self.token = infos[12]
            file = open('token.txt', 'w')
            file.write(self.token)
            file.close()
            print('Connection réussi')
            return True
        else:
            return False

    def connection_token(self):
        try:
            token = open('token.txt', 'r').read()
        except FileNotFoundError:
            print('error')
            file = open('token.txt', 'w')
            file.close()
            token = open('token.txt', 'r').read()
        if token != '':
            data = {
                'request': 'ConnectionToken',
                'token': token
            }
            if self.create_cache_account(data, add_data=[token]):
                self.main_window()
            else:
                self.login_window()
        else:
            self.login_window()

    def login_window(self):

        self.window.title("Fenètre de connexion")
        self.window.geometry("1080x720")
        self.window.iconbitmap(self.ico)

        canvas = Canvas(self.window, width=1080, height=720)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.background, anchor="nw")

        self.login_user_entry = Entry(self.window, font=("ebrima", 24), width=20, fg="#000000", bd=0)
        self.login_password_entry = Entry(self.window, font=("ebrima", 24), width=20, fg="#000000", bd=0)

        self.login_password_entry.config(show="*")

        login_button = Button(self.window, text="Se connecter", font=("ebrima 18 underline"), bg="#ffffff",
                              fg="#000000", bd=2, relief='groove', command=self.login_id_request)

        canvas.create_window(540, 570, window=login_button)

        create_button = Button(self.window, text="Se créer un compte", font=("ebrima 18 underline"), bg="#ffffff",
                               fg="#000000", bd=2, relief='groove', command=self.create_window)

        canvas.create_window(540, 640, window=create_button)

        canvas.create_text(450, 235, text="Identifiant :", font=("ebrima 23 underline"), fill="white")
        canvas.create_text(470, 390, text="Mot de passe :", font=("ebrima 23 underline"), fill="white")
        canvas.create_text(540, 25, text="Bienvenue, veuillez choisir un mode de connexion",
                           font=("ebrima 30 underline"), fill="white")

        un_window = canvas.create_window(540, 270, anchor="n", window=self.login_user_entry)
        pw_window = canvas.create_window(540, 470, anchor="s", window=self.login_password_entry)

        self.window.mainloop()

    def login_id_request(self):

        user = self.login_user_entry.get()
        password = self.login_password_entry.get()

        data = {
            'request': 'ConnectionId',
            'user': user,
            'password': password
        }

        if self.create_cache_account(data):
            self.window.destroy()
            self.main_window()

    def create_window(self):
        self.homme = IntVar()
        self.femme = IntVar()

        self.window_front = Toplevel()
        self.window_front.grab_set()
        self.window_front.focus_set()
        self.window_front.title("Se créer un compte")
        self.window_front.geometry("400x600")
        self.window_front.iconbitmap(self.ico)
        self.window_front.config(background='#474643')

        canvas = Canvas(self.window_front, width=400, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=PhotoImage(file="background.png"), anchor='nw')

        canvas.create_text(55, 30, text="Nom :", font=("ebrima 20 underline"), fill="white")
        self.create_surname_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_name = canvas.create_window(20, 50, anchor="nw", window=self.create_surname_entry)

        canvas.create_text(75, 110, text="Prénom :", font=("ebrima 20 underline"), fill="white")
        self.create_name_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_name = canvas.create_window(20, 130, anchor="nw", window=self.create_name_entry)

        self.create_male_check = Checkbutton(self.window_front, text="Homme", font=("ebrima 20 underline"),
                                             fg="#000000", offvalue=OFF, variable=self.homme)
        self.create_female_check = Checkbutton(self.window_front, text="Femme", font=("ebrima 20 underline"),
                                               fg="#000000", offvalue=OFF, variable=self.femme)

        window_H = canvas.create_window(20, 185, anchor="nw", window=self.create_male_check)
        window_F = canvas.create_window(200, 185, anchor="nw", window=self.create_female_check)

        canvas.create_text(65, 255, text="E-Mail :", font=("ebrima 20 underline"), fill="white")
        self.create_mail_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_mail = canvas.create_window(20, 275, anchor="nw", window=self.create_mail_entry)

        canvas.create_text(85, 325, text="Identifiant :", font=("ebrima 20 underline"), fill="white")
        self.create_user_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_identifiant = canvas.create_window(20, 350, anchor="nw", window=self.create_user_entry)

        canvas.create_text(105, 400, text="Mot de passe :", font=("ebrima 20 underline"), fill="white")
        self.create_password_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        self.create_password_entry.config(show="*")
        window_mdp = canvas.create_window(20, 425, anchor="nw", window=self.create_password_entry)

        create_button = Button(self.window_front, text="Créer le compte", font=("ebrima 18 underline"), bg="#ffffff",
                               fg="#000000", bd=2, relief='groove', command=self.create_account_request)

        canvas.create_window(175, 525, window=create_button)
        self.window_front.mainloop()

    def create_account_request(self):

        self.name = self.create_name_entry.get()
        self.surname = self.create_surname_entry.get()
        self.mail = self.create_mail_entry.get()
        self.user = self.create_user_entry.get()
        F = self.femme.get()
        H = self.homme.get()

        if str(F) == '1' and str(H) == '0':
            self.civility = 'F'
        elif str(H) == '1' and str(F) == '0':
            self.civility = 'H'
        else:
            print("Erreur, veulliez préciser la civilité .")

        data = {
            'request': 'Creation',
            'name': self.name,
            'surname': self.surname,
            'civility': self.civility,
            'email': self.mail,
            'user': self.user,
            'password': self.create_password_entry.get()
        }
        infos = self.do_request(data)

        if infos[0]:
            self.window_front.destroy()
            self.window.destroy()
            self.cb = infos[1]
            self.crypto = infos[2]
            self.expiration = infos[3]
            self.last_connection_date = infos[4]
            self.connection_date = infos[4]
            self.token = infos[5]
            self.main_window()
        else:
            print('Erreur dans la requête')

    def main_window(self):
        self.window = Tk()
        self.window.title("Fenètre principale")
        self.window.geometry("1080x720")
        self.window.iconbitmap(self.ico)

        canvas = Canvas(self.window, width=1080, height=720)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=PhotoImage(file="background.png"), anchor="nw")

        canvas.create_text(540, 25, text="Bienvenue sur la banque CQLM", font=("ebrima 30 underline"), fill="white")

        self.main_info_button = Button(self.window, text="Informations \ndu compte", font=("ebrima 22 "), bg="#ffffff",
                                       fg="#000000", bd=2, relief='groove', command=self.info_window)
        canvas.create_window(800, 250, window=self.main_info_button)
        self.main_virement_button = Button(self.window, text="Virement", font=("ebrima 22 "), bg="#ffffff",
                                           fg="#000000", bd=2, relief='groove', command=self.virement_window)
        canvas.create_window(550, 250, window=self.main_virement_button)
        self.main_retrait_button = Button(self.window, text="Retrait", font=("ebrima 22 "), bg="#ffffff", fg="#000000",
                                          bd=2, relief='groove', command=self.retrait_window)
        canvas.create_window(350, 250, window=self.main_retrait_button)
        self.main_depot_button = Button(self.window, text="Depot", font=("ebrima 22 "), bg="#ffffff", fg="#000000",
                                        bd=2, relief='groove', command=self.depot_window)
        canvas.create_window(150, 250, window=self.main_depot_button)

        canvas.create_text(300, 680, text="Mentions légales", font=("ebrima 18 underline"), fill="white")
        canvas.create_text(500, 680, text="Sécurité", font=("ebrima 18 underline"), fill="white")
        canvas.create_text(700, 680, text="En savoir plus", font=("ebrima 18 underline"), fill="white")

        recto = PhotoImage(file="carte_recto.png").zoom(18).subsample(32)
        canvas.create_image(300, 500, image=recto)

        verso = PhotoImage(file="carte_verso.png").zoom(18).subsample(32)
        canvas.create_image(700, 500, image=verso)
        canvas.create_text(180, 523, text=self.cb[:4], font=("ebrima 14"), fill="white")
        canvas.create_text(254, 523, text=self.cb[4:8], font=("ebrima 14"), fill="white")
        canvas.create_text(328, 523, text=self.cb[8:12], font=("ebrima 14"), fill="white")
        canvas.create_text(400, 523, text=self.cb[12:], font=("ebrima 14"), fill="white")

        canvas.create_text(416, 553, text=self.expiration, font=("ebrima 12"), fill="white")
        canvas.create_text(240, 580, text=self.civility + ' ' + self.surname + ' ' + self.name, font=("ebrima 15"),
                           fill="white")
        canvas.create_text(745, 507, text=self.crypto, font=("ebrima 15"), fill="white")

        self.window.mainloop()

    def depot_window(self):
        self.window_front = Toplevel()
        self.window_front.grab_set()
        self.window_front.focus_set()
        self.window_front.title("Depot")
        self.window_front.geometry("300x300")
        self.window_front.iconbitmap(self.ico)
        self.window_front.config(background='#474643')
        canvas = Canvas(self.window_front, width=300, height=300)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.background, anchor='nw')

        canvas.create_text(125, 45, text="Montant du depot", font=("ebrima 20 underline"), fill="white")

        self.depot_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_depot_entry = canvas.create_window(150, 100, anchor="s", window=self.depot_entry)

        self.depot_button = Button(self.window_front, text="Effectuer le depot", font=("ebrima 18 underline"),
                                   bg="#ffffff", fg="#000000", bd=2, relief='groove', command=self.depot_request)
        window_depot_button = canvas.create_window(150, 200, window=self.depot_button)

        self.window_front.mainloop()

    def depot_request(self):
        amount = float(self.depot_entry.get())
        if amount <= 0:
            return
        data = {
            'request': 'CreditDepot',
            'token': self.token,
            'amount': amount
        }
        infos = self.do_request(data)
        if infos[0] == 'True':
            self.sold = infos[1]
            self.window_front.destroy()

    def retrait_window(self):
        self.window_front = Toplevel()
        self.window_front.grab_set()
        self.window_front.focus_set()
        self.window_front.title("Retrait")
        self.window_front.geometry("300x300")
        self.window_front.iconbitmap(self.ico)
        self.window_front.config(background='#474643')
        canvas = Canvas(self.window_front, width=300, height=300)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=PhotoImage(file="background.png"), anchor='nw')

        canvas.create_text(125, 45, text="Montant du retrait", font=("ebrima 20 underline"), fill="white")

        self.retrait_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_depot_entry = canvas.create_window(150, 100, anchor="s", window=self.retrait_entry)

        self.retrait_button = Button(self.window_front, text="Effectuer le retrait", font=("ebrima 18 underline"),
                                     bg="#ffffff", fg="#000000", bd=2, relief='groove', command=self.retrait_request)
        window_depot_button = canvas.create_window(150, 200, window=self.retrait_button)

        self.window_front.mainloop()

    def retrait_request(self):
        amount = float(self.retrait_entry.get())
        if amount <= 0:
            return
        data = {
            'request': 'CreditDepot',
            'token': self.token,
            'amount': amount * -1
        }
        infos = self.do_request(data)
        if infos[0] == 'True':
            self.sold = infos[1]
            self.window_front.destroy()

    def virement_window(self):
        self.window_front = Toplevel()
        self.window_front.grab_set()
        self.window_front.focus_set()
        self.window_front.title("Virement")
        self.window_front.geometry("300x300")
        self.window_front.iconbitmap(self.ico)
        self.window_front.config(background='#474643')
        canvas = Canvas(self.window_front, width=400, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=PhotoImage(file="background.png"), anchor='nw')

        canvas.create_text(145, 20, text="Montant du virement", font=("ebrima 20 underline"), fill="white")
        self.virement_amount_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_virement_entry = canvas.create_window(150, 75, anchor="s", window=self.virement_amount_entry)

        canvas.create_text(140, 95, text="Mail du destinataire", font=("ebrima 20 underline"), fill="white")
        self.virement_mail_entry = Entry(self.window_front, font=("ebrima", 18), width=20, fg="#000000", bd=0)
        window_mail_virement_entry = canvas.create_window(150, 150, anchor="s", window=self.virement_mail_entry)

        self.virement_button = Button(self.window_front, text="Effectuer le virement", font=("ebrima 18 underline"),
                                      bg="#ffffff", fg="#000000", bd=2, relief='groove', command=self.virement_request)
        window_virement_button = canvas.create_window(150, 200, window=self.virement_button)

        self.window_front.mainloop()

    def virement_request(self):
        amount = float(self.virement_amount_entry.get())
        if amount <= 0:
            return
        data = {
            'request': 'Transaction',
            'token': self.token,
            'amount': amount,
            'direction': self.virement_mail_entry.get()
        }
        infos = self.do_request(data)
        if infos[0] == 'True':
            self.sold = infos[1]
            self.window_front.destroy()

    def info_window(self):
        self.window_front = Toplevel()
        self.window_front.grab_set()
        self.window_front.focus_set()
        self.window_front.title("Informations des transactions")
        self.window_front.geometry("650x324")
        self.window_front.iconbitmap(self.ico)
        self.window_front.config(background='#474643')
        canvas = Canvas(self.window_front, width=500, height=500)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=PhotoImage(file="background.png"), anchor='nw')
        infos = self.info_request()
        for y in range(5):
            for x in range(4):
                canvas.create_text(100 + x * 175, 100 + x * 50, text=infos[y][x], font=("ebrima 18"), fill="white")

        canvas.create_line(0, 75, 650, 75, width=2, fill='white')
        canvas.create_line(0, 125, 650, 125, width=2, fill='white')
        canvas.create_line(0, 175, 650, 175, width=2, fill='white')
        canvas.create_line(0, 225, 650, 225, width=2, fill='white')
        canvas.create_line(0, 275, 650, 275, width=2, fill='white')
        canvas.create_line(0, 325, 650, 325, width=2, fill='white')

        canvas.create_line(175, 0, 175, 350, width=2, fill='white')
        canvas.create_line(380, 0, 380, 350, width=2, fill='white')
        canvas.create_line(500, 0, 500, 350, width=2, fill='white')

        canvas.create_text(85, 35, text="Type de\ntransaction", font=("ebrima 18"), fill="white")
        canvas.create_text(275, 35, text="Date de la\ntransaction", font=("ebrima 18"), fill="white")
        canvas.create_text(435, 35, text="Montant", font=("ebrima 18"), fill="white")
        print('ptdr')
        self.window_front.mainloop()

    def info_request(self):
        data = {
            'request': 'TransactionLogs',
            'token': self.token
        }
        infos = self.do_request(data)
        if infos[0] == 'True':
            return infos[1]


b = BankApp()
b.connection_token()
