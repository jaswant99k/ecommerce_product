from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


def get_category_image_filepath(self, filename):
    return "category/" + str(self.pk) + "/category.png"


def get_category_image():
    return "upload/category/default_category_image.png"


def get_category_icon_image_filepath(self, filename):
    return "upload/category/" + str(self.pk) + "/category_icon.png"


def get_category_icon_image():
    return "upload/category/default_category_icon_image.png"


class CategoryManager(models.Manager):
    def all(self):
        return self.filter(is_active=True)

    def parent_categories(self):
        return self.filter(is_active=True).filter(parent_id__isnull=True)

    def mega_menu(self):
        return self.filter(is_active=True).filter(is_mega=True)[:4]


class Category(models.Model):
    name = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    image = models.ImageField(
        max_length=255,
        upload_to=get_category_image_filepath,
        null=True,
        blank=True,
        default=get_category_image,
    )
    icon = models.ImageField(
        max_length=255,
        upload_to=get_category_icon_image_filepath,
        null=True,
        blank=True,
        default=get_category_icon_image,
    )
    parent_id = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )
    slug = models.SlugField(blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_banner = models.BooleanField(default=False)
    is_mega = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="updated_date", auto_now=True)

    objects = CategoryManager()

    def get_category_image_filename(self):
        return str(self.image)[
            str(self.image).index("upload/category/" + str(self.pk) + "/") :
        ]

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def all(self):
        return self.filter(is_active=True)

    def products_by_category(self, category):
        return self.filter(is_active=True).filter(category=category)

    def featured_products(self, limit):
        return self.filter(is_active=True).filter(is_featured=True)[:limit]

    def top_selling(self, limit):
        return self.filter(is_top_selling=True).filter(is_active=True)[:limit]

    def trending_products(self, limit):
        return self.filter(is_trending=True).filter(is_active=True)[:limit]

    def single_product(self, slug):
        return self.get(slug=slug, is_active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_today_deal = models.BooleanField(default=False)
    is_top_selling = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    gst = models.DecimalField(max_digits=10, decimal_places=2, default="")
    tag = models.CharField(max_length=255, blank=True)
    unit = models.CharField(max_length=255, default="pc")
    num_of_sale = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    meta_title = models.TextField(default="demo title")
    meta_description = models.TextField(default="demo title")
    meta_img = models.ImageField(upload_to="upload/products/meta", blank=True)
    short_desc = models.TextField(max_length=350)
    long_desc = models.TextField(max_length=350)
    auto_created = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="updated_date", auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def category_name(self):
        return Category.objects.get(name=self.category).name