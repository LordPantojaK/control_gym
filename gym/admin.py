from django.contrib import admin

# Register your models here.
from .models import Noticia, Sucursal, Salon, Miembro, Profesor, Pago, Membrecia, Clase

#admin.site.register(Profes)
#admin.site.register(Miembroo)
#admin.site.register(Horario)
#admin.site.register(Distributivo)
class NoticiaAdmin(admin.ModelAdmin):
	list_display = ('autor','titulo','fecha')

admin.site.register(Noticia,NoticiaAdmin)
admin.site.register(Sucursal)
admin.site.register(Salon)
admin.site.register(Miembro)
admin.site.register(Profesor)
admin.site.register(Clase)
admin.site.register(Membrecia)
admin.site.register(Pago)

