# Sistema de Gestion de Talleres de Biblioteca

Sistema web para la gestion de talleres recreativos de una biblioteca, con control de alumnos, docentes, pagos, asistencia, ingresos y notificaciones.

## Caracteristicas

- **Gestion de usuarios**: Registro, login, roles (alumno, docente, administrador)
- **Gestion de talleres**: CRUD completo, horarios, cupo, cuota mensual
- **Inscripciones**: Con control de cupo y lista de espera
- **Pagos**: Cuotas mensuales, registro de pagos, estado "al dia" / "adeudado" / "pago parcial"
- **Asistencia**: Planilla por clase, calculo de promedios
- **Control de ingreso**: Registro por DNI, visualizacion de talleres inscriptos
- **Notificaciones**: Avisos dentro del sistema y por email
- **Estadisticas**: Panel con graficos y exportacion a CSV
- **Auditoria**: Registro de acciones criticas

## Requisitos

- Python 3.11+
- PostgreSQL (para produccion) o SQLite (para desarrollo)

## Instalacion rapida

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/Gestion-Talleres-Biblioteca-Alberdi.git
   cd Gestion-Talleres-Biblioteca-Alberdi
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con los valores reales
   ```

5. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

8. **Abrir en el navegador:**
   ```
   http://127.0.0.1:8000/
   ```

## Pruebas

Ejecutar todas las pruebas automatizadas:

```bash
python manage.py test
```

## Documentacion

- [Manual de usuario](docs/manual_usuario.md)
- [Documentacion tecnica](docs/documentacion_tecnica.md)
- [Guia de despliegue](docs/despliegue.md)
- [Hoja de ruta](docs/hoja_de_ruta.md)

## Despliegue

Ver `docs/despliegue.md` para instrucciones detalladas sobre como publicar el sistema en internet.

## Licencia

Este proyecto es de uso educativo.
