from django import forms
from app.models import Combi


def get_error_dict(errors):
    error_dict = {}
    for field_name, errors in errors.items():
        error_dict[field_name] = []
        for error in errors:
            error_dict[field_name].append(error)
    return error_dict


class CombiCreateAPIForm(forms.ModelForm):
    """
    作成フォーム
    officeはget_or_create()を用いるためfieldsに含めず
    """

    def clean_office(self):
        return self.data.get('office')

    class Meta:
        model = Combi
        fields = ('name',)
