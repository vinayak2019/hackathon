from django import forms


class CreateDBForm(forms.Form):
    SCHEMA = (("compchem", "Compchem"),
                 ('qm9_v1', "QM9 v1"),
                 ('qm9_v2', "QM9 v2"))
    database_schema = forms.ChoiceField(required=True, choices=SCHEMA)
    database_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['database_schema', 'database_name', 'email', 'full_name', 'password']


class LoginForm(forms.Form):
    database = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['database', 'email', 'password']
