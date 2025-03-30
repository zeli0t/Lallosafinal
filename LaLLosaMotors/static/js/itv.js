// Funcionalidad para Recordatorios ITV
document.addEventListener('DOMContentLoaded', function() {
    // Configurar el botón de eliminar recordatorio
    const botonesEliminar = document.querySelectorAll('.eliminar-recordatorio');
    
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            if (confirm('¿Está seguro de eliminar este recordatorio?')) {
                eliminarRecordatorio(id);
            }
        });
    });
    
    // Función para eliminar un recordatorio
    function eliminarRecordatorio(id) {
        fetch(`/recordatorios/itv/eliminar/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error al eliminar recordatorio:', error);
            alert('Error al eliminar el recordatorio. Inténtelo de nuevo.');
        });
    }
    
    // Establecer la fecha actual en el campo de fecha
    const fechaITV = document.getElementById('fecha_itv');
    if (fechaITV) {
        const ahora = new Date();
        const formato = ahora.toISOString().split('T')[0];
        fechaITV.value = formato;
    }
});