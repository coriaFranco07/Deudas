from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from functools import reduce
import operator
from django.db.models import Q




class RolView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
    template_name = 'usuarios_roles.html'
    permission_required = "auth.add_user"
    login_url = 'index' 

    def get(self, request, *args, **kwargs):
        users_with_permissions = User.objects.prefetch_related('user_permissions').all()
        context = {'users_with_permissions': users_with_permissions}
        return render(request, self.template_name, context)
    

    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('index')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
    
class RolUserView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
    template_name = 'usuario_permisos.html'
    

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        user_permissions = user.user_permissions.all()
        context = {'selected_user': user, 'user_permissions': user_permissions}
        return render(request, self.template_name, context)
    

    permission_required = "auth.add_user"
    login_url = 'index' 

    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('roles')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

class DeleteRolUserView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
    template_name = 'delete_usuarioPermiso.html'

    def get(self, request, user_id, permission_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        permission = get_object_or_404(Permission, pk=permission_id)
        context = {'user': user, 'permission': permission}
        return render(request, self.template_name, context)
    

    permission_required = "auth.add_user"
    login_url = 'index' 


    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('roles')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
    


    def post(self, request, user_id, permission_id, *args, **kwargs):
        user = User.objects.get(pk=user_id)
        permission = Permission.objects.get(pk=permission_id)
        user.user_permissions.remove(permission)
        return redirect('roles')

class AddRolUserView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
    template_name = 'add_usuarioPermiso.html'

    permission_required = "auth.add_user"
    login_url = 'index' 

    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('roles')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        
        # Obtener todos los permisos, incluidos los específicos de superusuario
        data=['Agregar','Eliminar','Modificar','Ver']
        all_permissions = Permission.objects.filter(reduce(operator.or_, (Q(name__icontains=p) for p in data)))

        # Obtener permisos asignados al usuario
        user_permissions = user.user_permissions.all()

        context = {
            'user': user,
            'all_permissions': all_permissions,
            'user_permissions': user_permissions,
        }

        return render(request, self.template_name, context)

class AgregarRolView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
    def get(self, request, user_id, permission_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        permission = get_object_or_404(Permission, pk=permission_id)
        user.user_permissions.add(permission)
        return redirect('roles')
    
    permission_required = "auth.add_user"
    login_url = 'index' 

    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('roles')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
