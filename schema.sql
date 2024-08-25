DROP TABLE IF EXISTS tb_usuario;

CREATE TABLE tb_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nascimento DATE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

DROP TABLE IF EXISTS tb_produto;
CREATE TABLE tb_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    setor_id INTEGER NOT NULL,
    foreign key (categoria_id) references tb_categoria(id),
    foreign key (setor_id) references tb_setor(id)
);

DROP TABLE IF EXISTS tb_categoria;
CREATE TABLE tb_categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

DROP TABLE IF EXISTS tb_setor;
CREATE TABLE tb_setor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);


insert into tb_usuario(nome, nascimento) values ('Administrador', '2024-07-23');