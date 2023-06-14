
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('et-admin/', admin.site.urls),
    path('',include('product.urls')),
    path('',include('account.urls')),
    path('accounts/', include('account.passwords.urls')), 
    path('',include('wishlist.urls')),
    path('',include('cart.urls')),
    path('',include('address.urls')),
    path('',include('order.urls')),
    path('',include('review.urls')),
    path('',include('shop.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
