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