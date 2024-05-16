fetch('/pedidos/solicitar/' + pk + '/', {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    }
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // alert('Pedido realizado con éxito.');
        mostrarFeedbackSolicitudPedido();
        // Otras acciones si el pedido se realiza correctamente
    } else {
        alert('Error: ' + data.message);
        // Otras acciones si hay un error en el pedido
    }
})
.catch(error => {
    console.error('Error al procesar la solicitud: ', error);
});

function mostrarFeedbackSolicitudPedido() {
    var feedback = document.getElementById("feedback-solicitudPeds");
    feedback.style.display = "block";
    setTimeout(function() {
        feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
        window.location.href = '/listado_products/'; // Redirigir a la página principal
    }, 3000); // Cambia este valor para ajustar la duración del feedback
}


fetch('/pedidos/confirmar/' + pk + '/', {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    }
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // alert('Pedido confirmado.');
        mostrarFeedbackConfirmacionPedido();
        // Otras acciones si el pedido se confirma correctamente
    } else {
        alert('Error: ' + data.message);
        // Otras acciones si hay un error al confirmar el pedido
    }
})
.catch(error => {
    console.error('Error al procesar la solicitud: ', error);
});

function mostrarFeedbackConfirmacionPedido() {
    var feedback = document.getElementById("confirmation-message");
    feedback.style.display = "block";
    setTimeout(function() {
        feedback.style.display = "none"; // Ocultar el feedback después de unos segundos
        window.location.href = '/'; // Redirigir a la página principal
    }, 3000); // Cambia este valor para ajustar la duración del feedback
}