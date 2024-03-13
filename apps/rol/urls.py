from django.urls import path
from .views import RolView, RolUserView, DeleteRolUserView, AddRolUserView, AgregarRolView

urlpatterns = [

    path('roles/', RolView.as_view(), name='roles'),
    path('rolesUsuario/<int:user_id>/', RolUserView.as_view(), name='rolesUsuario'),
    path('eliminarRolesUsuario/<int:user_id>/<int:permission_id>/', DeleteRolUserView.as_view(), name='rolesUsuarioDelet'),
    path('agregarRolesUsuario/<int:user_id>/', AddRolUserView.as_view(), name='rolesUsuarioAdd'),
    path('agregarRol/<int:user_id>/<int:permission_id>', AgregarRolView.as_view(), name='agregarPermiso'),

]