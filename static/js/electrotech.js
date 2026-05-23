/**
 * ELECTROTECH — Funciones JavaScript compartidas
 * Plataforma de gestión de inventario de hardware
 */

// ============================================================
// Confirmación antes de eliminar
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    // Todos los botones con clase 'confirmar-eliminar' piden confirmación
    document.querySelectorAll('.confirmar-eliminar').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('¿Está seguro de que desea eliminar este elemento? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });

    // Todos los formularios con clase 'form-confirmar' piden confirmación al enviar
    document.querySelectorAll('.form-confirmar').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm('¿Está seguro de que desea realizar esta acción? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
});

// ============================================================
// Habilitar/deshabilitar fecha/hora personalizada y validaciones
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const usarCheckbox = document.getElementById('id_usar_fecha_hora');
    const customFields = document.querySelectorAll('.custom-datetime');

    function toggleCustomFields() {
        const enabled = usarCheckbox && usarCheckbox.checked;
        customFields.forEach(function (el) {
            el.disabled = !enabled;
        });
    }

    if (usarCheckbox) {
        toggleCustomFields();
        usarCheckbox.addEventListener('change', toggleCustomFields);
    }

    // Forzar que los campos de cédula sólo acepten números en cliente
    document.querySelectorAll('input[name="cedula"]').forEach(function (input) {
        input.addEventListener('input', function (e) {
            const cleaned = this.value.replace(/[^0-9]/g, '');
            if (this.value !== cleaned) this.value = cleaned;
        });
    });
});

// ============================================================
// Cerrar mensajes automáticamente después de 5 segundos
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const mensajes = document.querySelectorAll('.animate-fade-in');
    mensajes.forEach(function (msg) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease';
            setTimeout(function () {
                if (msg.parentElement) {
                    msg.remove();
                }
            }, 500);
        }, 5000);
    });
});

// ============================================================
// Vista previa de imagen antes de subir
// ============================================================
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// ============================================================
// Imprimir página actual
// ============================================================
function imprimirPagina() {
    window.print();
}
