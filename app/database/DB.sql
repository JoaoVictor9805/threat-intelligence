CREATE DATABASE threat_intelligence;

CREATE TABLE consulta (
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
indicador VARCHAR(255) NOT NULL,
tipo ENUM('ip', 'dominio', 'hash') NOT NULL,
fonte VARCHAR(50) NOT NULL,
dataConsulta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, resultado JSON NOT NULL
);

USE threat_intelligence;
SELECT * FROM CONSULTA;

USE threat_intelligence;
TRUNCATE TABLE consulta;

CREATE EVENT limpar_consultas_antigas
ON SCHEDULE EVERY 1 DAY
DO
    DELETE FROM consulta
    WHERE dataConsulta < CURRENT_TIMESTAMP - INTERVAL 30 DAY;

USE threat_intelligence;
ALTER TABLE consulta ADD COLUMN resumo_ia TEXT NULL;