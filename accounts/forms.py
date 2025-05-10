from django import forms
from django.contrib.auth import get_user_model
from printers.utils import get_cups_printers

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    personal_printer = forms.ChoiceField(
        label="Stampante personale",
        required=False,
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        printers = get_cups_printers()
        self.fields['personal_printer'].choices = [('', '--- Nessuna ---')] + [(p, p) for p in printers]

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'theme', 'personal_printer']
