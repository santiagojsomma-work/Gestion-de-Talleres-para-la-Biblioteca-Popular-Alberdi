# PROGRESO.md - Sistema de Gestion de Talleres de Biblioteca

## Estado del proyecto

- **Etapa actual**: Etapa 3 - Talleres y horarios
- **Fecha de inicio**: 2026-10-03
- **Estado**: Etapa 2 completada

## Etapas completadas

| Etapa | Nombre | Estado | Fecha |
|-------|--------|--------|-------|
| 0 | Analisis y planificacion | Completada | 2026-10-03 |
| 1 | Entorno y esqueleto del proyecto | Completada | 2026-10-06 |
| 2 | Usuarios y roles | Completada | 2026-10-07 |

## Decisiones tomadas

### Reglas de negocio validadas (Etapa 0)

1. **Estado de pago**: Tres estados posibles: "Al dia", "Pago parcial" y "Adeudado".
2. **Alumnos activos**: Se consideran activos desde el dia de su inscripcion, sin periodo de gracia.
3. **Calculo de % al dia**: Solo se consideran cuotas vencidas hasta la fecha de hoy, no las futuras.
4. **Promedio de asistencia**: Solo se contabilizan las clases posteriores a la inscripcion del alumno.
5. **Registro de pagos**: El docente o administrador registra el pago. El alumno solo consulta. Se envia email automatico al alumno cuando se registra su pago.
6. **Menores de edad**: Es obligatorio cargar datos del padre, madre o tutor. El sistema valida automaticamente segun fecha de nacimiento.

## Proximos pasos

- Completar los documentos de analisis de la Etapa 0.
- Realizar el primer commit.
- Comenzar la Etapa 1: Entorno y esqueleto del proyecto.

## Ideas futuras

- Implementar pasarela de pago Mercado Pago.
- Crear API REST con Django REST Framework.
- Convertir la aplicacion en PWA (Progressive Web App).
- Agregar notificaciones push.
- Implementar reportes en PDF.
