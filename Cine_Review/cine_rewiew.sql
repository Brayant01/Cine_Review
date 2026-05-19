create database cine_review;
use cine_review;

create table usuario(  -- pronto no py
  id int primary key auto_increment not null,
  nome varchar(150) not null,
  senha varchar(255) not null,
  email varchar(255) not null unique,
  type_user tinyint (1) default 0
);

create table categoria( -- pronto no py
  id int primary key auto_increment not null,
  genero varchar(65) not null
);

create table filme( -- pronto no py
  id int primary key auto_increment not null,
  titulo varchar(255) not null,
  ano_lancamento year not null,
  sinopse text not null,
  classificacao_indicativa enum('L', '10', '12', '14', '16', '18') not null
);

create table film_cat(  -- pronto no py
  id_filme int not null,
  id_categoria int not null,
  primary key(id_filme, id_categoria),
  foreign key (id_filme) references filme(id),
  foreign key (id_categoria) references categoria(id)
);

create table avaliacao( 
  id int primary key auto_increment not null,
  id_usuario int not null,
  id_filme int not null,
  nota tinyint unsigned not null check (nota <= 10),
  comentario text not null,
  dia_avaliacao timestamp not null default current_timestamp,
  foreign key(id_usuario) references usuario(id),
  foreign key(id_filme) references filme(id),
  unique (id_usuario, id_filme)
);

INSERT INTO filme(titulo, ano_lancamento, sinopse, classificacao_indicativa)
VALUES 
(
'A Última Fronteira', 
2021,
'Um ex-soldado precisa atravessar uma cidade destruída para salvar sua família durante uma guerra civil.',
'16'
),

(
'Estrelas do Amanhã',
2019,
'Um grupo de crianças descobre um observatório abandonado e começa uma aventura pelo universo.',
'L'
),

(
'Código Fantasma',
2023,
'Um jovem programador encontra um algoritmo misterioso capaz de invadir qualquer sistema do mundo.',
'14'
),

(
'Noite Sem Volta',
2020,
'Após testemunhar um crime, uma jornalista é perseguida por uma organização criminosa.',
'18'
),

(
'O Jardim de Elisa',
2018,
'Uma garota tímida encontra um jardim mágico capaz de realizar pequenos desejos.',
'10'
),

(
'Horizonte Vermelho',
2024,
'Colonizadores em Marte enfrentam uma ameaça desconhecida escondida abaixo da superfície do planeta.',
'16'
),

(
'Sombras da Cidade',
2022,
'Um detetive investiga desaparecimentos misteriosos ligados ao submundo da cidade.',
'14'
),

(
'Velocidade Máxima',
2017,
'Um piloto iniciante tenta vencer o campeonato nacional de corrida enquanto enfrenta rivais experientes.',
'12'
),

(
'Além do Tempo',
2021,
'Dois estudantes encontram um relógio antigo capaz de voltar alguns minutos no passado.',
'10'
),

(
'Operação Eclipse',
2025,
'Uma equipe secreta tenta impedir um ataque internacional que ameaça milhões de pessoas.',
'18'
);

INSERT INTO categoria (genero)
VALUES
('Ação'),
('Ficção Científica'),
('Drama'),
('Suspense'),
('Terror'),
('Comédia'),
('Romance'),
('Aventura'),
('Fantasia'),
('Mistério');

INSERT INTO film_cat (id_filme, id_categoria)
VALUES

-- A Última Fronteira
(1, 1),
(1, 8),

-- Além do Tempo
(2, 7),
(2, 2),

-- Código Fantasma
(3, 2),
(3, 4),

-- Estrelas do Amanhã
(4, 9),
(4, 8),

-- Horizonte Vermelho
(5, 1),
(5, 3),

-- Noite Sem Volta
(6, 5),
(6, 4),

-- O Jardim de Elisa
(7, 3),
(7, 7),

-- Operação Eclipse
(8, 1),
(8, 2),

-- Sombras da Cidade
(9, 10),
(9, 4),

-- Velocidade Máxima
(10, 1),
(10, 8);