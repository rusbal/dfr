from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalKey 


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


class ImageFields(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    panels = [
        ImageChooserPanel('image'),
    ]

    class Meta:
        abstract = True


class HouseModelRelatedImage(Orderable, ImageFields):
    page = ParentalKey('listing.HouseModelPage', related_name='images')


class HouseModelPage(Page):
    developer = models.ForeignKey('Developer', max_length=50, blank=True, null=True)
    series = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50)
    description = RichTextField() 

    indexed_fields = ('description', )

HouseModelPage.content_panels = [
    FieldPanel('title', classname="full title"),
    MultiFieldPanel((FieldPanel('developer'),
                     FieldPanel('series'), 
                     FieldPanel('model'),
                     FieldPanel('description'),
                    ), "Model"),
    InlinePanel(HouseModelPage, 'images', label="Images"),
]

HouseModelPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
]


class PropertyRelatedImage(Orderable, ImageFields):
    page = ParentalKey('listing.PropertyPage', related_name='images')


class PropertyPage(Page):
    model = models.ForeignKey(
        'listing.HouseModelPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    property_owner = models.ForeignKey('seller.Owner', blank=True, null=True)
    description = RichTextField() 

    block = models.PositiveSmallIntegerField(blank=True, null=True)
    lot = models.PositiveSmallIntegerField(blank=True, null=True)
    lot_area = models.DecimalField(max_digits=12, decimal_places=2)
    floor_area = models.DecimalField(max_digits=12, decimal_places=2)

    tcp = models.DecimalField("Total Contract Price", max_digits=12, decimal_places=2)
    reservation_fee = models.DecimalField(max_digits=12, decimal_places=2) 

    indexed_fields = ('description', )

PropertyPage.content_panels = [
    FieldPanel('title', classname="full title"),
    MultiFieldPanel((FieldPanel('model'),
                     FieldPanel('property_owner'),
                     FieldPanel('description'),
                    ), "Model"),
    MultiFieldPanel((FieldPanel('block'),
                     FieldPanel('lot'),
                     FieldPanel('lot_area'),
                     FieldPanel('floor_area'),
                    ), "Location / Area"),
    MultiFieldPanel((FieldPanel('tcp'),
                     FieldPanel('reservation_fee'),
                    ), "Price"),
    InlinePanel(PropertyPage, 'images', label="Images"),
]

PropertyPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
]
