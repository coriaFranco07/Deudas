from typing import Any
from django.shortcuts import get_object_or_404, redirect,  render
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import AdminForm
from .models import HistorialAdmin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from .models import User, HistorialAdmin
from django.contrib.auth.hashers import make_password
from axes.utils import reset
from django.db import transaction
from django.utils import timezone
from django.contrib import messages



class ListAdmin(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=User
        template_name='admin.html'
        context_object_name='administradores' 
        permission_required = "auth.view_user"
        login_url = 'index' 

        def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('index')

        def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
        

class AddAdmin(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'add_admin.html'
    form_class = AdminForm
    permission_required = "auth.add_user"
    login_url = 'index'
    success_message = "Registro Creado Correctamente"

    def handle_no_permission(self):
        messages.error(self.request, 'Acceso Denegado!!!')
        return redirect('administradores')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
            try:
                with transaction.atomic():
                    password = form.cleaned_data.get('password')
                    print("CCCCCCCCCCCCCCCCCCCC" + password)
                    new_admin = form.save(commit=False)
                    new_admin.password = make_password(password)
                    new_admin.save()

                    # Obtener el ID del usuario en sesión
                    usuario = self.request.user

                    # Crear entrada en HistorialAdmin después de guardar el usuario
                    historial_entry = HistorialAdmin.objects.create(
                        id_user=new_admin.id,
                        username=new_admin.username,
                        email=new_admin.email,
                        h_user_proc=usuario,
                        h_fch_creacion=new_admin.date_joined,
                        h_tipo_proc='C',
                    )

                    return super().form_valid(form)
            except Exception as e:
                messages.error(self.request, 'Error en el servidor')
                return JsonResponse({'mensaje': 'Error en el servidor', 'error': str(e)}, status=500)

    def form_invalid(self, form):
        mensaje = 'No se ha podido realizar el Registro'
        error = form.errors
        response = JsonResponse({'mensaje': mensaje, 'error': error})
        response.status_code = 400
        return response

    def get_success_url(self):
        return reverse('list_admins')
    

class EditAdmin(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'edit_admin.html'
    form_class = AdminForm
    success_message = 'Registro editado correctamente'
    permission_required = "auth.change_user"
    login_url = 'index'

    def handle_no_permission(self):
        messages.error(self.request, 'Acceso Denegado!!!')
        return redirect('list_admins')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                password = form.cleaned_data.get('password')
                new_admin = form.save(commit=False)
                new_admin.password = make_password(password)
                new_admin.save()

                # Obtener el ID del usuario en sesión
                usuario = self.request.user

                # Crear entrada en HistorialAdmin para el usuario editado
                historial_entry = HistorialAdmin.objects.create(
                    id_user=new_admin.id,
                    username=new_admin.username,
                    email=new_admin.email,
                    h_user_proc=usuario,
                    h_fch_creacion=new_admin.date_joined,
                    h_tipo_proc='U',
                )

                # Obtener el registro anterior del usuario antes de la edición
                #usuario_anterior = HistorialAdmin.objects.filter(id_user=new_admin.id).exclude(h_id_user=historial_entry.h_id_user).order_by('-h_fch_creacion').first()
                #print("Registro anterior del usuario: " + str(usuario_anterior))

                #usuario_anterior.h_fch_modificacion = timezone.now()  # Actualizar la fecha de modificación del registro anterior
                #usuario_anterior.save()  # Guardar los cambios

                

                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, 'Error en el servidor')
            return JsonResponse({'mensaje': 'Error en el servidor', 'error': str(e)}, status=500)

    def form_invalid(self, form):
        mensaje = 'No se ha podido editar el Registro'
        error = form.errors
        return JsonResponse({'mensaje': mensaje, 'error': error}, status=400)

    def get_success_url(self):
        return reverse('list_admins')
     

class DeleteAdmin(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'del_admin.html'
    success_url = reverse_lazy('list_admins')
    success_message = 'Registro Eliminado Correctamente'
    permission_required = "auth.delete_user"
    login_url = 'index' 

    def handle_no_permission(self):
        messages.error(self.request, 'Acceso Denegado!!!')
        return redirect('list_admins')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    

    def post(self, request, *args, **kwargs):
        
        try:
            # Recuperar el objeto antes de eliminarlo
            user = self.get_object()

            usuario = self.request.user

            # Guardar los atributos del usuario antes de eliminarlo
            id_user = user.id  
            username = user.username
            email = user.email
            date_joined = user.date_joined
            

            # Crear entrada en HistorialAdmin antes de eliminar el usuario
            historial_entry = HistorialAdmin.objects.create(
                id_user=id_user,
                username=username,
                email=email,
                h_user_proc=usuario,
                h_fch_creacion=date_joined,
                h_tipo_proc='D',
            )

            # Obtener el registro anterior del usuario antes de la edición
            #usuario_anterior = HistorialAdmin.objects.filter(id_user=user.id).exclude(h_id_user=historial_entry.h_id_user).order_by('-h_fch_creacion').first()
            #print("Registro anterior del usuario: " + str(usuario_anterior))

            #if usuario_anterior:
                #usuario_anterior.h_fch_modificacion = timezone.now()  # Actualizar la fecha de modificación del registro anterior
                #usuario_anterior.save()  # Guardar los cambios

            # Eliminar el usuario
            user.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_admins')


class ListAdminHistorial(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=HistorialAdmin
        template_name='adminHist.html'
        context_object_name='administradoresHist' 
        permission_required = "auth.view_historialadmin"
        login_url = 'index' 

        def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('index')

        def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
 
    
class reset_axe(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
   
    success_message = 'Registro editado correctamente'
    template_name = "admin.html"
    
    success_url=reverse_lazy('list_admins')
    permission_required = "auth.change_user"
    login_url = 'index' 
 
    


    def handle_no_permission(self):
            messages.error(self.request, 'Acceso Denegado!!!')
            return redirect('list_admins')

    def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            
            return super().dispatch(request, *args, **kwargs)
    


    def get(self, request, pk, *args, **kwargs):
        
        user=User.objects.get(pk=pk)
        
        reset(username=user.username)
        messages.success(self.request, 'Usuario Desbloqueado')
        #return render(request, 'admin.html', {"mensaje": mensaje})
        
        return redirect(reverse_lazy('list_admins'))
        

 