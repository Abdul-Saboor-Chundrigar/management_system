from django.core.mail.backends.smtp import EmailBackend
from .models import PosteIOConfig

class PosteIOEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        config = PosteIOConfig.objects.first()
        if not config:
            raise ValueError("Poste.io configuration not set.")
        super().__init__(
            host=config.smtp_host,
            port=config.smtp_port,
            username=config.smtp_username,
            password=config.smtp_password,
            use_tls=config.smtp_use_tls,
            fail_silently=False,
            *args,
            **kwargs
        )
        self.default_from_email = config.default_from_email
