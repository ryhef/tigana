from django import forms

class InquiryForm(forms.Form):
    customer_first_name = forms.CharField(label="First Name")
    customer_last_name = forms.CharField(label="Last Name")
    customer_email = forms.EmailField(label="Email")
    customer_phone = forms.CharField(label="Phone")
    question = forms.CharField(label="Question",widget=forms.Textarea)
    PHONE = 'Phone'
    EMAIL = 'Email'
    CONTACT_METHOD = [(PHONE,'Phone'),(EMAIL,'Email')]
    prefered_contact_method = forms.ChoiceField(choices=CONTACT_METHOD)
    