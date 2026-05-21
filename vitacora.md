# 🧠 Vitácora de Proyecto — ElectroTech

> **Propósito:** Archivo de contexto entre sesiones. Leer SIEMPRE al iniciar una nueva sesión de trabajo.  
> **Última actualización:** 21 de mayo de 2026 — Sesión #3 en progreso — Rama `develop`

---

## 🟢 AL INICIAR UNA NUEVA SESIÓN — CHECKLIST

Cuando se abra una nueva sesión de trabajo, el agente DEBE:

1. **Leer este archivo completo** (`vitacora.md`).
2. **Leer `fases.md`** para conocer el estado de cada tarea y la asignación del equipo.
3. **Activar el entorno virtual:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. **PREGUNTAR:** `"¿Cómo te llamás? (Daniel, Alejandro o Ricardo)"` para ubicar al usuario en sus fases.
5. **Activar SDD** (`sdd-init-lowcost` ya fue ejecutado; verificar con `mem_search`).
6. **Buscar en Engram** el estado anterior: `mem_search(query: "sdd/electrotech/state")`.
7. **NO construir nada sin preguntar primero** (modo interactivo activo).

---

## 👥 EQUIPO DE DESARROLLO

| Integrante | Rol | Fases | Rama |
|------------|-----|-------|------|
| **Ricardo** | Coordinador / Arquitecto | Fase 0, 1, 2 + Diseño global + Sistema de diseño | `main` (setup inicial) |
| **Daniel** | Desarrollador | **Fase 3** (CRUD Inventario) + **Fase 4** (Ingreso/Egreso PDF) | `develop` |
| **Alejandro** | Desarrollador | **Fase 5** (Dashboard/Métricas/Chart.js) + **Fase 6** (Pulido/Pruebas) | `develop` |

> ⚠️ **Dependencia:** Alejandro necesita que Daniel complete Fase 3 y 4 primero (sin datos de movimientos no hay métricas ni historial).

---

## 📋 Reglas de Sesión (OBLIGATORIAS)

1. **Activar entorno virtual SIEMPRE:** Antes de cualquier comando Python/Django, ejecutar:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   Si falla por políticas de ejecución:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

2. **Idioma:** Español neutral latinoamericano en TODO el código, templates, comentarios, mensajes al usuario y documentación.

3. **Sistema de diseño:** Usar las clases globales de `static/css/electrotech.css` (tema oscuro, glassmorphism, dark-inputs, dark-tables, badges, botones). NO inventar estilos nuevos — reutilizar los existentes.

4. **Versión de Django adaptable:** `Django>=5.0,<6.1` en `requirements.txt`.

5. **Commits convencionales:** `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.

6. **Rama de trabajo:** `develop` para Daniel y Alejandro. `main` solo para Ricardo.

7. **No hacer build automático** a menos que se solicite.

---

## 📊 Estado Actual del Proyecto

| Fase | Responsable | Estado | Descripción |
|------|-------------|--------|-------------|
| 0 — Inicialización | Ricardo | ✅ Completada | Venv, Django, estructura, templates base, static files |
| 1 — Auth y Roles | Ricardo | ✅ Completada | Login/logout, roles, formularios, decoradores, templates |
| 2 — Modelos Base | Ricardo | ✅ Completada | Categoría, Componente, Movimiento, DetalleMovimiento, migraciones, 13 seeds |
| 3 — CRUD + Inventario | **Daniel** | 🔲 Pendiente | Vistas y templates del catálogo visual y CRUD |
| 4 — Ingreso/Egreso | **Daniel** | 🔲 Pendiente | Formularios, lógica de stock, planillas PDF con ReportLab |
| 5 — Dashboard/Métricas | **Alejandro** | 🔄 Parcial | Templates base listos (dashboard + métricas). Falta: lógica, Chart.js, historial |
| 6 — Pulido final | **Alejandro** | 🔄 Parcial | Sistema de diseño global listo. Falta: responsive, validaciones, README, pruebas |

---

## 🎨 Sistema de Diseño Global (NUEVO — Sesión #3)

El proyecto ahora tiene un sistema de diseño unificado en `static/css/electrotech.css`:

- **Tema oscuro** por defecto en sesiones autenticadas (`#080d14`)
- **Fondo tech animado** global: chip SVG flotante, trazas de circuito, partículas azules
- **Tarjetas glass**: `.glass-card`, `.glass-card-flat`, `.dashboard-card`, `.inventory-card`
- **Formularios**: `.dark-input`, `.dark-select`, `.dark-textarea`, `.dark-label`, `.dark-input-icon`
- **Botones**: `.btn`, `.btn-primary`, `.btn-danger`, `.btn-secondary`, `.btn-success`, `.btn-ghost`
- **Tablas**: `.dark-table`
- **Badges**: `.badge`, `.badge-blue/-green/-red/-amber/-gray/-purple`
- **Alertas**: `.alert-glass`, `.alert-danger/-warning/-info/-success`
- **Tipografía**: `.text-heading`, `.text-body`, `.text-muted`, `.text-subtle`, `.text-accent`
- **Iconos**: `.icon-wrap`, `.icon-wrap-green/-red/-blue/-purple/-amber/-gray`

Todos los templates nuevos DEBEN usar estas clases. Ver `electrotech.css` para la referencia completa.

---

## 🔧 Datos Técnicos

