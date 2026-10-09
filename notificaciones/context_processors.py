"""
Context processors del modulo de notificaciones.
"""


def notificaciones_no_leidas(request):
    """
    Agrega al contexto la cantidad de notificaciones no leidas del usuario actual.
    """
    if request.user.is_authenticated:
        return {
            'notificaciones_no_leidas': request.user.notificaciones.filter(leida=False).count()
        }
    return {'notificaciones_no_leidas': 0}
