document.addEventListener('DOMContentLoaded', function() {
    const user_type = document.getElementById('id_user_type');
    const empleado_fields = document.getElementById('empleado_fields');
    const cliente_fields = document.getElementById('cliente_fields');

    function toggleFields() {
        if (user_type.value === 'empleado') {
            empleado_fields.style.display = 'block';
            cliente_fields.style.display = 'none';
        } else if (user_type.value === 'cliente') {
            empleado_fields.style.display = 'none';
            cliente_fields.style.display = 'block';
        } else {
            empleado_fields.style.display = 'none';
            cliente_fields.style.display = 'none';
        }
    }

    user_type.addEventListener('change', toggleFields);
    toggleFields(); // Llamar a la función inicialmente para mostrar los campos adecuados según el valor actual del selector
});