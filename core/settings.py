import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i5eam4a&74pn2(le&r@vc07xbv4vl4)c30u%kd!bl@@9r5rtg_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    # admin-dashboard defintion
    'jazzmin',
     
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-part apps defintion
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'mptt',
    
    # internal-apps definition
    'account',
    'address',
    'cart',
    'coupon',
    'order',
    'product',
    'review',
    'shop',
    'wishlist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'account.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Deafult Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgrSQL Database Configuration
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'EtShopStoreDB',
#        'USER': 'postgres',
#        'PASSWORD': 'root',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Ckeditor [Rich text] configuration


CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline',
             'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList'],
            ['Indent', 'Outdent'],
            ['Maximize'],
        ],
        'extraPlugins': 'justify,liststyle,indent',
        'height': "auto",
        'width': "auto",
    },
}

# django-jazzmin config [admin dashboard]
JAZZMIN_SETTINGS = {
    # title of the window 
    "site_title": "ET-SHOP STORE",
    # Title on the login screen (19 chars max) 
    "site_header": "ET-SHOP STORE",
    # Title on the brand (19 chars max)
    "site_brand": "ET-SHOP STORE",
    # Logo to use for your site, present in static files
    "site_logo": "images/logo2.png",

    "welcome_sign": "Welcome to the ET-SHOP STORE",
    # Copyright on the footer
    "copyright": "ET-SHOP STORE",
    "user_avatar": None,

    # List of model admins to search from the search bar, search bar omitted if excluded
    "search_model": ["account.User",'shop.Product','shop.Order'],

     # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "ET-SHOP STORE", "url": "home", "permissions": ["account.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "account.User"},
    ],

    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,

    # for the full list of 5.13.0 free icon classes
    "icons": {
        "account.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "product.Product": "fas fa-shopping-basket",
        "product.Category":"fas fa-list",
        "order.Order" :"fas fa-list-alt",
        "address.Address":"fas fa-map-marker",
        "coupon.Coupon":"fas fa-check-circle",
        "cart.Cart":"fas fa-cart-plus",
        "wishlist.WishlistItem":"fas fa-heart",
        "shop.Sliders":"fas fa-anchor",
        "wishlist.Wishlist":"fas fa-heart",
        "order.ReturnOrder":"fas fa-reply",
        #"shop.Pages":"fas fa-link",
        "review.Review":"fas fa-eye",
        "shop.Sale":"fas fa-plus-square",
        "shop.SalesItem":"fas fa-id-card",
    },
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    "custom_js": None,
    "custom_css": "css/bootstrap-dark.css",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "account.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

