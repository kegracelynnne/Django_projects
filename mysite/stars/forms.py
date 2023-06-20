from django.forms import ModelForm
from stars.models import Type


# Create the form class.
class TypeForm(ModelForm):
    class Meta:
        model = Type    # Model form
        fields = '__all__'