from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AdminForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False)
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:  # Nuevo usuario, campo de nombre de usuario editable
            self.fields['username'].widget.attrs.pop('readonly', None)
        else:  # Usuario existente, campo de nombre de usuario de solo lectura
            self.fields['username'].widget.attrs.update({
                'readonly': True,
            })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username',
            'id': 'username',
            'title': 'Usuario',
            'style': 'width: 100%',
            'autofocus': True,
        })

        self.fields["password"].widget.attrs.update({
            'class': "form-control",
            'name': "password",
            'id': "password",
            'title': "Contraseña",
            'style': "width: 100%",
        })

        self.fields["email"].widget.attrs.update({
            'class': "form-control",
            'name': "email",
            'id': "email",
            'title': "Email",
            'style': "width: 100%",
        })

        self.fields["is_active"].widget.attrs.update({
            'class': "form-check-input",
            'name': "is_active",
            'id': "is_active",
            'title': "Activo",
        })

        
        self.fields["password_confirm"].widget.attrs.update({
            'class': "form-control",
            'name': "password_confirm",
            'id': "password_confirm",
            'title': "Confirmar Contraseña",
            'style': "width: 100%",
        })

    def clean_is_active(self):
        return self.cleaned_data.get('is_active', False)
    
    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        
        usuario = cleaned_data.get("username")
        contra = cleaned_data.get("password")
        email = cleaned_data.get("email")
        password_confirm = cleaned_data.get('password_confirm')

        if not usuario:
            raise forms.ValidationError('Ingrese usuario de la persona')

        if not contra:
            raise forms.ValidationError('Ingrese contraseña de la persona')
        
        if not password_confirm:
            raise forms.ValidationError('Ingrese confirmación de contraseña de la persona')

        if not email:
            raise forms.ValidationError('Ingrese email de la persona')

        # Verificar si el usuario ya existe
        if self.instance.pk:
            if User.objects.filter(username=usuario).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Cambio no permitido, persona existente')

        # Verificar si el correo electrónico ya está en uso
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")

        # Verificar si ambas contraseñas tienen valores y son diferentes
        if contra and password_confirm and contra != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data

    def clean_username(self):
        return self.cleaned_data['username'].title()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password == username:
            raise forms.ValidationError('La contraseña es igual al usuario.')
        

        # Verificar si ambas contraseñas tienen valores y son diferentes
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
    

        # Verificar longitud de la contraseña
        if len(password) < 8:
            raise forms.ValidationError('La contraseña es demasiado corta. Debe contener al menos 8 caracteres.')

        # Verificar si la contraseña es común (puedes personalizar la lista según tus necesidades)
        common_passwords = ['password', '12345678']
        if password.lower() in common_passwords:
            raise forms.ValidationError('La contraseña tiene un valor demasiado común.')

        return password

    def clean_email(self):
        return self.cleaned_data['email']
    
    def clean_estado(self):
        return self.cleaned_data['id_active']
