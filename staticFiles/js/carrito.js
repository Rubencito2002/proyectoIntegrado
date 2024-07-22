document.addEventListener('DOMContentLoaded', function(){
    let carrito;
    const carritoLocal = localStorage.getItem('carrito');

    if(carritoLocal){
        try{
            carrito = JSON.parse(carritoLocal);
        } catch (error){
            console.error('Error al analizar el carrito desde el almacenamiento local:', error);
            carrito = [];
        }
    } else {
        carrito = [];
    }

    let total = 0;

    actualizarCarrito();

    document.getElementById('iconCarrito').addEventListener('click', actualizarCarrito);

    function añadirCarrito(nombre, precio){
        const existente = carrito.find(item => item.nombre === nombre);

        if(existente){
            existente.cantidad++;
        } else {
            carrito.push({nombre, precio, cantidad: 1});
        }

        localStorage.setItem('carrito', JSON.stringify(carrito));
        
        actualizarCarrito();
        actualizarIconoCarrito();
    }

    function actualizarCantidad(index, nuevaCantidad) {
        carrito[index].cantidad = parseInt(nuevaCantidad);
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarrito();
        actualizarIconoCarrito();
    }

    function eliminarProducto(index){
        carrito.splice(index, 1);
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarrito();
        actualizarIconoCarrito();
        mostrarFeedbackDelete();
    }

    function actualizarCarrito() {
        const carritoList = document.getElementById('carrito-list');
        carritoList.innerHTML = ''; // Limpiar el contenido existente
    
        total = 0;
    
        // Crear una tabla
        const table = document.createElement('table');
        table.classList.add('table');
    
        // Crear encabezados de tabla
        const headerRow = document.createElement('tr');
        const headers = ['Producto', 'Precio', 'Cantidad', 'Subtotal', 'Acciones'];
        headers.forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.classList.add('modalCustom');
            headerCell.textContent = headerText;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);
    
        // Agregar filas de tabla para cada producto en el carrito
        carrito.forEach((item, index) => {
            const row = document.createElement('tr');
    
            // Celdas de la fila
            const nombreCell = document.createElement('td');
            nombreCell.textContent = item.nombre;
            row.appendChild(nombreCell);
    
            const precioCell = document.createElement('td');
            precioCell.textContent = item.precio.toFixed(2) + '€';
            row.appendChild(precioCell);
    
            const cantidadCell = document.createElement('td');
            const cantidadInput = document.createElement('input');
            cantidadInput.classList.add('form-control', 'cantidad-input');
            cantidadInput.type = 'number';
            cantidadInput.min = 1;
            cantidadInput.value = item.cantidad;
            cantidadInput.addEventListener('change', () => actualizarCantidad(index, cantidadInput.value));
            cantidadCell.appendChild(cantidadInput);
            row.appendChild(cantidadCell);
    
            const subtotalCell = document.createElement('td');
            const subtotal = item.precio * item.cantidad;
            subtotalCell.textContent = subtotal.toFixed(2) + '€';
            row.appendChild(subtotalCell);
    
            const eliminarCell = document.createElement('td');
            const botonEliminar = document.createElement('button');
            botonEliminar.textContent = 'Eliminar';
            botonEliminar.classList.add('btn', 'btn-danger', 'btn-sm');
            botonEliminar.addEventListener('click', () => eliminarProducto(index));
            eliminarCell.appendChild(botonEliminar);
            row.appendChild(eliminarCell);
    
            table.appendChild(row);
    
            // Calcular el total
            total += subtotal;
        });
    
        // Agregar la tabla al contenedor del carrito
        carritoList.appendChild(table);
    
        // Actualizar el total
        document.getElementById('total').textContent = total.toFixed(2) + '€';

        // Verificar si el carrito está vacío y ocultar el contador de productos si es así
        if (carrito.length === 0) {
            const contadorProductos = document.getElementById('contProducts');
            contadorProductos.style.display = 'none';
        }
    }

    const carritoModal = document.getElementById('carrito-modal');
    carritoModal.addEventListener('hidden.bs.modal', function () {
        actualizarIconoCarrito();
    });

    function actualizarIconoCarrito(){
        const carritoBtn = document.getElementById('iconCarrito');
        const contadorProductos = document.getElementById('contProducts');

        if (carrito.length > 0) {
            carritoBtn.classList.add('carritoProductos');
            contadorProductos.textContent = carrito.length;
            contadorProductos.style.display = 'block';
            carritoBtn.style.color = ''; // Restablece el color del icono del carrito a su valor por defecto
        } else {
            carritoBtn.classList.remove('carritoProductos');
            contadorProductos.style.display = 'none';
            carritoBtn.style.color = 'black'; // Aplica el color del fondo del contador al icono del carrito
        }
    }

    const añadirCarritoBoton = document.querySelectorAll('.addCart');
    añadirCarritoBoton.forEach(button => {
        button.addEventListener('click', function(){
            const nombre = this.getAttribute('data-name');
            const precio = parseFloat(this.getAttribute('data-price'));
            añadirCarrito(nombre, precio);
            mostrarFeedbackAdd();

            // carrito.forEach((item, index) => {
            //     console.log(`Producto ${index + 1}: ${item.nombre} - Precio: ${item.precio}`);
            // });
        });
    });

    function redireccionarAConfirmacion() {
        window.location.href = '/confirmarCompra/';
    }
    
    document.getElementById('btnComprar').addEventListener('click', redireccionarAConfirmacion);
    
    document.getElementById('btnConfirmarCompra').addEventListener('click', realizarCompra);

    function realizarCompra(){
        let carritoLocal = localStorage.getItem('carrito');

        if(carritoLocal){
            try{
                let carrito = JSON.parse(carritoLocal);
                const usuarioActual = "{{ request.user.username }}";
                const datosEnvio = obtenerDatosEnvio();
                const formaPago = obtenerFormaPago();

                fetch('/procesarCompra/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': obtenerCookie('csrftoken') // Si estás usando CSRF protection en Django
                    },
                    body: JSON.stringify({ carrito: carrito, usuario: usuarioActual, datosEnvio: datosEnvio, formaPago: formaPago})
                })
                .then(response => {
                    if (response.redirected) {
                        mostrarFeedbackLogin();
                    } else {
                        response.json()
                    }
                })
                .then(data => {
                    console.log(data);
                    if(data.success){
                        mostrarFeedbackConfirmacion();
                    } else {
                        console.error(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error al realizar la compra: ', error);
                })
            }
            catch (error) {
                console.error('Error al analizar el carrito desde el almacenamiento local:', error);
            }
        } else {
            console.error('No se encontró ningún carrito en el almacenamiento local.');
        }
    }

    // Funcion para obtner los datos de envio para la compra de los productos.
    function obtenerDatosEnvio(){
        const formData = new FormData(document.getElementById('formularioEnvio'));
        const datosEnvio = {};

        formData.forEach((value, key) => {
            datosEnvio[key] = value;
        });
        return datosEnvio;
    }

    // Funcion para obtener los datos de forma de pago para la compra de los productos.
    function obtenerFormaPago(){
        const formaPagoSeleccionado = document.querySelector('input[name="formaPago"]:checked');

        if(formaPagoSeleccionado){
            return formaPagoSeleccionado.value;
        } else {
            return null;
        }
    }


    // Función para obtener el valor de una cookie por su nombre
    function obtenerCookie(nombre) {
        var nombreCookie = nombre + "=";
        var cookies = document.cookie.split(';');
        for(var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.indexOf(nombreCookie) === 0) {
                return cookie.substring(nombreCookie.length, cookie.length);
            }
        }
        return null;
    }

    // Aquí integras el nuevo script para mostrar los datos del carrito en la página de confirmación de compra.
    function actualizarCarritoConfirmacion(){
        const carritoList = document.getElementById('listaCarrito');
        carritoList.innerHTML = '';

        let totalCompra = 0;

        carrito.forEach(item => {
            const subtotal = item.precio * item.cantidad;
            totalCompra += subtotal;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.nombre}</td>
                <td>${item.precio.toFixed(2)} €</td>
                <td>${item.cantidad}</td>
                <td>${subtotal.toFixed(2)} €</td>`;
            carritoList.appendChild(tr);
        });

        document.getElementById('totalCompra').textContent = total.toFixed(2) + '€';
    }
    
    // Mostrar formulario de datos de pago según la forma seleccionada.
    const formularioPago = document.getElementById('formularioPago');
    const tarjetaDiv = document.getElementById('tarjetaDiv');
    const paypalDiv = document.getElementById('paypalDiv');

    // Función para mostrar u ocultar los formularios según la opción seleccionada
    function mostrarFormularioSegunSeleccion() {
        const formaPagoSeleccionada = formularioPago.querySelector('input[name="formaPago"]:checked');

        // Mostrar u ocultar los formularios de tarjeta y PayPal según la opción seleccionada
        if (formaPagoSeleccionada && formaPagoSeleccionada.value === 'tarjeta') {
            tarjetaDiv.style.display = 'block';
            paypalDiv.style.display = 'none';
        } else if (formaPagoSeleccionada && formaPagoSeleccionada.value === 'paypal') {
            tarjetaDiv.style.display = 'none';
            paypalDiv.style.display = 'block';
        } else {
            tarjetaDiv.style.display = 'none';
            paypalDiv.style.display = 'none';
        }
    }

    // Llamar a la función inicialmente para establecer el estado inicial
    mostrarFormularioSegunSeleccion();

    // Escuchar el evento change en el campo de método de pago
    formularioPago.addEventListener('change', mostrarFormularioSegunSeleccion);

    // Después de confirmar la compra y regresar a la página principal
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('confirmarCompra')) {
        limpiarCarrito();
    }

    // Función para limpiar el carrito visualmente y en el almacenamiento local
    function limpiarCarrito() {
        // Limpiar el carrito en el DOM
        carritoList.innerHTML = '';

        // Limpiar el carrito en el almacenamiento local
        localStorage.removeItem('carrito');
    }

    // Mostrar el feedback cuando se agrega un producto al carrito
    function mostrarFeedbackAdd() {
        var feedback = document.getElementById("feedback-message-add");
        feedback.style.display = "block";
        setTimeout(function() {
            feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
        }, 3000); // Cambia este valor para ajustar la duración del feedback
    }

    function mostrarFeedbackDelete() {
        var feedback = document.getElementById("feedback-message-delete");
        feedback.style.display = "block";
        setTimeout(function() {
            feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
        }, 3000); // Cambia este valor para ajustar la duración del feedback
    }

    function mostrarFeedbackConfirmacion() {
        var feedback = document.getElementById("confirmation-message");
        feedback.style.display = "block";
        setTimeout(function() {
            feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
            window.location.href = '/'; // Redirigir a la página principal
        }, 3000); // Cambia este valor para ajustar la duración del feedback
    }

    function mostrarFeedbackLogin() {
        var feedback = document.getElementById("login-message");
        feedback.style.display = "block";
        setTimeout(function() {
            feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
            window.location.href = '/usuarios/login/';
        }, 3000); // Cambia este valor para ajustar la duración del feedback
    }

    actualizarCarritoConfirmacion();
});