from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={"ct_model": ct_model, "id": obj.id})


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        "Ноутбуки": "notebook__count",
        "Смартфоны": "smartphone__count"
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_category_for_site_bar(self):
        model = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*model))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class LatestProductManager:

    @staticmethod
    def get_product_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_to")
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            get_product = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(get_product)
        if with_respect_to and with_respect_to in args:
            return sorted(
                products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
            )
        return products


class LatestProduct:

    object = LatestProductManager()


class Brand(models.Model):

    name = models.CharField(max_length=255, verbose_name="Производитель")
    slug = models.SlugField(unique=True, verbose_name="slug_brands")

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(unique=True, verbose_name="slug_category")
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={"slug": self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Наименование")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Стоимость")
    description = models.TextField(max_length=255, verbose_name="Описание")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Производитель")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField(verbose_name="Изображение")
    view = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    like = models.PositiveIntegerField(default=0, verbose_name="Этот товар понравился")
    discount = models.IntegerField(verbose_name="Скидка")
    new = models.BooleanField(default=False, verbose_name="Новинка")


class NoteBook(Product):

    class Meta:
        verbose_name = "Ноутбуки"

    display = models.CharField(max_length=255, verbose_name="Диагональ экрана")
    processor = models.CharField(max_length=255, verbose_name="Процессор")
    video_cart = models.CharField(max_length=255, verbose_name="Параметры видеокарты")
    ram = models.CharField(max_length=20, verbose_name="Оперативная память")
    acum = models.CharField(max_length=255, verbose_name="Время работы от аккамулятора")
    ssd = models.BooleanField(default=False, verbose_name="Наличие ssd диска")
    ssd_info = models.CharField(max_length=20, verbose_name="Объем ssd диска", null=True, blank=True)
    hdd = models.BooleanField(default=False, verbose_name="Наличие hdd диска")
    hdd_info = models.CharField(max_length=20, verbose_name="Объем hdd диска", null=True, blank=True)
    backlight_keyboard = models.BooleanField(default=False, verbose_name="Наличие подсветки клавиатуры")

    def __str__(self):
        return f"Ноутбук {self.brand} {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class SmartPhone(Product):

    class Meta:
        verbose_name = "Смартфоны"

    display = models.CharField(max_length=255, verbose_name="Диагональ экрана")
    processor = models.CharField(max_length=255, verbose_name="Процессор")
    ram = models.CharField(max_length=20, verbose_name="Оперативная память")
    acum_value = models.CharField(max_length=255, verbose_name="Объем аккамулятора")
    sd_cart = models.BooleanField(default=True, verbose_name="Наличие sd карты")
    sd_value = models.CharField(max_length=255, verbose_name="Максимальный объем sd карты")
    main_cam_value = models.CharField(max_length=255, verbose_name="Оснавная камера")
    frontal_cam_value = models.CharField(max_length=255, verbose_name="Фронтальная камера")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name="")
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="")

    def __str__(self):
        return self.content_object.title


class Cart(models.Model):

    owner = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name="")
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f"product in cart {self.products}"


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="")
    address = models.CharField(max_length=255, verbose_name="")

    def __str__(self):
        return "Покупатель"


#
#
# class Camera(Product):
#     pass
#
#
# class Television(Product):
#     pass
#
#
# class Monitor(Product):
#     pass
#
#
# class AudioSystem(Product):
#     pass
#
#
# class HeadPhones(Product):
#     pass
