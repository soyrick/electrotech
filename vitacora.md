# 🧠 Vitácora de Proyecto — ElectroTech

> **Propósito:** Archivo de contexto entre sesiones. Leer SIEMPRE al iniciar una nueva sesión de trabajo.  
> **Última actualización:** 20 de mayo de 2026 — 23:00 UTC-4 — **Sesión #1 CERRADA**

---

## 🟢 AL INICIAR UNA NUEVA SESIÓN — CHECKLIST

Cuando se abra una nueva sesión de trabajo, el agente DEBE:

1. **Leer este archivo completo** (`vitacora.md`).
2. **Leer `fases.md`** para conocer el estado de cada tarea.
3. **Activar el entorno virtual:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. **Activar SDD** (`sdd-init-lowcost` ya fue ejecutado; verificar con `mem_search`).
5. **Buscar en Engram** el estado anterior: `mem_search(query: "sdd/electrotech/state")`.
6. **Ubicarse en la Fase 3 — CRUD de Componentes e Inventario** (primera tarea pendiente).
7. **NO construir nada sin preguntar primero** (modo interactivo activo desde Fase 3).

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

2. **Activar Engram y SDD cada sesión:** El sistema de memoria persistente (Engram) y el flujo de trabajo SDD (Spec-Driven Development) deben estar activos en cada sesión. No omitir.

3. **No suponer nada:** No dar nada por sentado. Verificar siempre antes de actuar.

4. **Solo hacer lo solicitado:** No ejecutar acciones no pedidas explícitamente por el usuario.

5. **Idioma:** Español neutral latinoamericano en TODO el código, templates, comentarios, mensajes al usuario y documentación.

6. **Versión de Django adaptable:** El proyecto usa Django 6.0.3 como base. En `requirements.txt` se especifica `Django>=5.0,<6.1` para que cada miembro del equipo pueda usar la versión 5.x o 6.x según su entorno. Cada miembro debe adaptar su entorno virtual a la versión especificada en `requirements.txt`.

7. **Commits convencionales:** Usar Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

8. **No hacer build automático:** Nunca ejecutar build después de cambios a menos que se solicite explícitamente.

---

## 📊 Estado Actual del Proyecto

| Fase | Estado | Descripción |
|---|---|---|
| 0 — Inicialización | ✅ Completada | Venv, Django, estructura, templates base, static files, commit |
| 1 — Auth y Roles | ✅ Completada | Login/logout, roles, formularios, decoradores, templates |
| 2 — Modelos Base | ✅ Completada | Categoría, Componente, Movimiento, DetalleMovimiento, migraciones, seeds |
| 3 — CRUD + Inventario | 🔲 Pendiente | Vistas y templates del catálogo visual y CRUD |
| 4 — Ingreso/Egreso | 🔲 Pendiente | Formularios, lógica de stock, planillas PDF con ReportLab |
| 5 — Dashboard/Métricas | 🔄 Parcial | Dashboard base listo (tarjetas, header, alertas). Falta: métricas, historial, Chart.js |
| 6 — Pulido final | 🔲 Pendiente | README, validaciones extra, pruebas |

---

## 🔧 Datos Técnicos

- **Python:** 3.12.10
- **Django:** 6.0.3 (instalado en .venv)
- **Node.js:** v24.14.1 (disponible)
- **Base de datos:** SQLite (`db.sqlite3` creado con 12 tablas)
- **PDF:** ReportLab 4.5.1
- **CSS:** Tailwind CSS (CDN) con paleta personalizada
- **Íconos:** Font Awesome 6.5.1 (CDN)
- **Gráficas:** Chart.js (CDN, pendiente implementar)
- **Entorno virtual:** `.venv/` (raíz del proyecto)

---

## 🔑 Credenciales Semilla

| Rol | Email | Contraseña |
|---|---|---|
| Super-admin | ricardoenriquegr27@gmail.com | regr270998 |

---

## 📂 Estructura del Proyecto (estado actual)

```
electrotech/
├── manage.py
├── requirements.txt
├── vitacora.md
├── fases.md
├── db.sqlite3
├── .venv/
├── electrotech/           # Configuración del proyecto
│   ├── settings.py        # Configurado: apps, DB, static, media, i18n
│   ├── urls.py            # Rutas principales con includes
│   ├── context_processors.py  # Datos globales (stock bajo)
│   └── ...
├── accounts/              # ✅ Autenticación y roles
│   ├── models.py          # Usuario personalizado (AbstractUser + rol)
│   ├── forms.py           # LoginForm, CrearAdminForm, CambiarPasswordForm
│   ├── views.py           # login, logout, crear_admin, cambiar_password
│   ├── decorators.py      # super_admin_required, admin_required
│   ├── urls.py
│   └── admin.py
├── inventory/             # ✅ Modelos listos, vistas placeholder
│   ├── models.py          # Categoria, Componente
│   ├── views.py           # Placeholders (pendiente implementar)
│   └── ...
├── movements/             # ✅ Modelos listos, vistas placeholder
│   ├── models.py          # Movimiento, DetalleMovimiento
│   └── ...
├── metrics/               # 🔄 Dashboard base listo, vistas placeholder
│   ├── views.py
│   ├── urls.py
│   └── urls_dashboard.py
├── templates/
│   ├── base.html          # Layout con Tailwind + Font Awesome + Header nav
│   ├── accounts/
│   │   ├── login.html     # Login con gradiente oscuro
│   │   ├── crear_admin.html
│   │   ├── cambiar_password.html
│   │   └── permiso_denegado.html
│   └── metrics/
│       └── dashboard.html # Dashboard con 6 tarjetas + panel admin
├── static/
│   ├── css/electrotech.css
│   └── js/electrotech.js
└── media/
    └── componentes/
```

---

## ⏭️ Próxima Sesión — Fase 3

**Tareas prioritarias:**
1. Implementar vistas reales de inventory: listado catálogo, detalle, CRUD
2. Implementar filtro por categoría con dropdown dinámico
3. Templates de tarjetas del inventario con diseño responsive
4. Subida y visualización de imágenes con placeholder
5. Commit de Fase 3

**Nota:** El usuario indicó modo interactivo a partir de Fase 2 (que ya está completa en modelos). La Fase 3 será la primera en modo interactivo con revisión entre pasos.

---

## 📝 Historial de Sesiones

### Sesión #1 — 20 de mayo de 2026 (22:18 - 23:00) ✅ CERRADA
- Proyecto iniciado desde cero. Repo vacío.
- Rama renombrada `master` → `main`.
- SDD inicializado con engram (topic: `sdd-init-lowcost/electrotech`).
- Creados: vitacora.md, fases.md, .venv, estructura Django completa.
- **Fase 0 completada:** Proyecto Django, dependencias, estructura, static, templates base.
- **Fase 1 completada:** Auth con roles, login/logout, formularios, decoradores, 4 templates.
- **Fase 2 completada:** Modelos Categoria, Componente, Movimiento, DetalleMovimiento, migraciones, 13 seeds.
- **Dashboard base listo:** 6 tarjetas de acceso, alerta stock bajo, header responsive.
- Commit inicial: `9810ea3` — 58 archivos, 2,653 líneas.
- **Modo de trabajo:** Automático para Fases 0-2. A partir de Fase 3 → **INTERACTIVO** (revisar entre pasos).
- **Artifact store:** Engram activo. SDD inicializado.
- **Próxima acción:** Iniciar Fase 3 — CRUD de Componentes e Inventario.
