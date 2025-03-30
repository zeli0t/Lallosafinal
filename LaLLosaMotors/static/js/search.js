// Funcionalidad de búsqueda
document.addEventListener('DOMContentLoaded', function() {
    const buscador = document.getElementById('buscador');
    const resultadosBusqueda = document.getElementById('resultados-busqueda');
    const listaServicios = document.getElementById('lista-servicios');
    const listaPresupuestos = document.getElementById('lista-presupuestos');
    
    if (!buscador) return; // Si no estamos en una página con buscador, salimos
    
    // Evitar que la tecla Enter recargue la página
    buscador.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
    
    // Manejar la búsqueda al escribir
    let timeoutId;
    buscador.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const termino = buscador.value.trim();
        
        if (termino.length < 2) {
            resultadosBusqueda.classList.add('d-none');
            return;
        }
        
        // Esperar un poco antes de buscar para evitar muchas peticiones
        timeoutId = setTimeout(function() {
            buscar(termino);
        }, 300);
    });
    
    // Función para realizar la búsqueda
    function buscar(termino) {
        fetch(`/buscar?q=${encodeURIComponent(termino)}`)
            .then(response => response.json())
            .then(data => {
                mostrarResultados(data);
            })
            .catch(error => {
                console.error('Error en la búsqueda:', error);
            });
    }
    
    // Función para mostrar los resultados
    function mostrarResultados(data) {
        listaServicios.innerHTML = '';
        listaPresupuestos.innerHTML = '';
        
        // Mostrar servicios
        if (data.servicios && data.servicios.length > 0) {
            data.servicios.forEach(servicio => {
                const item = document.createElement('li');
                item.className = 'list-group-item bg-dark text-white border-secondary';
                item.innerHTML = `
                    <a href="${servicio.url}" class="text-white text-decoration-none">
                        <strong>${servicio.nombre}</strong> - ${formatCurrency(servicio.precio)}
                    </a>
                    <p class="text-muted small mb-0">${servicio.descripcion || ''}</p>
                `;
                listaServicios.appendChild(item);
            });
            document.getElementById('resultados-servicios').classList.remove('d-none');
        } else {
            document.getElementById('resultados-servicios').classList.add('d-none');
        }
        
        // Mostrar presupuestos
        if (data.presupuestos && data.presupuestos.length > 0) {
            data.presupuestos.forEach(presupuesto => {
                const item = document.createElement('li');
                item.className = 'list-group-item bg-dark text-white border-secondary';
                item.innerHTML = `
                    <a href="${presupuesto.url}" class="text-white text-decoration-none">
                        <strong>${presupuesto.cliente}</strong> - ${presupuesto.vehiculo}
                    </a>
                    <p class="text-muted small mb-0">Fecha: ${presupuesto.fecha}</p>
                `;
                listaPresupuestos.appendChild(item);
            });
            document.getElementById('resultados-presupuestos').classList.remove('d-none');
        } else {
            document.getElementById('resultados-presupuestos').classList.add('d-none');
        }
        
        // Mostrar u ocultar el panel de resultados
        if ((data.servicios && data.servicios.length > 0) || (data.presupuestos && data.presupuestos.length > 0)) {
            resultadosBusqueda.classList.remove('d-none');
        } else {
            resultadosBusqueda.classList.add('d-none');
        }
    }
    
    // Función para formatear moneda
    function formatCurrency(value) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(value);
    }
    
    // Cerrar resultados al hacer clic fuera
    document.addEventListener('click', function(event) {
        if (!resultadosBusqueda.contains(event.target) && event.target !== buscador) {
            resultadosBusqueda.classList.add('d-none');
        }
    });
});