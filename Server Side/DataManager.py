class File:
    """Class to manage data files"""

    def __init__(self, file_name, path=''):
        """Class initialization function

        Args:
            self (File request_type): Current class object
            file_name (str): Name of the data file
            path (str, optional): Path to the data file. Defaults to ''.
        """

        self.fileName = file_name
        self.path = path
        try:
            self.file = open(str(self.path) + str(self.fileName), 'r')
            self.labels = self.file.readline().replace('\n', '').split(',')
            self.content = [line.replace('\n', '').split(',') for line in self.file.readlines()]
            self.file.close()
        except FileNotFoundError:
            file = open(str(self.path) + str(self.fileName), 'w')
            file.close()
            self.file = open(str(self.path) + str(self.fileName), 'r')
            self.labels = self.file.readline().replace('\n', '').split(',')
            self.content = [line.replace('\n', '').split(',') for line in self.file.readlines()]
            self.file.close()

    def get_data(self, column=None, line=None, column_id='id'):
        """Get a data in the data file

        Args:
            self (File request_type): Current class object
            column (str, optional): Column of the data we want. Defaults to None.
            line (int/str, optional): Column of the data we want. Defaults to None.
            column_id (str, optional): Id of the column if line is not a int. Defaults to 'id'.

        Returns:
            str: Data we want to get
            NoneType: return this if error
        """

        if line is not None and isinstance(line, str):
            line = self.get_index_of_data(line, column_id)
        if (column is None and line is None) or (column is not None and not isinstance(column, str)) or (
                line is not None and not isinstance(line, int)) or (column is None and line >= len(self.content)) or (
                line is None and column not in self.labels):
            print('Error - get_data')
            data = None

        elif column is None:
            data = self.content[line]

        elif column not in self.labels:
            print('Error - get_data')
            data = None

        elif line is None:
            data = [i[self.labels.index(column)] for i in self.content]

        elif line >= len(self.content):
            print('Error - get_data')
            data = None

        else:
            data = self.content[line][self.labels.index(column)]

        return data

    def get_index_of_data(self, data, column):
        """Get index of the line of a data 

        Args:
            self (File request_type): Current class object
            data (str): Data that we want to know the line
            column (str): Column where the data is

        Returns:
            int: Index of the line
            NoneType: Return if error
        """
        cData = self.get_data(column=column)
        if data not in cData:
            print('Error - get_index_of_data')
            return None
        return cData.index(data)

    def set_data(self, data, column, line, column_id='id'):
        """Set a data in the data file

        Args:
            self (File request_type): Current class object
            data (str): Data we want to set
            column (str): Column where we want to set a data
            line (int/str): Line where we want to set a data
            column_id (str, optional): Id of the column if line is not a int. Defaults to 'id'.
        """

        if isinstance(line, str):
            line = self.get_index_of_data(line, column_id)

        if not isinstance(column, str) or not isinstance(line, int) or line >= len(self.content) or column not in \
                self.labels or line is None:
            print('Error - set_data')
            return

        self.content[line][self.labels.index(column)] = data

        file = open(str(self.path) + str(self.fileName), 'w')
        file.write(assemble_content(self.labels, content=self.content))
        file.close()

        return

    def add_line(self, line=None, lines=None):
        """Add a line at the end of the data file

        Args:
            self (File request_type): Current class object
            line (list[str], optional): Elements to push into a new line. Defaults to None.
            lines (list[list[str]], optional): Elements to push into new lines. Defaults to None.
        """
        if line is None:
            labels = lines[0]
            content = lines[1:]
        else:
            labels = line
            content = None
        file = open(str(self.path) + str(self.fileName), 'a')
        file.write(assemble_content(labels, content=content))
        file.close()

    def remove_line(self, line, column_id='id'):
        """Remove a line into the data file

        Args:
            self (File request_type): Current class object
            line (int/str): Index of the line we want to delete
            column_id (str, optional): Id of the column if line is not a int. Defaults to 'id'.
        """

        if isinstance(line, str):
            line = self.get_index_of_data(line, column_id)

        if not isinstance(line, int) or line >= len(self.content) or line is None:
            print('Error - removeData')
            return

        del self.content[line]

        file = open(str(self.path) + str(self.fileName), 'w')
        c = ''
        for i in self.content:
            c = c + i
        file.write(self.labels + c)
        file.close()


def assemble_content(labels, content=None):
    """Assemble a content to the CSV format

    Args:
        labels (list[str]): Labels of the data file
        content (list[str], optional): Content of the data file. Defaults to None.

    Returns:
        str: Content in the CSV format
    """

    r = ''
    for label in labels:
        r = r + str(label) + ','
    r = r.rstrip(',')
    r = r + '\n'
    if content is not None:
        for line in content:
            for item in line:
                r = r + str(item) + ','
            r = r.rstrip(',')

            r = r + '\n'
    return r

# #Définition d'un objet portant toutes les infos concernant le dossier CSV qu'on veut ouvrir
# # -> <une variable> = File(<nom du csv.csv>, path=<chemin depuis votre fichier pour aller au fichier>[inutile si dans le même endroit])
# f = File('Op_banq3def.csv', path='./Data/')

# #Depuis notre objet nous pouvons ouvrir et récuperer des données avec la fonction get_data(column=<label de votre colonne(Id, nom, prenom, ...)>, line=<l'index de votre ligne en partant de 0 sans compter les labels ou alors en utilisant l'user_id correspondant à la ligne>)
# #Si vous ne mettez pas column=... on vous retournera sous la forme d'une liste la totalité de la ligne
# #Si vous ne mettez pas line=... on vous retournera sous la forme d'une liste la colonne entière
# data = f.get_data(line=10)
# print(data)

# #Nous pouvons aussi récuperer l'index d'une ligne de donnée avec get_index_of_data(la donnée dont vous voulez savoir la ligne, la colonne dont vous avez la donnée)

# #Depuis notre objet nous pouvons définir des données dans la base de données avec la fonction set_data(votre donnée, la colonne(fonctionne comme dans le get_data hormis le fait que là il est obligatoire), la ligne(même chose que pour la colonne))
# f.set_data(62, 'Id', 10)
# print(f.get_data(line=1))

# #On peut aussi ajouter une ligne à la fin de la base de données avec la fonction add_line(vos données sous la forme d'une liste(voir les labels))
# f.add_line(line=['53', '01/01/2021', '530101053', 'Edouard', 'A', '0', '5000', '0', '5000'])
# print(f.get_data(line=-1))

# #On peut aussi enlever une ligne avec la fonction remove_line(la ligne(comme dans le set data))
# f.remove_line(-1)
# print(f.get_data(line=-1))
