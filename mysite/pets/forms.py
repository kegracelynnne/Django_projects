from django.forms import ModelForm
from pets.models import Type


# Create the form class.
class TypeForm(ModelForm):
    class Meta:
        model = Type    # Model form
        fields = '__all__'