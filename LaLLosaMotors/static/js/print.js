document.addEventListener('DOMContentLoaded', function() {
    // Imprimir automáticamente al cargar la página
    window.setTimeout(function() {
        window.print();
    }, 500);
    
    // Botón para volver a la página anterior
    document.getElementById('btnVolver').addEventListener('click', function() {
        window.close();
    });
});
