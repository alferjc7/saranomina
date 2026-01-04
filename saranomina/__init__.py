from django import forms

_original_init = forms.ModelForm.__init__

def patched_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)

    for field in self.fields.values():

        if isinstance(field.widget, forms.Select):
            if hasattr(field, 'empty_label'):
                field.empty_label = '— Seleccione —'

        if hasattr(field, 'choices'):
            choices = list(field.choices)

            if choices and choices[0][0] in ('', None):
                choices[0] = ('', '— Seleccione —')
                field.choices = choices

forms.ModelForm.__init__ = patched_init