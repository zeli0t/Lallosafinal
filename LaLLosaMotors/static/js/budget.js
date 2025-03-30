document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const btnNuevoPresupuesto = document.getElementById('btnNuevoPresupuesto');
    const modalElement = document.getElementById('modalPresupuesto');
    const modalPresupuesto = new bootstrap.Modal(modalElement);
    const formPresupuesto = document.getElementById('formPresupuesto');
    
    // Evento para cuando se cierra el modal (para resetear el modo de edición)
    modalElement.addEventListener('hidden.bs.modal', function () {
        presupuestoIdEnEdicion = null;
        const modalTitle = document.querySelector('#modalPresupuesto .modal-title');
        if (modalTitle) {
            modalTitle.textContent = 'Nuevo Presupuesto';
        }
    });
    const tablaItems = document.getElementById('tablaItems');
    const tbodyItems = document.getElementById('tbodyItems');
    const btnAgregarItem = document.getElementById('btnAgregarItem');
    const selectServicio = document.getElementById('selectServicio');
    const inputCantidad = document.getElementById('inputCantidad');
    const clienteInput = document.getElementById('cliente');
    const vehiculoInput = document.getElementById('vehiculo');
    const observacionesInput = document.getElementById('observaciones');
    const totalSinIvaSpan = document.getElementById('totalSinIva');
    const ivaSpan = document.getElementById('iva');
    const totalConIvaSpan = document.getElementById('totalConIva');
    const presupuestosContainer = document.getElementById('presupuestosContainer');

    // Variables globales
    let servicios = [];
    let itemsPresupuesto = [];
    
    // Cargar servicios desde la API
    cargarServicios();
    // Cargar presupuestos existentes
    cargarPresupuestos();
    
    // Función para cargar servicios desde la API
    function cargarServicios() {
        fetch('/api/servicios')
            .then(response => response.json())
            .then(data => {
                servicios = data;
                // Llenar el select de servicios
                if (selectServicio) {
                    selectServicio.innerHTML = '<option value="">Seleccione un servicio</option>';
                    servicios.forEach(servicio => {
                        const option = document.createElement('option');
                        option.value = servicio.id;
                        option.textContent = `${servicio.nombre} - ${formatCurrency(servicio.precio)}`;
                        option.dataset.precio = servicio.precio;
                        selectServicio.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error al cargar servicios:', error));
    }
    
    // Función para cargar presupuestos existentes
    function cargarPresupuestos() {
        if (!presupuestosContainer) return;
        
        fetch('/api/presupuestos')
            .then(response => response.json())
            .then(data => {
                presupuestosContainer.innerHTML = '';
                
                if (data.length === 0) {
                    presupuestosContainer.innerHTML = '<div class="alert alert-info">No hay presupuestos registrados</div>';
                    return;
                }
                
                data.forEach(presupuesto => {
                    const card = document.createElement('div');
                    card.className = 'card mb-4';
                    
                    let itemsHtml = '';
                    presupuesto.items.forEach(item => {
                        itemsHtml += `
                            <tr>
                                <td class="descripcion-servicio">${item.servicio}</td>
                                <td class="text-center" style="color: white !important;">${item.cantidad}</td>
                                <td class="text-end" style="color: white !important;">${formatCurrency(item.precio_unitario)}</td>
                                <td class="text-end" style="color: white !important;">${formatCurrency(item.subtotal)}</td>
                            </tr>
                        `;
                    });
                    
                    card.innerHTML = `
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">Presupuesto #${presupuesto.id} - ${presupuesto.fecha}</h5>
                            <div>
                                <a href="/presupuestos/imprimir/${presupuesto.id}" target="_blank" class="btn btn-sm btn-outline-primary me-2">
                                    <i class="bi bi-printer"></i> Imprimir
                                </a>
                                <button class="btn btn-sm btn-outline-warning me-2 editar-presupuesto" data-id="${presupuesto.id}">
                                    <i class="bi bi-pencil"></i> Editar
                                </button>
                                <button class="btn btn-sm btn-outline-danger eliminar-presupuesto" data-id="${presupuesto.id}">
                                    <i class="bi bi-trash"></i> Eliminar
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <p><strong>Cliente:</strong> ${presupuesto.cliente}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Vehículo:</strong> ${presupuesto.vehiculo}</p>
                                </div>
                            </div>
                            ${presupuesto.observaciones ? `<p><strong>Observaciones:</strong> ${presupuesto.observaciones}</p>` : ''}
                            <h6>Servicios</h6>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Servicio</th>
                                            <th class="text-center">Cantidad</th>
                                            <th class="text-end">Precio</th>
                                            <th class="text-end">Subtotal</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-white">
                                        ${itemsHtml}
                                    </tbody>
                                    <tfoot class="text-white">
                                        <tr>
                                            <th colspan="3" class="text-end" style="color: white !important;">Total sin IVA:</th>
                                            <th class="text-end" style="color: white !important;">${formatCurrency(presupuesto.total_sin_iva)}</th>
                                        </tr>
                                        <tr>
                                            <th colspan="3" class="text-end" style="color: white !important;">IVA (21%):</th>
                                            <th class="text-end" style="color: white !important;">${formatCurrency(presupuesto.iva)}</th>
                                        </tr>
                                        <tr>
                                            <th colspan="3" class="text-end" style="color: white !important;">Total con IVA:</th>
                                            <th class="text-end" style="color: white !important;">${formatCurrency(presupuesto.total_con_iva)}</th>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                    `;
                    
                    presupuestosContainer.appendChild(card);
                });
            })
            .catch(error => console.error('Error al cargar presupuestos:', error));
    }
    
    // Evento para abrir modal de nuevo presupuesto
    if (btnNuevoPresupuesto) {
        btnNuevoPresupuesto.addEventListener('click', function() {
            // Resetear el formulario y los items
            if (formPresupuesto) formPresupuesto.reset();
            itemsPresupuesto = [];
            presupuestoIdEnEdicion = null; // Resetear el ID de edición
            actualizarTablaItems();
            calcularTotales();
            
            // Resetear el título del modal a "Nuevo Presupuesto"
            const modalTitle = document.querySelector('#modalPresupuesto .modal-title');
            if (modalTitle) {
                modalTitle.textContent = 'Nuevo Presupuesto';
            }
            
            // Mostrar modal
            modalPresupuesto.show();
        });
    }
    
    // Agregar item al presupuesto
    if (btnAgregarItem) {
        btnAgregarItem.addEventListener('click', function() {
            if (!selectServicio.value) {
                alert('Debe seleccionar un servicio');
                return;
            }
            
            const cantidad = parseInt(inputCantidad.value) || 1;
            if (cantidad <= 0) {
                alert('La cantidad debe ser mayor a 0');
                return;
            }
            
            const servicioId = parseInt(selectServicio.value);
            const servicio = servicios.find(s => s.id === servicioId);
            
            if (!servicio) {
                alert('Servicio no encontrado');
                return;
            }
            
            // Verificar si el servicio ya está en la lista
            const itemExistente = itemsPresupuesto.find(item => item.servicio_id === servicioId);
            
            if (itemExistente) {
                // Sumar la cantidad al item existente
                itemExistente.cantidad += cantidad;
            } else {
                // Agregar nuevo item
                itemsPresupuesto.push({
                    servicio_id: servicioId,
                    nombre_servicio: servicio.nombre,
                    precio_unitario: servicio.precio,
                    cantidad: cantidad
                });
            }
            
            // Actualizar tabla de items
            actualizarTablaItems();
            calcularTotales();
            
            // Resetear selector y cantidad
            selectServicio.value = '';
            inputCantidad.value = '1';
        });
    }
    
    // Actualizar la tabla de items
    function actualizarTablaItems() {
        if (!tbodyItems) return;
        
        tbodyItems.innerHTML = '';
        
        if (itemsPresupuesto.length === 0) {
            tbodyItems.innerHTML = '<tr><td colspan="5" class="text-center" style="color: white !important;">No hay items en el presupuesto</td></tr>';
            return;
        }
        
        itemsPresupuesto.forEach((item, index) => {
            const subtotal = item.precio_unitario * item.cantidad;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="descripcion-servicio">${item.nombre_servicio}</td>
                <td class="text-center" style="color: white !important;">${item.cantidad}</td>
                <td class="text-end" style="color: white !important;">${formatCurrency(item.precio_unitario)}</td>
                <td class="text-end" style="color: white !important;">${formatCurrency(subtotal)}</td>
                <td class="text-center">
                    <button type="button" class="btn btn-sm btn-danger" onclick="eliminarItem(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            
            tbodyItems.appendChild(tr);
        });
    }
    
    // Eliminar item del presupuesto
    window.eliminarItem = function(index) {
        itemsPresupuesto.splice(index, 1);
        actualizarTablaItems();
        calcularTotales();
    };
    
    // Calcular totales
    function calcularTotales() {
        if (!totalSinIvaSpan || !ivaSpan || !totalConIvaSpan) return;
        
        let totalSinIva = 0;
        
        itemsPresupuesto.forEach(item => {
            totalSinIva += item.precio_unitario * item.cantidad;
        });
        
        const iva = totalSinIva * 0.21; // 21% de IVA
        const totalConIva = totalSinIva + iva;
        
        totalSinIvaSpan.textContent = formatCurrency(totalSinIva);
        ivaSpan.textContent = formatCurrency(iva);
        totalConIvaSpan.textContent = formatCurrency(totalConIva);
    }
    
    // Función para cargar un presupuesto para editar
    function cargarPresupuestoParaEditar(id) {
        fetch(`/presupuestos/editar/${id}`)
            .then(response => response.json())
            .then(presupuesto => {
                // Guardar el ID del presupuesto en edición
                presupuestoIdEnEdicion = id;
                
                // Llenar el formulario con los datos del presupuesto
                clienteInput.value = presupuesto.cliente;
                vehiculoInput.value = presupuesto.vehiculo;
                observacionesInput.value = presupuesto.observaciones || '';
                
                // Cargar los items del presupuesto
                itemsPresupuesto = presupuesto.items.map(item => ({
                    servicio_id: item.servicio_id,
                    nombre_servicio: item.nombre_servicio,
                    precio_unitario: item.precio_unitario,
                    cantidad: item.cantidad
                }));
                
                // Actualizar la tabla de items y totales
                actualizarTablaItems();
                calcularTotales();
                
                // Cambiar el título del modal
                const modalTitle = document.querySelector('#modalPresupuesto .modal-title');
                if (modalTitle) {
                    modalTitle.textContent = `Editar Presupuesto #${id}`;
                }
                
                // Mostrar el modal
                modalPresupuesto.show();
            })
            .catch(error => {
                console.error('Error al cargar presupuesto para editar:', error);
                alert('Error al cargar el presupuesto. Inténtelo de nuevo.');
            });
    }
    
    // Guardar presupuesto (nuevo o editar)
    if (formPresupuesto) {
        formPresupuesto.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!clienteInput.value.trim()) {
                alert('El nombre del cliente es obligatorio');
                return;
            }
            
            if (!vehiculoInput.value.trim()) {
                alert('La descripción del vehículo es obligatoria');
                return;
            }
            
            if (itemsPresupuesto.length === 0) {
                alert('Debe agregar al menos un servicio al presupuesto');
                return;
            }
            
            // Preparar datos para enviar
            const data = {
                cliente: clienteInput.value.trim(),
                vehiculo: vehiculoInput.value.trim(),
                observaciones: observacionesInput.value.trim(),
                items: itemsPresupuesto.map(item => ({
                    servicio_id: item.servicio_id,
                    cantidad: item.cantidad,
                    precio_unitario: item.precio_unitario
                }))
            };
            
            // Determinar si es un nuevo presupuesto o una edición
            const url = presupuestoIdEnEdicion 
                ? `/presupuestos/editar/${presupuestoIdEnEdicion}` 
                : '/presupuestos/nuevo';
            
            // Enviar datos al servidor
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert(presupuestoIdEnEdicion ? 'Presupuesto actualizado correctamente' : 'Presupuesto guardado correctamente');
                    modalPresupuesto.hide();
                    
                    // Resetear el ID en edición
                    presupuestoIdEnEdicion = null;
                    
                    // Resetear el título del modal
                    const modalTitle = document.querySelector('#modalPresupuesto .modal-title');
                    if (modalTitle) {
                        modalTitle.textContent = 'Nuevo Presupuesto';
                    }
                    
                    cargarPresupuestos(); // Recargar lista de presupuestos
                } else {
                    alert('Error al guardar presupuesto: ' + result.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al guardar presupuesto');
            });
        });
    }
    
    // Formato de moneda
    function formatCurrency(value) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(value);
    }
    
    // Configurar eventos de eliminación y edición de presupuestos
    // Usamos delegación de eventos para capturar clics en botones que podrían no existir al cargar la página
    if (presupuestosContainer) {
        presupuestosContainer.addEventListener('click', function(event) {
            // Verificar si el clic fue en un botón de eliminar
            if (event.target.closest('.eliminar-presupuesto')) {
                const boton = event.target.closest('.eliminar-presupuesto');
                const id = boton.getAttribute('data-id');
                
                if (confirm('¿Está seguro de eliminar este presupuesto? Esta acción no se puede deshacer.')) {
                    eliminarPresupuesto(id);
                }
            }
            
            // Verificar si el clic fue en un botón de editar
            if (event.target.closest('.editar-presupuesto')) {
                const boton = event.target.closest('.editar-presupuesto');
                const id = boton.getAttribute('data-id');
                
                cargarPresupuestoParaEditar(id);
            }
        });
    }
    
    // Variable para almacenar el ID del presupuesto en edición
    let presupuestoIdEnEdicion = null;
    
    // Función para eliminar un presupuesto
    function eliminarPresupuesto(id) {
        fetch(`/presupuestos/eliminar/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Presupuesto eliminado correctamente');
                cargarPresupuestos(); // Recargar la lista de presupuestos
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error al eliminar presupuesto:', error);
            alert('Error al eliminar el presupuesto. Inténtelo de nuevo.');
        });
    }
});
