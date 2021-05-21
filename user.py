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
        Host = 'ec2-54-74-14-109.eu-west-1.compute.amazonaws.com'
        Database = 'd8i5e964chmjgj'
        User = 'psgtekdhofssij'
        Password = '04e85cf222296a32c40d9354d7aa92d5b1a7c961a994f0f5c67faa9f1941e46c'
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

