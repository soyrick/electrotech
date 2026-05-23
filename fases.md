# 📐 Fases del Proyecto — ElectroTech

> **Objetivo:** Dividir el desarrollo en fases ordenadas y trazables.  
> **Leyenda:** ✅ Completado | 🔄 En progreso | 🔲 Pendiente | ⚠️ Bloqueado

---

## 🤖 PROTOCOLO PARA AGENTES DE IA — LEER PRIMERO

**Al iniciar una sesión con un nuevo usuario, el agente DEBE:**

1. Leer este archivo completo y `vitacora.md`.
2. Activar el entorno virtual (`.\.venv\Scripts\Activate.ps1`).
3. **PREGUNTAR OBLIGATORIAMENTE:** `"¿Cómo te llamás? (Daniel o Alejandro)"` — o una variante si detecta un nombre distinto.
4. Según la respuesta, dirigir al usuario a sus fases asignadas (ver tabla abajo).
5. Si el nombre no coincide con Daniel ni Alejandro, preguntar si es **Ricardo** (coordinador) o un nuevo integrante.
6. Usar **español neutral latinoamericano** en TODO: código, templates, comentarios, mensajes.
7. Seguir el **sistema de diseño global** definido en `static/css/electrotech.css` (tema oscuro, glassmorphism, clases reutilizables).

---

## 👥 ASIGNACIÓN DE EQUIPO

| Integrante | Rol | Fases asignadas | Rama |
|------------|-----|-----------------|------|
| **Ricardo** | Coordinador / Arquitecto | Fase 0, 1, 2, diseño global | `main` |
| **Daniel** | Desarrollador Backend + Frontend | **Fase 3** (CRUD Inventario) + **Fase 4** (Ingreso/Egreso) | `develop` |
| **Alejandro** | Desarrollador Frontend + Métricas | **Fase 5** (Dashboard/Métricas) + **Fase 6** (Pulido) | `develop` |

> ⚠️ **IMPORTANTE:** Cada integrante trabaja en la rama `develop`. Daniel debe completar Fase 3 y 4 antes que Alejandro arranque Fase 5 (dependencia de datos).

---

## Fase 0: Inicialización del Proyecto — 👤 Ricardo
**Objetivo:** Preparar el entorno de desarrollo y la estructura base del proyecto Django.

- [x] 0.1 — Crear entorno virtual Python (.venv)
- [x] 0.2 — Instalar Django y dependencias base (ReportLab, Pillow)
- [x] 0.3 — Crear proyecto Django (`electrotech`)
- [x] 0.4 — Configurar `settings.py` (base de datos, static, media, timezone, idioma)
- [x] 0.5 — Crear apps: `accounts`, `inventory`, `movements`, `metrics`
- [x] 0.6 — Configurar `urls.py` principal con inclusión de apps
- [x] 0.7 — Crear estructura de templates base (`base.html` con Tailwind + Font Awesome)
- [x] 0.8 — Configurar archivos estáticos globales (CSS, JS)
- [x] 0.9 — Crear `requirements.txt`
- [x] 0.10 — Commit inicial del proyecto

---

## Fase 1: Autenticación y Roles — 👤 Ricardo
**Objetivo:** Sistema de login, roles (super-admin, admin) y gestión de usuarios.

- [x] 1.1 — Extender modelo User de Django con campo `rol`
- [x] 1.2 — Crear formulario de login personalizado (`LoginForm`)
- [x] 1.3 — Crear vista de login con validaciones
- [x] 1.4 — Crear template de login con diseño responsive (Tailwind, gradiente oscuro)
- [x] 1.5 — Implementar cierre de sesión
- [x] 1.6 — Crear vista panel super-admin: crear administradores
- [x] 1.7 — Crear vista panel super-admin: cambiar contraseñas
- [x] 1.8 — Implementar decoradores de permisos por rol (`super_admin_required`, `admin_required`)
- [x] 1.9 — Crear template de permisos denegados (403)
- [x] 1.10 — Seed: crear super-admin inicial (ricardoenriquegr27@gmail.com)

---

## Fase 2: Modelos de Datos — 👤 Ricardo
**Objetivo:** Definir todos los modelos Django para categorías, componentes, movimientos.

- [x] 2.1 — Modelo `Categoria` (nombre, fecha_creacion)
- [x] 2.2 — Modelo `Componente` (nombre, categoria, marca, modelo, serial, detalles, cantidad, ubicacion, imagen, fecha_ingreso, fecha_actualizacion)
- [x] 2.3 — Modelo `Movimiento` (tipo, numero_planilla, fecha_hora, usuario, datos_persona)
- [x] 2.4 — Modelo `DetalleMovimiento` (movimiento, componente, cantidad, snapshot_datos)
- [x] 2.5 — Crear migraciones y aplicarlas
- [x] 2.6 — Registrar modelos en Django Admin
- [x] 2.7 — Seed: crear 13 categorías iniciales

---

## Fase 3: CRUD de Componentes e Inventario — 🧑‍💻 Daniel
**Objetivo:** Catálogo visual de componentes con operaciones CRUD.
**Rama:** `develop`

