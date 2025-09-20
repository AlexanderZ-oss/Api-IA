// Funciones para crear gráficos
class FinancialCharts {
    static createProfitLossChart(revenue, expenses, profit) {
        const ctx = document.getElementById('profitLossChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Ingresos', 'Gastos', 'Beneficio'],
                datasets: [{
                    data: [revenue, expenses, profit],
                    backgroundColor: [
                        'rgba(76, 201, 240, 0.8)',
                        'rgba(247, 37, 133, 0.8)',
                        'rgba(57, 204, 155, 0.8)'
                    ],
                    borderColor: [
                        'rgba(76, 201, 240, 1)',
                        'rgba(247, 37, 133, 1)',
                        'rgba(57, 204, 155, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: $${context.raw.toLocaleString()}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    static createBreakEvenChart(fixedCosts, variableCosts, expectedSales) {
        const ctx = document.getElementById('breakEvenChart').getContext('2d');
        
        // Cálculo simplificado del punto de equilibrio
        const breakEvenPoint = fixedCosts / (1 - (variableCosts / expectedSales));
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'Ingresos',
                        data: [0, expectedSales * 0.4, expectedSales * 0.7, expectedSales, expectedSales * 1.2, expectedSales * 1.5],
                        borderColor: 'rgba(76, 201, 240, 1)',
                        backgroundColor: 'rgba(76, 201, 240, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Costos Totales',
                        data: [fixedCosts, fixedCosts + (variableCosts * 0.4), fixedCosts + (variableCosts * 0.7), fixedCosts + variableCosts, fixedCosts + (variableCosts * 1.2), fixedCosts + (variableCosts * 1.5)],
                        borderColor: 'rgba(247, 37, 133, 1)',
                        backgroundColor: 'rgba(247, 37, 133, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Punto de Equilibrio',
                        data: [breakEvenPoint, breakEvenPoint, breakEvenPoint, breakEvenPoint, breakEvenPoint, breakEvenPoint],
                        borderColor: 'rgba(57, 204, 155, 1)',
                        borderDash: [5, 5],
                        fill: false,
                        pointStyle: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Monto ($)'
                        }
                    }
                }
            }
        });
    }
    
    static createCashFlowChart(initialCapital, revenue, expenses) {
        const ctx = document.getElementById('cashFlowChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'Ingresos',
                        data: [revenue * 0.6, revenue * 0.8, revenue, revenue * 1.1, revenue * 1.3, revenue * 1.5],
                        backgroundColor: 'rgba(76, 201, 240, 0.7)',
                    },
                    {
                        label: 'Egresos',
                        data: [expenses * 0.7, expenses * 0.9, expenses, expenses * 1.1, expenses * 1.2, expenses * 1.3],
                        backgroundColor: 'rgba(247, 37, 133, 0.7)',
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Monto ($)'
                        }
                    }
                }
            }
        });
    }
}