-- Script para crear la base de datos y tablas
CREATE DATABASE baseIA;
GO

USE baseIA;
GO

CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY(1,1),
    email NVARCHAR(255) UNIQUE,
    password_hash NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE BusinessTypes (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    description NVARCHAR(500)
);

CREATE TABLE BusinessPlans (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT FOREIGN KEY REFERENCES Users(id),
    business_type_id INT FOREIGN KEY REFERENCES BusinessTypes(id),
    initial_capital DECIMAL(15, 2),
    fixed_expenses DECIMAL(15, 2),
    expected_sales DECIMAL(15, 2),
    variable_costs DECIMAL(15, 2),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE FinancialAnalyses (
    id INT PRIMARY KEY IDENTITY(1,1),
    plan_id INT FOREIGN KEY REFERENCES BusinessPlans(id),
    budget_analysis NVARCHAR(MAX),
    cash_flow_analysis NVARCHAR(MAX),
    break_even_analysis NVARCHAR(MAX),
    debt_capacity_analysis NVARCHAR(MAX),
    risk_level NVARCHAR(50),
    recommendations NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

-- Insertar datos de ejemplo
INSERT INTO BusinessTypes (name, description) VALUES
('Cafetería', 'Negocio de venta de café y alimentos ligeros'),
('Minimarket', 'Tienda pequeña con productos de primera necesidad'),
('Tienda Online', 'Comercio electrónico de diversos productos'),
('Restaurante', 'Establecimiento de comida con servicio completo'),
('Consultoría', 'Servicios profesionales de asesoramiento');

-- Crear índices para mejorar el rendimiento
CREATE INDEX IX_BusinessPlans_UserID ON BusinessPlans(user_id);
CREATE INDEX IX_FinancialAnalyses_PlanID ON FinancialAnalyses(plan_id);
CREATE INDEX IX_BusinessPlans_CreatedAt ON BusinessPlans(created_at);