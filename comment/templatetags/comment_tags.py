from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm


register = template.Library()


@register.simple_tag(name='get_model_name')
def get_model_name(obj):
    """ returns the model name of an object """
    return type(obj).__name__


@register.simple_tag(name='get_app_name')
def get_app_name(obj):
    """ returns the app name of an object """
    return type(obj)._meta.app_label


@register.simple_tag(name='comment_count')
def comment_count(obj):
    """ returns the count of comments of an object """
    model_object = type(obj).objects.get(id=obj.id)
    return model_object.comments.all().count()


@register.simple_tag(name='profile_url')
def profile_url(obj, profile_app_name, profile_model_name):
    """ returns profile url of user """
    try:
        content_type = ContentType.objects.get(
                            app_label=profile_app_name,
                            model=profile_model_name.lower()
                        )
        profile = content_type.get_object_for_this_type(user=obj.user)
        return profile.get_absolute_url()
    except ContentType.DoesNotExist:
        return ""


@register.simple_tag(name='img_url')
def img_url(obj, profile_app_name, profile_model_name):
    """ returns url of profile image of a user """
    try:
        content_type = ContentType.objects.get(
                            app_label=profile_app_name,
                            model=profile_model_name.lower()
                        )
    except ContentType.DoesNotExist:
        return ""
    Profile = content_type.model_class()
    fields = Profile._meta.get_fields()
    profile = content_type.model_class().objects.get(user=obj.user)
    for field in fields:
        if hasattr(field, "upload_to"):
            return field.value_from_object(profile).url


def get_comments(obj, user, oauth=False, profile_app_name=None, profile_model_name=None):
    """
    Retrieves list of comments related to a certain object and renders
    The appropriate template to view it
    """
    model_object = type(obj).objects.get(id=obj.id)
    comments = Comment.objects.filter_by_object(model_object)

    return {
        "commentform": CommentForm(),
        "model_object": obj,
        "user": user,
        "comments": comments,
        "comments_count": comments.count(),
        "oauth": oauth,
        "profile_app_name": profile_app_name,
        "profile_model_name": profile_model_name,
    }

register.inclusion_tag('comment/base.html')(get_comments)


def comment_form(obj, user):
    """
    renders template of comment form
    """
    return {
        "commentform": CommentForm(),
        "model_object": obj,
        "user": user,
    }

register.inclusion_tag('comment/commentform.html')(comment_form)


def include_static():
    """ include static files """
    return

register.inclusion_tag('comment/static.html')(include_static)

def include_bootstrap():
    """ include static files """
    return

register.inclusion_tag('comment/bootstrap.html')(include_bootstrap)