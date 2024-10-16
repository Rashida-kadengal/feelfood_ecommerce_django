from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/',views.about_us,name="about_us"),
    path('contact-us/',views.contact_us,name="contact_us"),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/buy_now/', views.buy_now, name='buy_now'),
    path('products/<int:product_id>/reviews/',views.create_product_review,name='create_product_review'),
    path('products/<int:product_id>/reviews/<int:review_id>/delete/', views.delete_product_review, name='delete_product_review'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/profile/'), name='change_password'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)