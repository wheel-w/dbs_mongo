from django.utils.module_loading import import_string

UserBackend = import_string("django.contrib.auth.backends.ModelBackend")
