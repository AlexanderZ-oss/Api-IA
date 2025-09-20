import pyodbc

def init_database():
    server = 'localhost' 
    database = 'master' 
    username = 'sa' 
    password = 'your_password'
    
    try:
        # Conectar al servidor SQL
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        cursor = conn.cursor()
        
        # Crear la base de datos si no existe
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'baseIA')
            CREATE DATABASE baseIA
        """)
        
        # Usar la base de datos
        cursor.execute("USE baseIA")
        
        # Crear tablas
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
            CREATE TABLE Users (
                id INT PRIMARY KEY IDENTITY(1,1),
                email NVARCHAR(255) UNIQUE,
                password_hash NVARCHAR(255),
                created_at DATETIME DEFAULT GETDATE()
            )
        """)
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BusinessTypes' AND xtype='U')
            CREATE TABLE BusinessTypes (
                id INT PRIMARY KEY IDENTITY(1,1),
                name NVARCHAR(100),
                description NVARCHAR(500)
            )
        """)
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BusinessPlans' AND xtype='U')
            CREATE TABLE BusinessPlans (
                id INT PRIMARY KEY IDENTITY(1,1),
                user_id INT FOREIGN KEY REFERENCES Users(id),
                business_type_id INT FOREIGN KEY REFERENCES BusinessTypes(id),
                initial_capital DECIMAL(15, 2),
                fixed_expenses DECIMAL(15, 2),
                expected_sales DECIMAL(15, 2),
                variable_costs DECIMAL(15, 2),
                created_at DATETIME DEFAULT GETDATE()
            )
        """)
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='FinancialAnalyses' AND xtype='U')
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
            )
        """)
        
        # Insertar datos de ejemplo para tipos de negocio
        cursor.execute("SELECT COUNT(*) FROM BusinessTypes")
        if cursor.fetchone()[0] == 0:
            business_types = [
                ('Cafetería', 'Negocio de venta de café y alimentos ligeros'),
                ('Minimarket', 'Tienda pequeña con productos de primera necesidad'),
                ('Tienda Online', 'Comercio electrónico de diversos productos'),
                ('Restaurante', 'Establecimiento de comida con servicio completo'),
                ('Consultoría', 'Servicios profesionales de asesoramiento')
            ]
            
            for name, description in business_types:
                cursor.execute(
                    "INSERT INTO BusinessTypes (name, description) VALUES (?, ?)",
                    name, description
                )
        
        conn.commit()
        conn.close()
        
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

if __name__ == '__main__':
    init_database()