from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar


urlpatterns = [
    path('', BaseView.as_view(), name="index"),
    path('products/<str:ct_model>/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),

]

if settings.DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
    }
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)