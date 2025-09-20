// Cargar datos desde sessionStorage
document.addEventListener('DOMContentLoaded', function() {
    const financialData = JSON.parse(sessionStorage.getItem('financialData'));
    
    if (!financialData) {
        // Redirigir al formulario si no hay datos
        window.location.href = 'index.html';
        return;
    }
    
    // Mostrar datos en el dashboard
    displayFinancialData(financialData);
    
    // Configurar botón de volver
    document.getElementById('backButton').addEventListener('click', function() {
        window.location.href = 'index.html';
    });
    
    // Configurar botones de acción
    document.getElementById('downloadPdf').addEventListener('click', function() {
        alert('Funcionalidad de descarga de PDF en desarrollo.');
    });
    
    document.getElementById('savePlan').addEventListener('click', function() {
        alert('Funcionalidad de guardado en desarrollo.');
    });
});

function displayFinancialData(data) {
    // Calcular métricas financieras
    const totalRevenue = data.expectedSales;
    const totalVariableCosts = data.variableCosts * (data.expectedSales / data.variableCosts); // Simplificación
    const operatingExpenses = data.fixedExpenses + totalVariableCosts;
    const netProfit = totalRevenue - operatingExpenses;
    
    // Mostrar valores en el dashboard
    document.getElementById('totalRevenue').textContent = `$${totalRevenue.toLocaleString()}`;
    document.getElementById('operatingExpenses').textContent = `$${operatingExpenses.toLocaleString()}`;
    document.getElementById('netProfit').textContent = `$${netProfit.toLocaleString()}`;
    
    // Generar recomendaciones
    generateRecommendations(data, netProfit);
    
    // Crear gráficos
    createCharts(data, totalRevenue, operatingExpenses, netProfit);
}

function generateRecommendations(data, netProfit) {
    const recommendations = [
        "Optimizar el gasto en marketing para maximizar ROI",
        "Explorar nuevos mercados para diversificar ingresos",
        "Reducir costos operativos mediante procesos más eficientes",
        "Considerar aumentar precios si el mercado lo permite",
        "Implementar sistema de inventario just-in-time para reducir costos"
    ];
    
    const recommendationsList = document.getElementById('aiRecommendations');
    recommendationsList.innerHTML = '';
    
    recommendations.forEach(rec => {
        const li = document.createElement('div');
        li.className = 'recommendation-item';
        li.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
        recommendationsList.appendChild(li);
    });
}

function createCharts(data, totalRevenue, operatingExpenses, netProfit) {
    // Crear gráfico de pérdidas y ganancias
    FinancialCharts.createProfitLossChart(totalRevenue, operatingExpenses, netProfit);
    
    // Crear gráfico de punto de equilibrio
    FinancialCharts.createBreakEvenChart(data.fixedExpenses, data.variableCosts, data.expectedSales);
    
    // Crear gráfico de flujo de caja
    FinancialCharts.createCashFlowChart(data.initialCapital, totalRevenue, operatingExpenses);
}