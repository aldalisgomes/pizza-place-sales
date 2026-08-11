USE PizzaSales;
GO
-- ============================================================
-- PROJETO: Pizza Place Sales - Estudo de SQL Avançado
-- CONTEÚDO: WHERE Complexos, LIKE, IN, BETWEEN, 
--           JOINS (INNER, LEFT, RIGHT, FULL), GROUP BY, 
--           Subconsultas e Operadores de Conjunto.
-- ============================================================

---------------------------------------------------------------
-- 1. CONDIÇÕES COMPLEXAS, LIKE, IN e BETWEEN
---------------------------------------------------------------

-- 1.1. Extrair pizzas que custam entre $15 e $20 e são tamanho L ou XL
-- (Uso de BETWEEN e IN)
SELECT 
    pizza_id,
    pizza_type_id,
    size,
    price
FROM pizzas
WHERE price BETWEEN 15.00 AND 20.00
  AND size IN ('L', 'XL');


-- 1.2. Buscar pizzas que tenham 'Chicken' no nome, MAS NÃO sejam tamanho 'S'
-- (Uso de LIKE, AND e NOT)
SELECT 
    p.pizza_id,
    pt.name,
    p.size,
    p.price
FROM pizzas p
JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
WHERE pt.name LIKE '%Chicken%' 
  AND NOT p.size = 'S';


---------------------------------------------------------------
-- 2. TRABALHANDO COM VÁRIAS TABELAS (JOINS)
---------------------------------------------------------------

-- 2.1. INNER JOIN (Retorna apenas os registros que têm correspondência nas duas tabelas)
-- Ex: Detalhes dos pedidos junto com o nome e categoria da pizza
SELECT TOP 100
    od.order_id,
    pt.name AS Pizza_Nome,
    c.category_name,
    od.quantity
FROM order_details od
INNER JOIN pizzas p ON od.pizza_id = p.pizza_id
INNER JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
INNER JOIN categories c ON pt.category_id = c.category_id;


-- 2.2. LEFT JOIN (Retorna TUDO da tabela da esquerda e os correspondentes da direita)
-- Ex: Garantir que todos os tipos de pizza apareçam, mesmo que não tenham vendido nada (hipotético)
SELECT 
    pt.name AS Pizza,
    SUM(od.quantity) AS Total_Vendido
FROM pizza_types pt
LEFT JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
LEFT JOIN order_details od ON p.pizza_id = od.pizza_id
GROUP BY pt.name
ORDER BY Total_Vendido ASC;


-- 2.3. RIGHT JOIN (Retorna TUDO da tabela da direita e os correspondentes da esquerda)
-- Ex: Listar todas as categorias e encontrar suas pizzas (inverso do anterior)
SELECT 
    pt.name AS Pizza,
    c.category_name
FROM pizza_types pt
RIGHT JOIN categories c ON pt.category_id = c.category_id;


-- 2.4. FULL OUTER JOIN (Retorna tudo de ambas as tabelas, cruzando onde há correspondência)
-- Útil em auditorias para achar "órfãos" (ex: uma pizza que não tem tipo ou um tipo que não tem pizza)
SELECT 
    p.pizza_id,
    pt.name
FROM pizzas p
FULL OUTER JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
WHERE p.pizza_id IS NULL OR pt.pizza_type_id IS NULL; -- Filtra apenas os problemas


---------------------------------------------------------------
-- 3. RELATÓRIOS SIMPLES (GROUP BY E FUNÇÕES AGREGADAS)
---------------------------------------------------------------

-- 3.1. Quantidade de pedidos, total de pizzas e média de pizzas por pedido diário
SELECT 
    o.date AS Data_Pedido,
    COUNT(DISTINCT o.order_id) AS Total_Pedidos,
    SUM(od.quantity) AS Total_Pizzas_Vendidas,
    AVG(CAST(od.quantity AS DECIMAL(5,2))) AS Media_Pizzas_Por_Pedido
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
GROUP BY o.date
ORDER BY Total_Pizzas_Vendidas DESC;


---------------------------------------------------------------
-- 4. SUBCONSULTAS (SUBQUERIES)
---------------------------------------------------------------

-- 4.1. Subconsulta no WHERE: 
-- Quais são os detalhes dos pedidos que incluíram a pizza MAIS CARA do cardápio?
SELECT 
    order_id,
    pizza_id,
    quantity
FROM order_details
WHERE pizza_id IN (
    -- Subconsulta: Encontra o ID da(s) pizza(s) com o maior preço
    SELECT pizza_id 
    FROM pizzas 
    WHERE price = (SELECT MAX(price) FROM pizzas)
);


-- 4.2. Subconsulta no SELECT:
-- Calcular o faturamento de cada pizza e mostrar a % que ela representa no faturamento total geral
SELECT 
    pt.name AS Nome_Pizza,
    SUM(od.quantity * p.price) AS Faturamento_Pizza,
    (SUM(od.quantity * p.price) / 
        (SELECT SUM(quantity * price) FROM order_details od2 JOIN pizzas p2 ON od2.pizza_id = p2.pizza_id)
    ) * 100 AS Porcentagem_Do_Total
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
GROUP BY pt.name
ORDER BY Faturamento_Pizza DESC;


---------------------------------------------------------------
-- 5. OPERAÇÕES DE CONJUNTO (UNION, INTERSECT, EXCEPT)
---------------------------------------------------------------

-- 5.1. UNION (Combina resultados empilhando um embaixo do outro, removendo duplicatas)
-- Ex: Uma lista de nomes de ingredientes que possuem "Cheese" OU "Garlic"
SELECT ingredient_name FROM ingredients WHERE ingredient_name LIKE '%Cheese%'
UNION
SELECT ingredient_name FROM ingredients WHERE ingredient_name LIKE '%Garlic%';


-- 5.2. INTERSECT (Retorna apenas os resultados que existem em AMBAS as consultas)
-- Ex: Quais ingredientes são usados TANTO na categoria 'Veggie' QUANTO na categoria 'Classic'?
SELECT i.ingredient_name
FROM ingredients i
JOIN pizza_type_ingredients pti ON i.ingredient_id = pti.ingredient_id
JOIN pizza_types pt ON pti.pizza_type_id = pt.pizza_type_id
JOIN categories c ON pt.category_id = c.category_id
WHERE c.category_name = 'Veggie'

INTERSECT

SELECT i.ingredient_name
FROM ingredients i
JOIN pizza_type_ingredients pti ON i.ingredient_id = pti.ingredient_id
JOIN pizza_types pt ON pti.pizza_type_id = pt.pizza_type_id
JOIN categories c ON pt.category_id = c.category_id
WHERE c.category_name = 'Classic';


-- 5.3. EXCEPT (Retorna os resultados da primeira consulta MENOS os que aparecem na segunda)
-- Ex: Quais ingredientes existem na categoria 'Veggie' que NUNCA aparecem na categoria 'Meat'?
SELECT i.ingredient_name
FROM ingredients i
JOIN pizza_type_ingredients pti ON i.ingredient_id = pti.ingredient_id
JOIN pizza_types pt ON pti.pizza_type_id = pt.pizza_type_id
JOIN categories c ON pt.category_id = c.category_id
WHERE c.category_name = 'Veggie'

EXCEPT

SELECT i.ingredient_name
FROM ingredients i
JOIN pizza_type_ingredients pti ON i.ingredient_id = pti.ingredient_id
JOIN pizza_types pt ON pti.pizza_type_id = pt.pizza_type_id
JOIN categories c ON pt.category_id = c.category_id
WHERE c.category_name = 'Meat';