    
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Import models inside the function to avoid AppRegistryNotReady error
    from .models import Post  # Ensure your Post model is imported

    try:
        # Create the Reader group if it doesn't exist
        reader_group, _ = Group.objects.get_or_create(name='Readers')
        # Assign read permission to Reader group
        reader_permission = Permission.objects.get(codename='view_post')
        reader_group.permissions.set([reader_permission])

        # Create the Author group if it doesn't exist
        author_group, _ = Group.objects.get_or_create(name='Authors')
        # Assign permissions to Author group
        author_permissions = [
            Permission.objects.get(codename='add_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
        ]
        author_group.permissions.set(author_permissions)

        # Create the Editor group if it doesn't exist
        editor_group, _ = Group.objects.get_or_create(name='Editors')
        # Assign permissions to Editor group
        editor_permissions = [
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='can_publish'),  # Ensure this permission exists
        ]
        editor_group.permissions.set(editor_permissions)

        print("Groups and permissions created successfully.")
    except ObjectDoesNotExist as a:
        print("One or more permissions do not exist.", a)
    except Exception as e:
        print(f"An error occurred: {e}")