from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsnippets.models import register_snippet

from common.models import Address


class Owner(Address):
    CLASSIFICATION_CHOICES = (
        (1, 'Individual'),
        (2, 'Dealer'),
    )

    first_name = models.CharField(max_length=25, blank=True, null=True)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    classification = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICES) 
    about = RichTextField(blank=True, null=True) 

    panels = [
        MultiFieldPanel((FieldPanel('first_name'),
                         FieldPanel('middle_name'),
                         FieldPanel('last_name'),
                         FieldPanel('classification', classname='full'),
                         FieldPanel('about', classname='full'),
                        ), "Owner Information"),
        MultiFieldPanel((FieldPanel('block'),
                         FieldPanel('lot'),
                         FieldPanel('street'),
                         FieldPanel('purok'),
                         FieldPanel('sitio'),
                         FieldPanel('barangay'),
                         FieldPanel('municipality'),
                         FieldPanel('province'),
                         FieldPanel('region'),
                        ), "Address"),
    ]

    def __str__(self):
        full_name = []
        if self.first_name:
            full_name.append(self.first_name)
        if self.middle_name:
            full_name.append(self.middle_name[:1] + '.')
        if self.last_name:
            full_name.append(self.last_name)
        return ' '.join(full_name)

register_snippet(Owner)
