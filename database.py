import pyodbc

class Manipulate_database:

    def __init__(self):
        pass

    def connect_immutable_database(self):

        # DADOS DE LOCALIZAÇÃO DA BLOCKCHAIN NO BANCO
        database_driver = "Sql Server;"
        server = "DESKTOP-0KMRQR5\SQLEXPRESS;"
        database = "CrudDelage;"
        user = ""
        password = ""

        #FAZ CONEXÃO COM O BANCO QUE OS ARQUIVOS SERÃO ESCRITOS
        print("     -----   CONNECTING TO BLOCKCHAIN   -----")
        try:
            connection = pyodbc.connect(f"""DRIVER={database_driver};SERVER={server};DATABASE={database};UID={user};PWD={password}""")
        except Exception:
            print("        BLOCKCHAIN CONNECTION ERROR")
            exit()

        else:
            print("             BLOCKCHAIN CONNECTION SUCCESS ")
            return connection

        finally:
            print("")

    def get_last_hash(self):
        table = "HISTORICO_HASH"

        #FAZ PEDIDO DE CONEXÃO
        cursor = self.connect_immutable_database().cursor()
        # FAZ A SEARCH NO Banco DE FORMA QUE O ULTIMO ID SEJA SELECIONADO 1°
        search = f"""SELECT CURRENT_HASH FROM {table} ORDER BY ID DESC"""

        cursor.execute(search)
        row = cursor.fetchall()

        #TRAZ APENAS O MAIOR ID
        global last_hash
        for last_hash in row:
            last_hash = last_hash[0]
            break
        if row == []:
            last_hash = 0
        return last_hash


    def record_blockchain_data(self,last_hash,current_hash,nonce,content):
        table = "HISTORICO_HASH"

        #FAZ PEDIDO DE CONEXÃO
        cursor = self.connect_immutable_database().cursor()

        insert = f"""INSERT INTO {table}(LAST_HASH,CURRENT_HASH,NONCE,CONTENT)
                VALUES('{last_hash}','{current_hash}','{nonce}','{content}');"""

        cursor.execute(insert)

        #INSERT OS DADOS NA BLOCKCAHIN
        cursor.commit()
        cursor.close()
