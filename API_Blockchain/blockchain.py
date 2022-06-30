from hashlib import sha256
from datetime import datetime
from database import Manipulate_database

database = Manipulate_database()

class BlockchainChanges:

    def __init__(self):
        self.colors = 0

    def mining_difficulty(self, hash_attempt):
        return hash_attempt.startswith('0')


    def create_genesis_block(self,time,last_hash):
        content = 'Blockchain started.'
        self.create_new_block(content,time,last_hash)


    def create_new_block(self,content,time,last_hash):
        current_hash = ''
        nonce = int(time)

        while not self.mining_difficulty(current_hash):
            new_block = '{}:{}:{}:{}'.format(
                content, time, last_hash, nonce)
            current_hash = sha256(new_block.encode()).hexdigest()
            nonce += 1

        if self.colors == 0:
            cor = "\033[1;30;104m "
            cor2 = "\033[1;30;102m "
            self.colors += 1
        else:
            cor = "\033[1;30;102m "
            cor2 = "\033[1;30;104m "
            self.colors -= 1

        print(f"""
                                    -----  BLOCK CREATED -----
            NONCE: {nonce}
            LAST HASH:    {cor}{last_hash}\033[m 
            CURRENT HASH: {cor2}{current_hash}\033[m 
            CONTENT: {content}
""")
        database.record_blockchain_data(last_hash,current_hash,nonce,content)


    def new_block(self,content):

        time = datetime.utcnow().timestamp()
        last_hash = database.get_last_hash()
        if last_hash == 0:
            self.create_genesis_block(time,last_hash)

            #PARA CONTINUAR COM OS DADOS CHAMAMOS O HASH NOVAMENTE E CRIMOS UM NOVO BLOCO
            last_hash = database.get_last_hash()
            self.create_new_block(content, time, last_hash)
        else:
            self.create_new_block(content, time, last_hash)


