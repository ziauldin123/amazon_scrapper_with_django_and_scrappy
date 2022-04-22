from django.db import models
from django.utils import timezone
from PIL import Image
import os
from urllib import request
import boto3
from django.conf import settings
from django.core.files import File


class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
    title = models.TextField(blank=True)
    contents = models.TextField(blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)
    recommends = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100, null=True)


class Product(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    market = models.CharField(max_length=3,verbose_name="Market")
    amazon_url = models.URLField()
    asin = models.CharField(max_length=50)
    product_name = models.CharField(max_length=500)
    list_price = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    currency_symbol = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=19, decimal_places=2,null=True, blank=True )
    save_price = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    save_in_percentage = models.IntegerField(null=True, blank=True)
    main_image = models.URLField()
    coupon = models.BooleanField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    ratings_total = models.PositiveIntegerField(default=0, null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True)
    is_prime = models.BooleanField()
    is_unqualify = models.NullBooleanField(default=None,null=True, blank=True)
    affiliate_link = models.URLField()
    number_of_calls_get_deal = models.PositiveIntegerField(default=0,verbose_name="No. Get deal")
    create_product_date = models.DateTimeField(default=timezone.now)
    update_product_date = models.DateTimeField(default=timezone.now)
    is_new = models.NullBooleanField(default=True,null=True, blank=True,verbose_name='New Product')
    is_sold_by_amazon = models.NullBooleanField(default=True,null=True, blank=True,verbose_name='Amazon Price')
    is_sold_by_third_party = models.NullBooleanField(default=None,null=True, blank=True,verbose_name='3rd Party Price')


    updated = models.BooleanField(default=False)
    update_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    import_type = models.CharField(max_length=50, default="Manual")

    def __str__(self):
        return self.asin
        # return "{}".format(self.asin)

    def alt_images_text(self):
        pr_name=self.product_name[:70].translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        return f''+pr_name.replace('   ', ' ').replace('  ', ' ')

    def human_readable_title(self):
        pr_name=self.product_name[:50].translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        return f''+pr_name.replace("'", '').replace(' ', '-').replace('-–-', '-').replace('---', '-').replace('--', '-')
        # return f''+self.product_name[:50].replace(' ', '-').replace(',','').replace('.-','-').replace('/','-').replace('&','').replace('|','').replace('(','').replace(')','').replace('---','-').replace('--','-')

    def get_absolute_url(self):
        return f'product/id={self.pk}'

