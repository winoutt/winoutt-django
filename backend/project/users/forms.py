from django.forms import Form, ModelForm, BooleanField, CharField, ValidationError
from .models import Setting, User


class UserSettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = ('is_dark_mode', 'enabled_notification')


class PasswordChangeForm(ModelForm):
    current_password = CharField(required=True, min_length=6)
    new_password = CharField(required=True, min_length=6)

    class Meta:
        model = User
        fields = ('current_password', 'new_password')
    
    def clean(self):
        user = self.instance
        current_password = self.cleaned_data.get('current_password', None)
        new_password = self.cleaned_data.get('new_password', None)
        if not user.check_password(current_password):
            raise ValidationError('Invalid current password.')
        elif current_password == new_password:
            raise ValidationError('New password can\'t be same as the current password.')

    
    def save(self, commit=True):
        user = super(PasswordChangeForm, self).save(commit=commit)
        new_password = self.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return user