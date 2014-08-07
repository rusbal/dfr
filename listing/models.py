from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


class Developer(models.Model):
    name = models.CharField('Developer', max_length=50)
    about = RichTextField(blank=True, null=True) 
    
    panels = [
        FieldPanel('name', classname="full title"),
        FieldPanel('about', classname="full"),
    ]

    def __str__(self):
        return self.name

register_snippet(Developer)


class HouseModelPage(Page):
    developer = models.ForeignKey('Developer', max_length=50, blank=True, null=True)
    series = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50)
    description = RichTextField() 

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    indexed_fields = ('description', )

HouseModelPage.content_panels = [
    FieldPanel('title', classname="full title"),
    MultiFieldPanel((FieldPanel('developer'),
                     FieldPanel('series'), 
                     FieldPanel('model'),
                     FieldPanel('description'),
                     ImageChooserPanel('image'),
                    ), "Model"),
]

HouseModelPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
]


class PropertyPage(Page):
    property_owner = models.ForeignKey('seller.Owner', blank=True, null=True)
    description = RichTextField() 
    block = models.PositiveSmallIntegerField(blank=True, null=True)
    lot = models.PositiveSmallIntegerField(blank=True, null=True)
    lot_area = models.DecimalField(max_digits=12, decimal_places=2)
    floor_area = models.DecimalField(max_digits=12, decimal_places=2)
    tcp = models.DecimalField("Total Contract Price", max_digits=12, decimal_places=2)
    reservation_fee = models.DecimalField(max_digits=12, decimal_places=2) 
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ), 
    model = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    indexed_fields = ('description', )

PropertyPage.content_panels = [
    FieldPanel('title', classname="full title"),
    PageChooserPanel('model', 'dfr.HouseModelPage'),
    MultiFieldPanel((FieldPanel('property_owner'),
                     FieldPanel('description'),
                     ImageChooserPanel('image'),
                    ), "Model"),
    MultiFieldPanel((FieldPanel('block'),
                     FieldPanel('lot'),
                     FieldPanel('lot_area'),
                     FieldPanel('floor_area'),
                    ), "Location / Area"),
    MultiFieldPanel((FieldPanel('tcp'),
                     FieldPanel('reservation_fee'),
                    ), "Price"),
]

PropertyPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
]
