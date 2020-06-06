from django import forms

# Users can specify quantity of items in this range.
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range (1,21)]

class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)

    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
