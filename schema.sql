-- Remove tabelas existentes (caso precise recriar o banco)
DROP TABLE IF EXISTS Aluguel;
DROP TABLE IF EXISTS Jogo;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Console;

-- Criação da tabela Console
CREATE TABLE Console (
    ID_Console SERIAL PRIMARY KEY,
    Modelo VARCHAR(50) NOT NULL,
    Ano_Lancamento INT
);

-- Criação da tabela Jogo
CREATE TABLE Jogo (
    ID_Jogo SERIAL PRIMARY KEY,
    Titulo VARCHAR(200) NOT NULL,
    Ano INT,
    ID_Console INT NOT NULL REFERENCES Console(ID_Console) ON DELETE CASCADE,
    Preco_Diaria DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_Console) REFERENCES Console(ID_Console)
);

-- Criação da tabela Cliente
CREATE TABLE Cliente (
    ID_Cliente SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Telefone VARCHAR(15),
    Email VARCHAR(100) UNIQUE
);

-- Criação da tabela Aluguel
CREATE TABLE Aluguel (
    ID_Aluguel SERIAL PRIMARY KEY,
    ID_Cliente INT NOT NULL,
    ID_Jogo INT,
    ID_Console INT,
    Data_Aluguel DATE DEFAULT CURRENT_DATE,
    Data_Devolucao DATE,
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Jogo) REFERENCES Jogo(ID_Jogo),
    FOREIGN KEY (ID_Console) REFERENCES Console(ID_Console),
    -- Garante que o aluguel é de um jogo OU um console
    CHECK (ID_Jogo IS NOT NULL OR ID_Console IS NOT NULL)
);