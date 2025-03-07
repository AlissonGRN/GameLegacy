-- Inserir consoles retro
INSERT INTO Console (Modelo, Ano_Lancamento) 
VALUES 
  ('Super Nintendo', 1990),
  ('Mega Drive', 1988),
  ('NES', 1985);

-- Inserir jogos clássicos
INSERT INTO Jogo (Titulo, Ano, ID_Console, Preco_Diaria) 
VALUES 
  ('Super Mario World', 1990, 1, 20.00),
  ('The Legend of Zelda', 1986, 3, 18.00),
  ('Sonic the Hedgehog 2', 1992, 2, 15.00),
  ('Metroid', 1986, 3, 12.00);

-- Inserir clientes
INSERT INTO Cliente (Nome, Telefone, Email) 
VALUES 
  ('João Silva', '(11) 99999-9999', 'joao@email.com'),
  ('Maria Oliveira', '(21) 88888-8888', 'maria@email.com'),
  ('Carlos Souza', '(31) 77777-7777', 'carlos@email.com');

-- Inserir aluguéis de exemplo
INSERT INTO Aluguel (ID_Cliente, ID_Jogo, ID_Console, Data_Aluguel, Data_Devolucao) 
VALUES 
  -- João alugou "Super Mario World" (jogo) em 20/03/2024 (não devolveu)
  (1, 1, NULL, '2024-03-20', NULL),
  -- Maria alugou um "Mega Drive" (console) em 21/03/2024 (devolveu em 25/03)
  (2, NULL, 2, '2024-03-21', '2024-03-25'),
  -- Carlos alugou "Metroid" (jogo) em 22/03/2024 (não devolveu)
  (3, 4, NULL, '2024-03-22', NULL);