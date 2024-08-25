import os
import psycopg2

# Conecta ao banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="cafedatabase",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS tb_usuario;')

# Cria a tabela 'tb_usuario'
cur.execute('''
    CREATE TABLE tb_usuario (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        nascimento DATE NOT NULL
    );
''')

conn.commit()

cur.close()
conn.close()

print("Tabela tb_usuario criada com sucesso.")
