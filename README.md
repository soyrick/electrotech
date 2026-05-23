<div align="center">

<img src="https://img.shields.io/badge/Django-6.0.3-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/Python-3.12.10-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind">
<img src="https://img.shields.io/badge/ReportLab-PDF-CC0000?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="ReportLab">
<img src="https://img.shields.io/badge/Chart.js-Metrics-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
<img src="https://img.shields.io/badge/SQLite-DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">

</div>

<br>

<div align="center">

# ⚡ ElectroTech

### Sistema de Gestión de Inventario de Hardware

*Plataforma web para el control de inventario de componentes de computadora y hardware. Desarrollado como proyecto universitario con Django + Tailwind CSS + ReportLab.*

[![Status](https://img.shields.io/badge/status-en%20desarrollo-blue?style=flat-square)]()
[![PRs](https://img.shields.io/badge/PRs-bienvenidos-brightgreen?style=flat-square)]()
[![Licencia](https://img.shields.io/badge/licencia-MIT-yellow?style=flat-square)]()

</div>

---

## 🎯 ¿Qué es ElectroTech?

ElectroTech es una plataforma web responsive diseñada para la **gestión integral de inventario** de un almacén de piezas de computadora y componentes de hardware. Permite registrar entradas y salidas de componentes, generar planillas en PDF con diseño profesional, visualizar métricas con gráficas interactivas y mantener un historial completo de movimientos.

---

## ✨ Características Principales

| Módulo | Descripción |
|--------|-------------|
| 🔐 **Autenticación** | Login con roles (Super Admin / Admin), control de permisos por decorador |
| 📦 **Inventario** | Catálogo visual tipo tarjetas con CRUD completo, filtros por categoría, imágenes |
| 📥 **Ingresos** | Registro de entrada de componentes con generación automática de planillas PDF |
| 📤 **Egresos** | Registro de salida con control de stock, selección múltiple y planillas PDF |
| 📄 **Planillas PDF** | Comprobantes estilo factura con diseño profesional, encabezado claro, tipo de movimiento resaltado y firmas para impresión |
| �📊 **Métricas** | Dashboard con gráficas Chart.js (ingresos vs egresos), resumen métrico mensual |
| 📜 **Historial** | Registro completo de movimientos con snapshots históricos y re-generación de PDF |
| 🎨 **Dark Theme** | Sistema de diseño global con glassmorphism, animaciones y fondo tech interactivo |

---

## 🛠️ Stack Tecnológico

| Tecnología | Uso |
|------------|-----|
| [Django 6.0.3](https://www.djangoproject.com/) | Backend framework |
| [Tailwind CSS](https://tailwindcss.com/) | Estilos utilitarios (CDN) |
| [Font Awesome 6.5](https://fontawesome.com/) | Íconos |
| [ReportLab 4.5](https://www.reportlab.com/) | Generación de PDF |
| [Chart.js](https://www.chartjs.org/) | Gráficas interactivas |
| [SQLite](https://www.sqlite.org/) | Base de datos |

---

## 👥 Equipo

| Integrante | Rol | Fases |
|------------|-----|-------|
| 🧑‍💼 **Ricardo** | Coordinador / Arquitecto | Fase 0-2 + Sistema de diseño global |
| 🧑‍💻 **Daniel** | Desarrollador | Fase 3 (CRUD) + Fase 4 (Ingreso/Egreso PDF) |
| 🧑‍💻 **Alejandro** | Desarrollador | Fase 5 (Dashboard/Métricas) + Fase 6 (Pulido) |

---

## 🚀 Instalación Rápida

```powershell
# Clonar el repositorio
git clone https://github.com/soyrick/electrotech.git
cd electrotech

# Cambiar a la rama de desarrollo
git checkout develop

# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador.

---

## 🔑 Credenciales por Defecto

| Rol | Email | Contraseña |
|-----|-------|------------|
| Super Admin | `ricardoenriquegr27@gmail.com` | `regr270998` |

> Después del primer inicio de sesión, creá cuentas de administrador desde el Panel de Administración del dashboard.

---

## 📂 Estructura del Proyecto

```
electrotech/
├── electrotech/              # ⚙️ Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py
├── accounts/                 # 🔐 Auth y roles
│   ├── models.py             # Usuario personalizado (AbstractUser + rol)
│   ├── forms.py              # LoginForm, CrearAdminForm, CambiarPasswordForm
│   ├── views.py              # Login, logout, gestión de admins
│   └── decorators.py         # super_admin_required, admin_required
├── inventory/                # 📦 Componentes (Fase 3 — Daniel)
│   ├── models.py             # Categoria, Componente
│   └── views.py              # CRUD
├── movements/                # 📥📤 Movimientos (Fase 4 — Daniel)
│   ├── models.py             # Movimiento, DetalleMovimiento (snapshots)
│   └── views.py              # Ingresos, egresos, PDF
├── metrics/                  # 📊 Dashboard + Métricas (Fase 5 — Alejandro)
│   ├── views.py              # Dashboard, gráficas, historial
│   └── urls.py
├── templates/
│   ├── base.html             # 🎨 Layout global + fondo tech
│   ├── accounts/             # Login partido, crear admin, cambiar password
│   └── metrics/              # Dashboard glass, métricas
├── static/
│   ├── css/electrotech.css   # ⭐ Sistema de diseño global (16 secciones)
│   └── js/electrotech.js     # Utilidades JS
├── media/componentes/        # 🖼️ Imágenes subidas
├── fases.md                  # 📐 Plan de desarrollo por fases + protocolo IA
├── vitacora.md               # 🧠 Bitácora de proyecto + contexto entre sesiones
└── requirements.txt
```

---

## 🎨 Sistema de Diseño

El proyecto cuenta con un **sistema de diseño unificado** en `static/css/electrotech.css` con 16 secciones de clases reutilizables:

| Sección | Clases clave |
|---------|-------------|
| 🃏 Tarjetas | `.glass-card`, `.dashboard-card`, `.inventory-card` |
| 📝 Formularios | `.dark-input`, `.dark-select`, `.dark-textarea`, `.dark-label` |
| 🔘 Botones | `.btn-primary`, `.btn-danger`, `.btn-secondary`, `.btn-success`, `.btn-ghost` |
| 📊 Tablas | `.dark-table` |
| 🏷️ Badges | `.badge-blue`, `.badge-green`, `.badge-red`, `.badge-amber` |
| ⚠️ Alertas | `.alert-glass`, `.alert-danger`, `.alert-success` |
| 🎯 Iconos | `.icon-wrap-green`, `.icon-wrap-blue`, `.icon-wrap-purple` |

> **Todos los templates nuevos deben usar estas clases.** No inventar estilos nuevos.

---

## 🧾 Vista previa y fecha personalizada (nueva)

- Ahora al crear un `Ingreso` o `Egreso` se mostrará un **resumen del comprobante** antes de descargar el PDF. Esto permite revisar los datos y descargar la planilla manualmente.
- Se añadió una opción `Usar fecha y hora personalizada` en los formularios. Si se activa, puede seleccionar una **fecha** (selector de calendario) y una **hora** antes de confirmar. Si no está activa, se usa la fecha/hora actual detectada por el sistema.
- La entrada de `cédula` ahora acepta sólo dígitos en el cliente y se valida en el servidor.


## 📐 Fases del Proyecto

El desarrollo está dividido en 6 fases. Para ver el detalle completo y el protocolo para agentes de IA, consultá [`fases.md`](fases.md).

| Fase | Descripción | Estado |
|------|-------------|--------|
| 0 | Inicialización del proyecto | ✅ |
| 1 | Autenticación y roles | ✅ |
| 2 | Modelos de datos | ✅ |
| 3 | CRUD de componentes | 🔲 |
| 4 | Ingreso y egreso + PDF | 🔲 |
| 5 | Dashboard, métricas, historial | ✅ |
| 6 | Diseño, pulido y pruebas | 🔄 |

---

## 📄 Licencia

MIT — Sentite libre de usar, modificar y compartir.

---

<div align="center">

*Hecho por Ricardo, Daniel y Alejandro*

</div>
