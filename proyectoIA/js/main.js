// Selección de tipo de negocio
document.querySelectorAll('.business-type-card').forEach(card => {
    card.addEventListener('click', function() {
        // Remover selección anterior
        document.querySelectorAll('.business-type-card').forEach(c => {
            c.classList.remove('selected');
        });
        
        // Agregar selección actual
        this.classList.add('selected');
        
        // Establecer el valor en el campo oculto
        document.getElementById('businessType').value = this.dataset.type;
    });
});

// Validación del formulario
document.getElementById('businessForm').addEventListener('submit', function(e) {
    const businessType = document.getElementById('businessType').value;
    const initialCapital = document.getElementById('initialCapital').value;
    const fixedExpenses = document.getElementById('fixedExpenses').value;
    const expectedSales = document.getElementById('expectedSales').value;
    const variableCosts = document.getElementById('variableCosts').value;
    
    // Validaciones
    if (!businessType) {
        e.preventDefault();
        alert('Por favor selecciona un tipo de negocio');
        return;
    }
    
    if (!initialCapital || !fixedExpenses || !expectedSales || !variableCosts) {
        e.preventDefault();
        alert('Por favor completa todos los campos financieros');
        return;
    }
    
    // Guardar datos en sessionStorage para pasarlos al dashboard
    const formData = {
        businessType,
        initialCapital: parseFloat(initialCapital),
        fixedExpenses: parseFloat(fixedExpenses),
        expectedSales: parseFloat(expectedSales),
        variableCosts: parseFloat(variableCosts)
    };
    
    sessionStorage.setItem('financialData', JSON.stringify(formData));
});

// Efectos de animación para elementos al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const formInputs = document.querySelectorAll('input, select');
    
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});