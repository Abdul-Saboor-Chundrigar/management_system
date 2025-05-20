from django.core.mail.backends.smtp import EmailBackend
from .models import EmailRelayConfig

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        config = EmailRelayConfig.objects.first()
        if not config:
            raise ValueError("Email relay configuration not set.")
        super().__init__(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
            use_tls=config.use_tls,
            fail_silently=False,
            *args,
            **kwargs
        )
        self.default_from_email = config.default_from_email
