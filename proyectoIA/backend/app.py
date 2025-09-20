from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de la base de datos SQL Server
server = 'localhost' 
database = 'baseIA' 
username = 'sa' 
password = 'your_password' 

def get_db_connection():
    conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return conn

@app.route('/api/business-types', methods=['GET'])
def get_business_types():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM BusinessTypes")
        rows = cursor.fetchall()
        
        business_types = []
        for row in rows:
            business_types.append({
                'id': row[0],
                'name': row[1],
                'description': row[2]
            })
        
        conn.close()
        return jsonify(business_types)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_finances():
    try:
        data = request.json
        user_id = data.get('user_id', 1)  # Por defecto user_id = 1 para usuarios no autenticados
        business_type = data.get('business_type')
        initial_capital = float(data.get('initial_capital'))
        fixed_expenses = float(data.get('fixed_expenses'))
        expected_sales = float(data.get('expected_sales'))
        variable_costs = float(data.get('variable_costs', 0))
        
        # Obtener el ID del tipo de negocio
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM BusinessTypes WHERE name LIKE ?", (f"%{business_type}%",))
        business_type_row = cursor.fetchone()
        
        if not business_type_row:
            return jsonify({'error': 'Tipo de negocio no encontrado'}), 400
            
        business_type_id = business_type_row[0]
        
        # Guardar en base de datos
        cursor.execute("""
            INSERT INTO BusinessPlans (user_id, business_type_id, initial_capital, fixed_expenses, expected_sales, variable_costs)
            VALUES (?, ?, ?, ?, ?, ?)
        """, user_id, business_type_id, initial_capital, fixed_expenses, expected_sales, variable_costs)
        
        conn.commit()
        
        # Obtener el ID del plan recién insertado
        plan_id = cursor.execute("SELECT @@IDENTITY AS id").fetchone().id
        
        # Análisis financiero con IA (simulado)
        analysis_result = perform_financial_analysis(initial_capital, fixed_expenses, expected_sales, variable_costs, business_type)
        
        # Guardar análisis en base de datos
        cursor.execute("""
            INSERT INTO FinancialAnalyses 
            (plan_id, budget_analysis, cash_flow_analysis, break_even_analysis, 
             debt_capacity_analysis, risk_level, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, 
        plan_id, 
        json.dumps({"initial_capital": initial_capital}),
        json.dumps({"expected_sales": expected_sales, "fixed_expenses": fixed_expenses, "variable_costs": variable_costs}),
        json.dumps({"break_even_point": analysis_result["break_even_point"]}),
        json.dumps({"debt_capacity": analysis_result["debt_capacity"]}),
        analysis_result["risk_level"],
        json.dumps(analysis_result["recommendations"])
        )
        
        conn.commit()
        conn.close()
        
        # Agregar el plan_id al resultado
        analysis_result['plan_id'] = plan_id
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def perform_financial_analysis(initial_capital, fixed_expenses, expected_sales, variable_costs, business_type):
    """Realiza análisis financiero con IA simulada"""
    
    # Cálculo del punto de equilibrio
    if expected_sales > 0 and variable_costs > 0:
        contribution_margin = (expected_sales - variable_costs) / expected_sales
        if contribution_margin > 0:
            break_even_point = fixed_expenses / contribution_margin
        else:
            break_even_point = 0
    else:
        break_even_point = 0
    
    # Capacidad de endeudamiento (hasta 30% del capital inicial)
    debt_capacity = initial_capital * 0.3
    
    # Margen esperado
    if expected_sales > 0:
        expected_margin = ((expected_sales - fixed_expenses - variable_costs) / expected_sales) * 100
    else:
        expected_margin = 0
    
    # Determinar nivel de riesgo
    if initial_capital >= 10000:
        risk_level = 'low'
    elif initial_capital >= 5000:
        risk_level = 'medium'
    else:
        risk_level = 'high'
    
    # Ajustar según el tipo de negocio
    business_risk_factors = {
        'cafeteria': 'medium',
        'tienda_online': 'medium',
        'minimarket': 'low', 
        'consultoria': 'low'
    }
    
    business_risk = business_risk_factors.get(business_type, 'medium')
    if business_risk == 'high' and risk_level != 'high':
        risk_level = 'medium'
    if business_risk == 'low' and risk_level == 'high':
        risk_level = 'medium'
    
    # Generar recomendaciones
    recommendations = generate_recommendations(risk_level, initial_capital, fixed_expenses, 
                                              expected_sales, break_even_point, business_type)
    
    # Calcular métricas para el dashboard
    total_revenue = expected_sales
    operating_expenses = fixed_expenses + variable_costs
    net_profit = total_revenue - operating_expenses
    
    return {
        "risk_level": risk_level,
        "break_even_point": break_even_point,
        "debt_capacity": debt_capacity,
        "expected_margin": expected_margin,
        "total_revenue": total_revenue,
        "operating_expenses": operating_expenses,
        "net_profit": net_profit,
        "recommendations": recommendations
    }

def generate_recommendations(risk_level, capital, expenses, sales, break_even, business_type):
    """Genera recomendaciones personalizadas basadas en el análisis"""
    recommendations = []
    
    if risk_level == 'high':
        recommendations.append("Considera comenzar con un capital mayor o reducir gastos fijos iniciales.")
        recommendations.append("Evita endeudamiento hasta estabilizar tus flujos de caja.")
        recommendations.append("Enfócate en alcanzar tu punto de equilibrio lo antes posible.")
    elif risk_level == 'medium':
        recommendations.append("Podrías considerar un crédito pequeño para impulsar el crecimiento.")
        recommendations.append("Mantén un control estricto de tus gastos durante los primeros meses.")
        recommendations.append("Diversifica tus fuentes de ingresos para reducir el riesgo.")
    else:
        recommendations.append("Tienes buena capacidad de inversión. Considera expandir tu negocio.")
        recommendations.append("Puedes acceder a líneas de crédito preferenciales.")
        recommendations.append("Invierte en marketing para acelerar el crecimiento de tu negocio.")
    
    if capital < expenses * 3:
        recommendations.append("Tu capital inicial es bajo para cubrir tus gastos iniciales. Considera reducir gastos fijos.")
    
    if sales < break_even * 1.2:
        recommendations.append("Tus ventas proyectadas están muy cerca del punto de equilibrio. Considera estrategias para aumentar ventas.")
    
    # Recomendaciones específicas por tipo de negocio
    if business_type == 'cafeteria' or business_type == 'restaurante':
        recommendations.append("Controla cuidadosamente el costo de ingredientes y manejo de inventario.")
        recommendations.append("Considera implementar un programa de fidelización para clientes recurrentes.")
    
    if business_type == 'tienda_online':
        recommendations.append("Invierte en SEO y marketing digital para aumentar tu visibilidad online.")
        recommendations.append("Optimiza los costos de envío y logística para mejorar márgenes.")
    
    if business_type == 'minimarket':
        recommendations.append("Gestiona cuidadosamente el inventario para evitar productos obsoletos.")
        recommendations.append("Considera ampliar horarios de atención para aumentar ventas.")
    
    if business_type == 'consultoria':
        recommendations.append("Diversifica tu cartera de clientes para reducir dependencia de pocos clientes.")
        recommendations.append("Invierte en desarrollo profesional para mantener tus habilidades competitivas.")
    
    return recommendations

@app.route('/api/reports/<int:plan_id>', methods=['GET'])
def generate_report(plan_id):
    try:
        # Obtener datos del plan
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT bp.initial_capital, bp.fixed_expenses, bp.expected_sales, bp.variable_costs,
                   bt.name as business_type, fa.risk_level, fa.recommendations
            FROM BusinessPlans bp
            JOIN BusinessTypes bt ON bp.business_type_id = bt.id
            JOIN FinancialAnalyses fa ON bp.id = fa.plan_id
            WHERE bp.id = ?
        """, plan_id)
        
        plan_data = cursor.fetchone()
        conn.close()
        
        if not plan_data:
            return jsonify({'error': 'Plan no encontrado'}), 404
            
        # Aquí iría la generación real del reporte PDF
        # Por ahora devolvemos los datos para generar el PDF en el frontend
        return jsonify({
            'message': 'Datos para generar reporte',
            'data': {
                'initial_capital': plan_data[0],
                'fixed_expenses': plan_data[1],
                'expected_sales': plan_data[2],
                'variable_costs': plan_data[3],
                'business_type': plan_data[4],
                'risk_level': plan_data[5],
                'recommendations': json.loads(plan_data[6]) if plan_data[6] else []
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans', methods=['POST'])
def save_plan():
    try:
        data = request.json
        plan_id = data.get('plan_id')
        plan_name = data.get('plan_name', 'Mi Plan de Negocio')
        
        # En una implementación real, guardaríamos esto en la base de datos
        # vinculado al usuario autenticado
        
        return jsonify({
            'message': 'Plan guardado exitosamente',
            'plan_id': plan_id,
            'plan_name': plan_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)