"""
Exportado de Modulos
"""
from django.contrib import admin
from .models import User

"""
UserAdmin: Configuarion del panel de administracion
"""
class UserAdmin(admin.ModelAdmin):
    list_filter = ('user_type', )
    search_fields = ('username', 'last_name', 'first_name', 'email')
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type')

"""
Otras configuraciones
"""
title = 'Proyecto Tokio Ivan Labrador'
subtitle = 'Panel de Gestion'
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle

"""
Registro de modelos
"""
admin.site.register(User, UserAdmin)