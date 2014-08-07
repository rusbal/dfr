from django.db import models

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel


class Address(models.Model): 
    REGION_CHOICES = (
        (14, 'National Capital Region (NCR)'),
        (1, 'Ilocos Region (Region I)'),
        (15, 'Cordillera Administrative Region (CAR)'),
        (2, 'Cagayan Valley (Region II)'),
        (3, 'Central Luzon (Region III)'),
        (41, 'CALABARZON (Region IV-A)'),
        (42, 'MIMAROPA (Region IV-B)'),
        (5, 'Bicol Region (Region V)'),
        (6, 'Western Visayas (Region VI)'),
        (7, 'Central Visayas (Region VII)'),
        (8, 'Eastern Visayas (Region VIII)'),
        (9, 'Zamboanga Peninsula (Region IX)'),
        (10, 'Northern Mindanao (Region X)'),
        (11, 'Davao Region (Region XI)'),
        (12, 'SOCCSKSARGEN (Region XII)'),
        (13, 'Caraga (Region XIII)'),
        (16, 'Autonomous Region in Muslim Mindanao (ARMM)'),
    ) 

    barangay = models.CharField(max_length=50, blank=True, null=True)
    block = models.PositiveSmallIntegerField(blank=True, null=True)
    lot = models.PositiveSmallIntegerField(blank=True, null=True)
    municipality = models.CharField('Municipality/City', max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    purok = models.CharField(max_length=50, blank=True, null=True)
    region = models.PositiveSmallIntegerField(choices=REGION_CHOICES) 
    sitio = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)

    panels = [
        MultiFieldPanel((
                FieldPanel('block'),
                FieldPanel('lot'),
                FieldPanel('street'),
                FieldPanel('purok'),
                FieldPanel('sitio'),
                FieldPanel('barangay'),
                FieldPanel('municipality'),
                FieldPanel('province'),
                FieldPanel('region'),
            ), "Address"
        ),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        addr = []
        if self.block and self.lot:
            addr.append("Blk %s" % self.block)
            addr.append("Lot %s" % self.lot)
        elif self.lot:
            addr.append("No. %s" % self.lot)

        if self.street:
            addr.append(self.street)
        if self.barangay:
            addr.append(self.barangay)
        if self.municipality:
            addr.append(self.municipality)
        if self.province:
            addr.append(self.province)
        return ', '.join(addr)
