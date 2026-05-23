"""
Vistas de la aplicación 'accounts'.
Autenticación (login, logout) y gestión de usuarios administradores.
Solo el super-admin puede crear administradores y cambiar contraseñas.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, CrearAdminForm, CambiarPasswordForm
from .decorators import super_admin_required


def login_view(request):
    """
    Vista de inicio de sesión.
    Autentica al usuario con correo electrónico y contraseña.
    Si el usuario ya está autenticado, redirige al dashboard.
    """
    if request.user.is_authenticated:
        return redirect('metrics:dashboard')
    
    form = LoginForm(request, data=request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            usuario = form.get_user()
            auth_login(request, usuario)
            messages.success(request, f'¡Bienvenido, {usuario.email}! Ha iniciado sesión correctamente.')
            
            # Redirigir a la página que intentaba visitar, o al dashboard
            next_url = request.GET.get('next', 'metrics:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Credenciales incorrectas. Verifique su correo y contraseña.')
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    email = request.user.email
    auth_logout(request)
    messages.info(request, f'Sesión de {email} cerrada correctamente.')
    return redirect('accounts:login')


@login_required
@super_admin_required
def crear_admin(request):
    """
    Panel exclusivo del super-admin para crear cuentas de administrador.
    """
    form = CrearAdminForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            nuevo_admin = form.save()
            messages.success(
                request,
                f'Administrador {nuevo_admin.email} creado exitosamente. Ya puede iniciar sesión.'
            )
            return redirect('accounts:crear_admin')
        else:
            messages.error(request, 'Error al crear el administrador. Revise los datos ingresados.')
    
    # Listar administradores existentes
    admins = Usuario.objects.filter(rol='admin').order_by('-date_joined')
    return render(request, 'accounts/crear_admin.html', {
        'form': form,
        'admins': admins,
    })


@login_required
@super_admin_required
def cambiar_password(request):
    """
    Panel exclusivo del super-admin para cambiar la contraseña de un administrador.
    """
    form = CambiarPasswordForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            nueva_password = form.cleaned_data['nueva_password']
            usuario.set_password(nueva_password)
            usuario.save()
            messages.success(
                request,
                f'Contraseña de {usuario.email} actualizada exitosamente.'
            )
            return redirect('accounts:cambiar_password')
        else:
            messages.error(request, 'Error al cambiar la contraseña. Revise los datos.')
    
    return render(request, 'accounts/cambiar_password.html', {'form': form})


def permiso_denegado(request):
    """
    Página de error cuando un usuario intenta acceder a una sección sin permisos.
    """
    return render(request, 'accounts/permiso_denegado.html', status=403)


# Importación al final para evitar referencia circular
from .models import Usuario

# ---- Registro de usuarios (público) ----
from django import forms as django_forms
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegistroForm(django_forms.ModelForm):
    """Formulario público de registro. Define password1/password2 y widgets con clases del sistema."""
    password1 = django_forms.CharField(
        label='Contraseña',
        widget=django_forms.PasswordInput(attrs={'class': 'dark-input', 'placeholder': 'Mínimo 8 caracteres'})
    )
    password2 = django_forms.CharField(
        label='Confirmar contraseña',
        widget=django_forms.PasswordInput(attrs={'class': 'dark-input', 'placeholder': 'Repita la contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email']
        widgets = {
            'username': django_forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Nombre de usuario'}),
            'email': django_forms.EmailInput(attrs={'class': 'dark-input', 'placeholder': 'correo@ejemplo.com'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise django_forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise django_forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password1'])
        # Asignar rol por defecto 'user' si existe la enumeración
        try:
            usuario.rol = Usuario.Rol.USER
        except Exception:
            usuario.rol = 'user'
        if commit:
            usuario.save()
        return usuario


class RegistrarUsuarioView(CreateView):
    """Vista pública para registrar nuevos usuarios.

    Redirige al login tras el registro y muestra un mensaje flash.
    """
    model = Usuario
    form_class = RegistroForm
    template_name = 'accounts/registro.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        # Si ya está autenticado, no permitir registro público
        if request.user.is_authenticated:
            messages.info(request, 'Ya has iniciado sesión.')
            return redirect('metrics:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada correctamente. Ahora puedes iniciar sesión.')
        return response
