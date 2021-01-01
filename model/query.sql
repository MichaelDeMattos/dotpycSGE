------------------------------------------------------------------------
create table empresa
(
  cod_empresa integer not null,
  razao_social varchar(100) not null,
  cpf_cnpj varchar(50) not null,
  data_contracao timestamp default current_timestamp,
  situacao varchar(1),
  chave varchar(500),
  constraint pk_empresa_cod_empresa primary key (cod_empresa)
);

alter table empresa add constraint chk_empresa_situacao
  check (situacao in ('L', 'B', 'D'));

create sequence sq_empresa_pk;

set term ^ ;
create trigger tg_cod_empresa_pk for empresa active
before insert position 0
as
begin
  if (new.cod_empresa is null) then begin
    new.cod_empresa = gen_id(sq_empresa_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------
create table login
(
  cod_login integer not null,
  usuario varchar(30) not null,
  senha varchar(30) not null,
  cod_empresa integer not null,
  constraint pk_login_cod_login primary key (cod_login)
);

alter table login add constraint fk_login_cod_empresa
  foreign key (cod_empresa) references empresa (cod_empresa);
  
create sequence sq_login_pk;

set term ^ ;
create trigger tg_cod_login for login active
before insert position 0
as
begin
  if (new.cod_login is null) then begin
    new.cod_login = gen_id(sq_login_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------

create table config_servidor (
    cod_config_servidor integer,
    servidor varchar(500) not null,
    email varchar(500) not null,
    tipo varchar(10) not null,
    porta integer not null,
    cod_usuario_registro integer not null, 
    data_registro timestamp default current_timestamp,
    constraint pk_config_servidor primary key (cod_config_servidor),
    constraint fk_config_servidor_cod_usuario foreign key (cod_usuario_registro)
        references login(cod_login)
);

create sequence sq_config_servidor_pk;

set term ^ ;
create trigger tg_config_servidor_pk for config_servidor active
before insert position 0
as
begin
  if (new.cod_config_servidor is null) then begin
    new.cod_config_servidor = gen_id(sq_config_servidor_pk, 1);
  end
end^
set term ; ^

alter table config_servidor add senha varchar(500) not null;
-----------------------------------------------------------------------

create table entidade (
    cod_entidade integer, 
    nome varchar(500) not null,
    sobrenome varchar(500) not null,
    telefone varchar(15) not null,
    celular varchar(15) not null,
    email varchar(500) not null,
    tipo_morador char(1) not null,
    cod_usuario_registro integer not null,
    data_registro timestamp default current_timestamp,
    constraint pk_entidade_cod_entidade
        primary key (cod_entidade),
    constraint fk_entidade_cod_usuario_reg
        foreign key (cod_usuario_registro)
        references login(cod_login)
);


create sequence sq_entidade_pk;

set term ^ ;
create trigger tg_entidade_pk for entidade active
before insert position 0
as
begin
  if (new.cod_entidade is null) then begin
    new.cod_entidade = gen_id(sq_entidade_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------

create table apartamento(
    cod_apartamento integer,
    bloco varchar(20) not null,
    andar varchar(20) not null,
    apartamento integer not null,
    cod_usuario_registro integer not null,
    data_registro timestamp default current_timestamp,
    constraint pk_apartamento
        primary key(cod_apartamento),
    constraint fk_apartamento_cod_usu_reg
        foreign key (cod_usuario_registro)
        references login(cod_login)
);

create sequence sq_apartamento_pk;

set term ^ ;
create trigger tg_apartamento_pk for apartamento active
before insert position 0
as
begin
  if (new.cod_apartamento is null) then begin
    new.cod_apartamento = gen_id(sq_apartamento_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------

create table endereco(
    cod_endereco integer,
    cod_entidade integer not null,
    cod_apartamento integer not null,
    cod_usuario_registro integer not null,
    data_registro timestamp default current_timestamp,
    constraint pk_endereco
        primary key(cod_endereco),
    constraint fk_endereco_cod_entidade
        foreign key(cod_entidade)
        references entidade(cod_entidade),
    constraint fk_endereco_cod_apartamento
        foreign key (cod_apartamento)
        references apartamento(cod_apartamento),
    constraint fk_endereco_cod_usu_reg
        foreign key (cod_usuario_registro)
        references login(cod_login)
);

create sequence sq_endereco_pk;

set term ^ ;
create trigger tg_endereco_pk for endereco active
before insert position 0
as
begin
  if (new.cod_endereco is null) then begin
    new.cod_endereco = gen_id(sq_endereco_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------
alter table entidade drop telefone;
alter table entidade add rg varchar(20) not null;
alter table apartamento drop apartamento;
alter table apartamento add numero integer not null;
------------------------------------------------------------------------

create table entrega
(
  cod_entrega integer not null,
  cod_apartamento integer not null,
  cod_entidade integer not null,
  remetente varchar(500) not null,
  entregador varchar(500) default 'CORREIOS' not null,
  prazo_retirada varchar(20) not null,
  obs varchar(500) not null,
  data_registro timestamp default current_timestamp,
  cod_usuario_registro integer not null,
  status char(1) default 'A' check(status in ('A', 'F', 'B', 'D')) not null,
  data_final timestamp,
  obs_final varchar(500),
  cod_usuario_final integer,
  constraint pk_entrega
    primary key (cod_entrega),
  constraint fk_entrega_cod_usu_reg
    foreign key (cod_usuario_registro)
    references login(cod_login),
  constraint fk_entrega_cod_usu_final
    foreign key (cod_usuario_final)
    references login(cod_login),
  constraint fk_entrega_cod_ap
    foreign key (cod_apartamento)
    references apartamento(cod_apartamento),
  constraint fk_entrega_cod_entidade
    foreign key (cod_entidade)
    references entidade(cod_entidade)
);

create sequence sq_entrega_pk;

set term ^ ;
create trigger tg_entrega_pk for entrega active
before insert position 0
as
begin
  if (new.cod_entrega is null) then begin
    new.cod_entrega = gen_id(sq_entrega_pk, 1);
  end
end^
set term ; ^

------------------------------------------------------------------------

alter table entidade add status char(1) default 'A' check (status in ('A', 'I'));
