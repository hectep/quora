from django_registration.forms import RegistrationForm

from profiles.models import Profile


class ProfileForm(RegistrationForm):
    """
    A standard user form.
    """

    class Meta(RegistrationForm.Meta):
        model = Profile
