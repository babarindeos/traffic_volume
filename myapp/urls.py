from . import views
from django.urls import path, include
from . import urls

urlpatterns = [
    path('', views.index, name='index'),  
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),    
    path('home', views.home, name='home'),
    path('basestation', views.basestation, name='basestation'),
    path('locations', views.locations, name='locations'),
    path('clusters', views.clusters, name='clusters'),
    path('nodes', views.nodes, name='nodes'),
    path('recharge', views.recharge, name='recharge'),
    path('faults', views.faults, name='faults'),
    path('traffic', views.traffic, name='traffic'),
    path('simulation', views.simulation, name='simulation'),
    path('run_simulation', views.run_simulation, name='run_simulation'),
    path('simulation_completed', views.simulation_completed, name='simulation_completed'),
    path('create_location', views.create_location, name='create_location'),
    path('location/edit/<int:id>', views.location_edit, name='location_edit'),
    path('location_update', views.location_update, name='location_update'),
    path('location/delete/<int:id>', views.location_delete, name='location_delete'),
    path('create_cluster', views.create_cluster, name='create_cluster'),
    path('cluster/edit/<int:id>', views.cluster_edit, name='cluster_edit'),
    path('cluster_update', views.cluster_update, name='cluster_update'),
    path('cluster/delete/<int:id>', views.cluster_delete, name='cluster_delete'),
    path('create_node', views.create_node, name='create_node'),
    path('node/edit/<int:id>', views.node_edit, name='node_edit'),
    path('node_update', views.node_update, name='node_update'),
    path('node/delete/<int:id>', views.node_delete, name='node_delete'),
    path('node/recharge/<int:id>', views.node_recharge, name='node_recharge'),
    path('recharge_allnodes', views.recharge_allnodes, name='recharge_allnodes'),
    path('node/repair/<int:id>', views.node_repair, name='node_repair'),
    path('generate_fault', views.generate_fault, name='generate_fault'),
    path('vehicles', views.vehicles, name='vehicles'),
    path('register_vehicle', views.register_vehicle, name='register_vehicle'),
    path('vehicle/delete/<int:id>', views.vehicle_delete, name="vehicle_delete"),
    path('traffic_details/<str:id>', views.traffic_details, name='traffic_details'),
    path('logout', views.logout, name='logout')

    
]