__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
import uuid
from popit.models.exception import PopItFieldNotExist


# Yay Popolo+!

# This is the source,
# This is potentially a json field. See if it is acceptable to lump together sources of different language together.
# If it is a json field, since we are using postgres, we can potentially save us from performance issue
class Link(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("label"))
    # This is our plus stuff, for citation
    field = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("field"))
    url = models.URLField(verbose_name=_("url"))
    translation = TranslatedFields(
        note = models.TextField(verbose_name=_("note"), blank=True, null=True)
    )
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super(Link, self).save(*args, **kwargs)

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        link = Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def __unicode__(self):
        return self.url

class Contact(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    translation = TranslatedFields(
        label = models.CharField(max_length=255, verbose_name=_("label"), null=True, blank=True), # hopefully people won't be searching via label :-/
        note = models.TextField(verbose_name=_("note"), blank=True, null=True)
    )
    type = models.CharField(max_length=255, verbose_name=_("type"))
    value = models.CharField(max_length=255, verbose_name=_("value"))
    valid_from = models.DateField(null=True, blank=True, verbose_name=_("valid from"))
    valid_until = models.DateField(null=True, blank=True, verbose_name=_("valid until"))
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    links = GenericRelation(Link)
    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super(Contact, self).save(*args, **kwargs)

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        link = Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def citation_exist(self, field):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        links = self.links.language(self.language_code).filter(field=field)
        if links:
            return True
        return False

    def __unicode__(self):
        return "%s:%s" % (self.type, self.value)


class Identifier(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    translations = TranslatedFields(
        scheme = models.CharField(max_length=255, verbose_name=_("scheme")) # This is not actually skim in Malay fyi
    )

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    links = GenericRelation(Link)

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super(Identifier, self).save(*args, **kwargs)

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        link = Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def citation_exist(self, field):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        links = self.links.language(self.language_code).filter(field=field)
        if links:
            return True
        return False

    def __unicode__(self):
        return "%s:%s" % (self.safe_translation_getter('scheme', ""), self.identifier)


# In media, only translated name is used not name in original language
# unless name uses a different character than in original language :-/
class OtherName(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255, verbose_name=_("name")),
         # We don't always get the name of the fllowing field
        family_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("family name")),
        given_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("given name")),
        additional_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("additional name")),
        # Not everyone a datuk/datin/etc
        honorific_prefix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific prefix")),
        # Datuk someone, and that's it.
        honorific_suffix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific suffix")),
        patronymic_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("patronymmic name")),
    )
    start_date = models.CharField(max_length=20, null=True, blank=True) # Sometime we have no idea
    end_date = models.CharField(max_length=20, null=True, blank=True)

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    links = GenericRelation(Link)

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super(OtherName, self).save(*args, **kwargs)

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)

        link = Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def citation_exist(self, field):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        links = self.links.language(self.language_code).filter(field=field)
        if links:
            return True
        return False

    def __unicode__(self):
        return self.safe_translation_getter('name')
