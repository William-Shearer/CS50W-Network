from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "User Name", max_length = 50, required = True, widget = forms.TextInput(attrs={"autofocus": True, "style": "text-align: center;"}))
    password = forms.CharField(label = "Password", max_length = 50, required = True, widget = forms.PasswordInput(attrs={"style": "text-align: center;"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label = "User Name", max_length = 50, required = True, widget = forms.TextInput(attrs={"autofocus": True, "style": "text-align: center;"}))
    first_name = forms.CharField(label = "First Name (optional)", max_length = 50, required = False, widget = forms.TextInput(attrs={"style": "text-align: center;"}))
    last_name = forms.CharField(label = "Last Name (optional)", max_length = 50, required = False, widget = forms.TextInput(attrs={"style": "text-align: center;"}))
    email = forms.EmailField(label = "Email", required = True, widget = forms.EmailInput(attrs={"style": "text-align: center;"}))
    userimage = forms.ImageField(label = "User Image", required = False)
    biography = forms.CharField(label = "Biography (optional)", required = False, widget = forms.Textarea())
    password = forms.CharField(label = "Password", min_length = 5, max_length = 50, required = True, widget = forms.PasswordInput(attrs={"style": "text-align: center;"}))
    confirmation = forms.CharField(label = "Confirm Password", min_length = 5, max_length = 50, required = True, widget = forms.PasswordInput(attrs={"style": "text-align: center;"}))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label = "New Password", min_length = 5, max_length = 50, required = True, widget = forms.PasswordInput(attrs={"autofocus": True, "style": "text-align: center;"}))
    confirmation = forms.CharField(label = "Confirm Password", min_length = 5, max_length = 50, required = True, widget = forms.PasswordInput(attrs={"style": "text-align: center;"}))


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label = "First Name", max_length = 50, required = False, widget = forms.TextInput(attrs={"autofocus": True, "style": "text-align: center;"}))
    last_name = forms.CharField(label = "Last Name", max_length = 50, required = False, widget = forms.TextInput(attrs={"style": "text-align: center;"}))
    email = forms.EmailField(label = "Email", required = True, widget = forms.EmailInput(attrs={"style": "text-align: center;"}))
    biography = forms.CharField(label = "Biography", required = False, widget = forms.Textarea())


class PostForm(forms.Form):
    subject = forms.CharField(label = "Subject", max_length = 50, required = True, widget = forms.TextInput(attrs={"autofocus": True}))
    content = forms.CharField(label = "Message", required = True, widget = forms.Textarea())


class EditPostForm(forms.Form):
    content = forms.CharField(label = "Content", required = True, widget = forms.Textarea())