> 📌 **Daniel**: Esta fase es tuya. Las vistas en `inventory/views.py` son placeholders — tenés que implementarlas con lógica real. Usá el sistema de diseño global (`electrotech.css`): tarjetas `.inventory-card`, formularios `.dark-input`, `.dark-select`, botones `.btn-primary`. El tema oscuro y fondo tech ya están configurados en `base.html`.

- [ ] 3.1 — Vista: listado de inventario (catálogo tipo tarjetas)
- [ ] 3.2 — Filtro por categoría (dropdown dinámico)
- [ ] 3.3 — Vista: detalle del componente
- [ ] 3.4 — Vista: crear componente (formulario con imagen)
- [ ] 3.5 — Vista: editar componente
- [ ] 3.6 — Vista: eliminar componente (con confirmación)
- [x] 3.7 — Configurar MEDIA_URL / MEDIA_ROOT para imágenes
- [ ] 3.8 — Placeholder genérico para componentes sin imagen
- [ ] 3.9 — Template del catálogo con diseño de tarjetas responsive
- [ ] 3.10 — Template de detalle del componente

---

## Fase 4: Ingreso y Egreso de Componentes — 🧑‍💻 Daniel
**Objetivo:** Registro de entradas y salidas con generación de planillas PDF.
**Rama:** `develop`

> 📌 **Daniel**: Esta fase también es tuya. Depende de que la Fase 3 esté completa (necesitás componentes en la DB). Las vistas en `movements/views.py` son placeholders. Usá ReportLab para los PDF. El modelo `Movimiento` ya tiene `generar_numero_planilla()` y `DetalleMovimiento` tiene `guardar_snapshot()`.

- [ ] 4.1 — Vista: formulario de ingreso de componentes
- [ ] 4.2 — Lógica: crear o actualizar componente al ingresar
- [ ] 4.3 — Numeración automática de planillas (ING-0001, ING-0002...)
- [ ] 4.4 — Generar PDF de planilla de ingreso (ReportLab)
- [ ] 4.5 — Impresión y descarga de planilla de ingreso
- [ ] 4.6 — Vista: formulario de egreso (selección múltiple de componentes)
- [ ] 4.7 — Validación: no retirar más de lo disponible
- [ ] 4.8 — Numeración automática de planillas (EGR-0001, EGR-0002...)
- [ ] 4.9 — Generar PDF de planilla de egreso (ReportLab)
- [ ] 4.10 — Impresión y descarga de planilla de egreso
- [ ] 4.11 — Actualizar stock automáticamente al egresar
- [ ] 4.12 — Guardar snapshot de datos del componente en DetalleMovimiento

---

## Fase 5: Dashboard, Métricas e Historial — 🧑‍💻 Alejandro
**Objetivo:** Panel principal con métricas, gráficas y registro histórico.
**Rama:** `develop`

> 📌 **Alejandro**: Esta fase es tuya. Depende de que Daniel complete Fase 3 y 4 (necesitás movimientos reales para métricas e historial). El dashboard y la vista de métricas ya tienen template con diseño glass. Implementá: API de datos JSON para Chart.js, vista de historial con tabla, y vista de planilla histórica. Usá las clases `.dark-table`, `.glass-card`, `.btn-*`.

- [x] 5.1 — Template del dashboard principal con 6 opciones en tarjetas
- [x] 5.2 — Tarjeta de alerta: componentes con stock bajo (≤ 3)
- [x] 5.3 — Header con navegación horizontal y botón de salir
- [x] 5.4 — Vista: métricas (selección de mes y componente)
- [x] 5.5 — Gráfica de líneas con Chart.js (ingresos azul, egresos rojo)
- [x] 5.6 — Resumen métrico (totales, días pico, componente más retirado)
- [x] 5.7 — Vista: historial de movimientos (tabla con filtros)
- [x] 5.8 — Botones ver planilla / imprimir / descargar PDF en historial
- [x] 5.9 — Vista de planilla histórica (re-generar PDF desde snapshot)

---

## Fase 6: Diseño, Pulido y Pruebas — 🧑‍💻 Alejandro
**Objetivo:** Afinar diseño responsive, validaciones y experiencia de usuario.
**Rama:** `develop`

> 📌 **Alejandro**: Esta fase también es tuya. Revisá responsive, agregá validaciones frontend/backend, creá el README.md, y ejecutá pruebas funcionales de todos los módulos.

- [ ] 6.1 — Revisar diseño responsive (escritorio, tablet, móvil)
- [x] 6.2 — Aplicar paleta de colores consistente (#1a66cc, #a3a8b7, #FFFFFF)
- [x] 6.3 — Efectos hover, sombras, bordes redondeados en tarjetas
- [ ] 6.4 — Validaciones de formularios (frontend + backend)
- [x] 6.5 — Mensajes de éxito/error claros (Django messages)
- [x] 6.6 — Logo genérico de ElectroTech preparado para reemplazo
- [x] 6.7 — Sistema de diseño global (CSS: glassmorphism, dark theme, forms, tablas, badges, botones)
- [x] 6.8 — Instrucciones finales en README.md para ejecutar el proyecto
- [ ] 6.9 — Pruebas funcionales de todos los módulos
- [ ] 6.10 — Commit final: "feat: plataforma ElectroTech completa"
