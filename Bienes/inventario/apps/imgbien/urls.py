from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AddImgBien, ListImgBien, RegImgBien, DeleteImgBien


urlpatterns = [
    path('img_bien/<slug>',ListImgBien.as_view(), name='list_imagenes' ),
    path('add_img_bien/<slug>',AddImgBien.as_view(), name='add_imagen' ),
    path('reg_img_bien',RegImgBien.as_view(), name='reg_img' ),
    path('del_img_bien/<slug>',DeleteImgBien.as_view(), name='del_img' ),
    
]