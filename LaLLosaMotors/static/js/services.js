document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const btnNuevoServicio = document.getElementById('btnNuevoServicio');
    const modalServicio = new bootstrap.Modal(document.getElementById('modalServicio'));
    const formServicio = document.getElementById('formServicio');
    const servicioIdInput = document.getElementById('servicioId');
    const servicioNombreInput = document.getElementById('servicioNombre');
    const servicioDescripcionInput = document.getElementById('servicioDescripcion');
    const servicioPrecioInput = document.getElementById('servicioPrecio');
    
    // Evento para mostrar modal de nuevo servicio
    if (btnNuevoServicio) {
        btnNuevoServicio.addEventListener('click', function() {
            // Resetear el formulario
            formServicio.reset();
            servicioIdInput.value = '';
            
            // Cambiar título y acción del formulario
            document.getElementById('modalServicioLabel').textContent = 'Nuevo Servicio';
            formServicio.action = '/servicios/nuevo';
            
            // Mostrar modal
            modalServicio.show();
        });
    }
    
    // Función para editar servicio
    window.editarServicio = function(id, nombre, descripcion, precio) {
        // Llenar el formulario con los datos del servicio
        servicioIdInput.value = id;
        servicioNombreInput.value = nombre;
        servicioDescripcionInput.value = descripcion || '';
        servicioPrecioInput.value = precio;
        
        // Cambiar título y acción del formulario
        document.getElementById('modalServicioLabel').textContent = 'Editar Servicio';
        formServicio.action = `/servicios/editar/${id}`;
        
        // Mostrar modal
        modalServicio.show();
    };
    
    // Validación del formulario antes de enviar
    if (formServicio) {
        formServicio.addEventListener('submit', function(event) {
            if (!servicioNombreInput.value.trim()) {
                alert('El nombre del servicio es obligatorio');
                event.preventDefault();
                return;
            }
            
            if (!servicioPrecioInput.value.trim() || isNaN(servicioPrecioInput.value)) {
                alert('El precio debe ser un número válido');
                event.preventDefault();
                return;
            }
        });
    }
    
    // Confirmación para eliminar servicio
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    botonesEliminar.forEach(function(boton) {
        boton.addEventListener('click', function(event) {
            if (!confirm('¿Está seguro de que desea eliminar este servicio?')) {
                event.preventDefault();
            }
        });
    });
});