- **Python:** 3.12.10
- **Django:** 6.0.3 (instalado en .venv)
- **Node.js:** v24.14.1 (disponible)
- **Base de datos:** SQLite (`db.sqlite3` creado con 12 tablas)
- **PDF:** ReportLab 4.5.1
- **CSS:** Tailwind CSS (CDN) + `electrotech.css` (sistema de diseño)
- **Íconos:** Font Awesome 6.5.1 (CDN)
- **Gráficas:** Chart.js (CDN, pendiente implementar por Alejandro)
- **Entorno virtual:** `.venv/` (raíz del proyecto)
- **Ramas:** `main` (producción) | `develop` (desarrollo activo)

---

## 🔑 Credenciales Semilla

| Rol | Email | Contraseña |
|---|---|---|
| Super-admin | ricardoenriquegr27@gmail.com | regr270998 |

---

## 📂 Estructura del Proyecto

```
electrotech/
├── manage.py
├── requirements.txt
├── vitacora.md
├── fases.md
├── db.sqlite3
├── .venv/
├── electrotech/              # Config del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py
├── accounts/                 # ✅ Auth y roles
│   ├── models.py             # Usuario personalizado (AbstractUser + rol)
│   ├── forms.py              # LoginForm, CrearAdminForm, CambiarPasswordForm
│   ├── views.py              # login, logout, crear_admin, cambiar_password
│   ├── decorators.py         # super_admin_required, admin_required
│   └── urls.py
├── inventory/                # 🔲 Modelos listos, vistas placeholder (Fase 3 — Daniel)
│   ├── models.py             # Categoria, Componente
│   └── views.py              # Placeholders
├── movements/                # 🔲 Modelos listos, vistas placeholder (Fase 4 — Daniel)
│   ├── models.py             # Movimiento, DetalleMovimiento
│   └── views.py              # Placeholders
├── metrics/                  # 🔄 Templates base listos (Fase 5 — Alejandro)
│   ├── views.py              # dashboard, metricas_graficas, historial
│   └── urls.py
├── templates/
│   ├── base.html             # Layout con fondo tech + tema oscuro autenticado
│   ├── accounts/
│   │   ├── login.html        # Login partido (gris/azul + chip SVG)
│   │   ├── crear_admin.html
│   │   ├── cambiar_password.html
│   │   └── permiso_denegado.html
│   └── metrics/
│       ├── dashboard.html    # 6 tarjetas glass + panel admin
│       └── graficas.html     # Filtros + placeholder gráfica + resumen métrico
├── static/
│   ├── css/electrotech.css   # ⭐ Sistema de diseño global
│   └── js/electrotech.js
└── media/
    └── componentes/
```

---

## ⏭️ Próximas Acciones

### Daniel (Fase 3 → 4)
1. Implementar `inventory/views.py`: listado, detalle, crear, editar, eliminar (CRUD)
2. Crear templates en `templates/inventory/`: `listado.html`, `detalle.html`, `crear.html`, `editar.html`, `eliminar.html`
3. Filtro por categoría con dropdown dinámico
4. Subida de imágenes con preview y placeholder
5. Luego Fase 4: ingresos, egresos, planillas PDF, control de stock

### Alejandro (Fase 5 → 6)
1. Implementar `api_datos_grafica` (JSON para Chart.js)
2. Conectar Chart.js en `graficas.html` (ingresos azul, egresos rojo)
3. Crear `templates/metrics/historial.html` con tabla de movimientos
4. Vista de planilla histórica (re-generar PDF desde snapshots)
5. Luego Fase 6: validaciones, responsive, README, pruebas

---

## 📝 Historial de Sesiones

### Sesión #3 — 21 de mayo de 2026 (en progreso) — Rama `develop`
- **Rama `develop` creada** desde `main` (commit `8142fb9`).
- **Sistema de diseño global** implementado en `electrotech.css` (16 secciones de clases reutilizables).
- **Fondo tech** (chip SVG, trazas, partículas) agregado a `base.html` (visible en sesiones autenticadas).
- **Dashboard rediseñado** con glassmorphism, íconos de colores, alertas glass.
- **Métricas** (`graficas.html`) creado con filtros, placeholder de gráfica, 4 tarjetas de resumen.
- **Login rediseñado** con layout partido 50/50, difuminado azul/gris, chip SVG animado.
- **Comentarios `{# #}` → `<!-- -->`** en todos los templates (6 archivos).
- **`@login_required`** agregado a dashboard y vistas de metrics.
- **`fases.md` actualizado** con asignación del equipo (Daniel F3+F4, Alejandro F5+F6) y protocolo para IA.
- **`vitacora.md` actualizado** con estructura del equipo, sistema de diseño, próximas acciones.

### Sesión #2 — 20 de mayo de 2026 (22:30 - 23:06) ✅ CERRADA
- Exploración inicial del proyecto, lectura completa de archivos.
- Detectado bug: dashboard sin `@login_required`.
- Detectado bug: comentarios `{# #}` visibles en HTML renderizado.
- Servidor Django levantado en puerto 8000.
- Propuestas de rediseño exploradas.

### Sesión #1 — 20 de mayo de 2026 (22:18 - 23:00) ✅ CERRADA
- Proyecto iniciado desde cero. Repo vacío.
- SDD inicializado con engram (topic: `sdd-init-lowcost/electrotech`).
- **Fase 0 completada:** Proyecto Django, dependencias, estructura, static, templates base.
- **Fase 1 completada:** Auth con roles, login/logout, formularios, decoradores, 4 templates.
- **Fase 2 completada:** Modelos Categoria, Componente, Movimiento, DetalleMovimiento, migraciones, 13 seeds.
- Commit inicial: `9810ea3` — 58 archivos, 2,653 líneas.
