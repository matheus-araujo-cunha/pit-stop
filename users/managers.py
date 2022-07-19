from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_args):
        if not email:
            raise ValueError("The given email must be set")

        if extra_args.get("name", False):
            extra_args["name"] = extra_args["name"].title()

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_args)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, email, password, **extra_args):
        extra_args.setdefault("is_staff", False)
        extra_args.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_args)

    def create_superuser(self, email, password, **extra_args):
        extra_args.setdefault("is_staff", True)
        extra_args.setdefault("is_superuser", True)

        return self._create_user(email, password, **extra_args)
