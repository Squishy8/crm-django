from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor"""

    def dispatch(self, request,  *args, **kwargs):
        if not request.user.is_organisor or not request.user.is_authenticated:
            return redirect("leads:lead-list")
            """return self.handle_no_permission()#Este método regresa un error 503, indicando que no tiene permiso."""
        return super().dispatch(request, *args, **kwargs)
    
    #Este mixin personalizado nos ayuda a verificar que un usuario este logeado Y además que sea un organisor para poder acceder a las vistas de la app Agents