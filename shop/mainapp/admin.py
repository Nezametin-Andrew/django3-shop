from django.contrib import admin
from .models import NoteBook, Brand, Category, SmartPhone, CartProduct, Cart
from django import forms
from django.forms import ModelForm


class SmartPhoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(kwargs)


class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug="notebooks"))
        if db_field.name == 'brand':
            return forms.ModelChoiceField(Brand.objects.filter(
                slug__in=['samsung', 'asus', 'lenovo', 'apple_book']
            ))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    form = SmartPhoneAdminForm
    change_form_template = 'admin.html'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(len(db_field.name))
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug="smartphones"))
        if db_field.name == 'brand':
            return forms.ModelChoiceField(Brand.objects.filter(
                slug__in=['apple_phone', 'samsung', 'asus', 'xiaomi']
            ))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(NoteBook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)

