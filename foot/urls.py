from django.urls import path
from .views import *
    
urlpatterns = [
    path('', Home, name='Home'),
    path('Services', Services, name='Services'),
    path('Contact', Contact, name='Contact'),
    path('About_us', About_us, name='About_us'),
    path('home', home, name='home'),
    path('realtime/', realtime, name='realtime'),  
    path('api/historical-data/', historical_data, name='historical_data'),
    path('api/real-time-data/', real_time_data, name='real_time_data'),
    path('api/add-footstep-data/', add_footstep_data, name='add_footstep_data'),
    path('api/hotspot-footstep-data/', hotspot_footstep_data, name='hotspot_footstep_data'),  
    path('api/hotspot-footstep-data/<str:location_name>/', hotspot_footstep_data_detail, name='hotspot_footstep_detail'), 
    path('traffic/', traffic, name='traffic'),
    path('vehicle-counting/', vehicle_counting, name='vehicle_counting'),
    path('video_feed/', video_feed, name='video_feed'),
]
