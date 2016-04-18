import pytest


@pytest.fixture
def user_pw():
    return "super pw"


@pytest.fixture
def user(user_pw):
    from photos.users.models import User
    return User.objects.create_user(
        username="ron",
        email="dumbledore@example.com",
        password=user_pw
    )


@pytest.fixture
def superuser(user_pw):
    from photos.users.models import User
    return User.objects.create_superuser(
        username="dumbledore",
        email="dumbledore@example.com",
        password=user_pw
    )


@pytest.fixture
def create_photo():
    from photos.gallery.models import Photo

    def inner_create_photo(**kwargs):
        kwargs.update(dict(
            file="photos/test.jpg",
            slug="snowing",
            taken_at=None,
            title="Snowing",
        ))
        return Photo.objects.create(**kwargs)

    return inner_create_photo


@pytest.fixture
def photo(create_photo, user):
    return create_photo(user=user)
