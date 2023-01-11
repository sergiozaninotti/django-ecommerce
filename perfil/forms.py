from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)  # excluindo usuário para ele não ter opção de selecionar um user


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,  # muda o tipo do campo no frontend
        widget=forms.PasswordInput(),  # coloca o input type como password no front
        label='Senha',
    )

    password_confirm = forms.CharField(
        required=False,  # muda o tipo do campo no frontend
        widget=forms.PasswordInput(),  # coloca o input type como password no front
        label='Confirme a senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password_confirm', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        error_msgs = {}

        user_name = cleaned.get('username')
        user_email = cleaned.get('email')
        user_password = cleaned.get('password')
        password_confirm = cleaned.get('password_confirm')
        usuario_db = User.objects.filter(username=user_name).first()
        email_db = User.objects.filter(email=user_email).first()

        error_msgs_user_exists = 'Usuário já existe'
        error_msgs_email_exists = 'E-mail já existe'
        error_msgs_password_match = 'As senhas não conferem!'
        error_msgs_password_short = 'Sua senha precisa de pelo menos 6 caracteres!'
        error_msgs_required_field = 'ESte campo é obrigatório!'

        # print(data) mostra os dados no terminal

        # Usuários logados: atualização
        if self.usuario:

            if usuario_db:
                if user_name != usuario_db.username:
                    error_msgs['username'] = error_msgs_user_exists

            if email_db:
                if user_email != email_db.email:
                    error_msgs['email'] = error_msgs_email_exists

            if user_password:
                if user_password != password_confirm:
                    error_msgs['password'] = error_msgs_password_match
                    error_msgs['password_confirm'] = error_msgs_password_match

                if len(user_password) < 6:
                    error_msgs['password'] = error_msgs_password_short

        # Usuários não logados: cadastro
        else:
            if usuario_db:  #só com este if já verifica o post com o que tem cadastrado no db
                error_msgs['username'] = error_msgs_user_exists

                if email_db:
                    error_msgs['email'] = error_msgs_email_exists

                if not user_password:
                    error_msgs['password'] = error_msgs_required_field

                    if not password_confirm:
                        error_msgs['password'] = error_msgs_required_field

                if user_password != password_confirm:
                    error_msgs['password'] = error_msgs_password_match
                    error_msgs['password_confirm'] = error_msgs_password_match

                if len(user_password) < 6:
                    error_msgs['password'] = error_msgs_password_short

        if error_msgs:
            raise (forms.ValidationError(error_msgs))
