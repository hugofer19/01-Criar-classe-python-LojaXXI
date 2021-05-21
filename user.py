import psycopg2


class User:
    db = 'db/Utilizadores.xlsx'

    def __init__(self):
        self.reset()

    def reset(self):
        self.id = None
        self.cliente = ''
        self.email = ''
        self.password = ''
        self.nif = ''
        self.nome = ''
        self.morada = ''

    def herokudb(self):
        Host = 'ec2-52-209-134-160.eu-west-1.compute.amazonaws.com'
        Database = 'dav5i22li2jrrj'
        User = 'itmuvbfzedxqkj'
        Password = 'cdbd5af7afc2a1330589b97900c5e29dbf9e334a666667fb5a7ab5f42e349f00'
        return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')

    def gravar(self, v1, v2, v3):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
        db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, self.code(v3)))
        ficheiro.commit()
        ficheiro.close()

    def existe(self, v1):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self,v1, v2):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, self.code(v2),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, v1, v2):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (self.code(v2), v1))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, v1):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM usr WHERE nome = %s", (v1,))
        ficheiro.commit()
        ficheiro.close()

    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from usr ORDER BY nome")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = None
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()

