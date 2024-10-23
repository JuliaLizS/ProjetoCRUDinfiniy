CREATE database industria_wayne;

use industria_wayne;

CREATE TABLE usuario (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    tipo ENUM('administrador','funcionario', 'gerente') NOT NULL,
    senha VARCHAR(60) NOT NULL
);

CREATE TABLE veiculo (
	id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(7) NOT NULL UNIQUE,
    modelo VARCHAR(30),
    marca VARCHAR(30),
    cor VARCHAR(15)
);

CREATE TABLE dispositivo (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT
);

/* TRIGGER */

DELIMITER $

CREATE TRIGGER CHECK_QUANTIDADE_INSERT
BEFORE INSERT ON dispositivo
FOR EACH ROW
BEGIN
	IF NEW.quantidade < 0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Erro: Quantidade negativa inserida";
	END IF;
END $

CREATE TRIGGER CHECK_QUANTIDADE_UPDATE
BEFORE UPDATE ON dispositivo
FOR EACH ROW
BEGIN
	IF NEW.quantidade < 0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Erro: Quantidade negativa inserida";
	END IF;
END $

DELIMITER ;

INSERT INTO usuario (nome, email, tipo, senha) VALUES ('Joao', 'joao@exemplo.com', 'administrador', 'hashed_senha');
INSERT INTO usuario (nome, email, tipo, senha) VALUES ('Maria', 'maria@exemplo.com', 'funcionario', 'hashed_senha');
INSERT INTO usuario (nome, email, tipo, senha) VALUES ('Joana', 'joana@exemplo.com', 'gerente', 'hashed_senha');

INSERT INTO veiculo (placa, modelo, marca, cor) VALUES ('pxu5236', 'ka', 'ford', 'azul');
INSERT INTO veiculo (placa, modelo, marca, cor) VALUES ('ouw2536', 'spin', 'wolksvagen', 'amarelo');
INSERT INTO veiculo (placa, modelo, marca, cor) VALUES ('was1425', 'sandero', 'renaul', 'vermelho');


INSERT INTO dispositivo (nome, tipo, quantidade) VALUES ('radio', 'pessoal', 3);

select * from usuario;


DESCRIBE usuario;








