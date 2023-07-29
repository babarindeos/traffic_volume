import json
import random
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature, Location, Cluster, Node, Traffic, Vehicle
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #return HttpResponse(password)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials" )
            return redirect('login')

    else:
        return render(request, 'login.html')
    


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def basestation(request):
    traffic = Traffic.objects.values('identifier').distinct()    
     
    return render(request, 'basestation.html', {'traffic':traffic}) 

@login_required
def locations(request):
    locations = Location.objects.all()    
    return render(request, 'locations.html', {'locations': locations})

@login_required
def clusters(request):
    clusters = Cluster.objects.all() 
   
    return render(request, 'clusters.html', {'clusters' : clusters})

@login_required
def nodes(request):
    nodes = Node.objects.all()
    return render(request, 'nodes.html', {'nodes': nodes})

@login_required
def recharge(request):
    nodes = Node.objects.all()
    return render(request, 'recharge.html', {'nodes': nodes})

@login_required
def faults(request):
    nodes = Node.objects.all()
    return render(request, 'faults.html', {'nodes': nodes})

@login_required
def traffic(request):
    return render(request, 'traffic.html')


@login_required
def simulation(request):
    return render(request, 'simulation.html')




@login_required
def run_simulation(request):
    #check for existing vehicle
    vehicle_count = Vehicle.objects.all().count()

    if vehicle_count==0:
        messages.info(request, 'There are no register Vehicles')
        return redirect('home')
    
    #check for locations
    location_count = Location.objects.all().count()
    if location_count==0:
        messages.info(request, 'There are no Locations')
        return redirect('home')
    
    #check for clusters
    cluster_count = Cluster.objects.all().count()
    if cluster_count==0:
        messages.info(request, 'There are no Clusters')
        return redirect('home')
    
    #check for nodes
    node_count = Node.objects.all().count()
    if node_count==0:
        messages.info(request, 'There are no Nodes')
        return redirect('home')


    
    sim_identifier = uuid.uuid4() 
    
    #get the total traffic
    randtrip = random.randint(5,100)

    #get the locations into an a list
    location_list = []
    locations = Location.objects.all()
    for location in locations:
        location_list.append(location.name)


    #get the vehicles into a list
    vehicle_list = []
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        vehicle_list.append(vehicle.plateno)


    # run trip
    for i in range(randtrip):
        # get location for round
        location = ""
        location_object = None
        cluster = None
        nodes = None
        nodehead = ""

        location = random.choice(location_list)

        location_object = Location.objects.get(name=location)

        # get the cluster to the location
        cluster = Cluster.objects.get(location=location_object)

        #get node in cluster
        nodes = Node.objects.filter(cluster=cluster)

        if nodes is not None:           
            for node in nodes:                
                if (node.headship == True):
                    nodehead = node.name
        
    
        
        #get vehicle
        vehicle = random.choice(vehicle_list)

        # save into traffic db
        new_traffic =  Traffic.objects.create(identifier=sim_identifier, location=location, 
                                              cluster=cluster.name, headnode=nodehead,
                                              vehicle=vehicle)
        new_traffic.save()
    
    
    #sim_identifier = str(sim_identifier)
    sim_identifier = json.dumps(sim_identifier, cls=DjangoJSONEncoder)
    sim_identifier = sim_identifier[1:-1]
    request.session['sim_identifier'] = sim_identifier

    return redirect('simulation_completed')


@login_required
def simulation_completed(request):
    sim_identifier = request.session.get('sim_identifier')
    traffic = Traffic.objects.filter(identifier = sim_identifier)

    context = {
        'sim_identifier' : sim_identifier,
        'traffic' : traffic
    }
    
    return render(request, 'simulation_completed.html', context)
    



@login_required
def create_location(request):
    if request.method=='POST':
        location_name = request.POST['location_name']

        if Location.objects.filter(name=location_name).exists():
            messages.info(request, 'A Location with the name ' + location_name + ' already exist, and cannot be duplicated.')
            return redirect('create_location')
        else:
            new_location = Location.objects.create(name=location_name)
            new_location.save()
            return redirect('locations')


    else:
        return render(request, 'create_location.html')
    

@login_required
def location_edit(request, id):    
    if Location.objects.filter(id=id).exists():
        location = Location.objects.get(id=id)             
        return render(request, 'location_edit.html', {'location':location})
    else:
        return redirect('locations')

@login_required
def location_update(request):
    id = request.POST['id']
    name = request.POST['location_name']
    location = Location.objects.get(id=id)
    location.name = name
    location.save()
    return redirect('locations')

@login_required
def location_delete(request, id):
    if Location.objects.filter(id=id).exists():
        location = Location.objects.get(id=id)
        location.delete()

        return redirect('locations')
    
@login_required
def create_cluster(request):
    if request.method == "POST":
        cluster_name = request.POST['cluster_name']
        location_id = request.POST['location_id']  

        if Cluster.objects.filter(name=cluster_name).exists(): 
            messages.info(request, "A Cluser with the name [" + cluster_name +" already exist, and cannot be duplicated]")
            return redirect('create_cluster') 
        else:
            new_cluster = Cluster.objects.create(name=cluster_name, location=Location.objects.get(id=location_id))
            new_cluster.save()
            return redirect(clusters)

    else:
        locations = Location.objects.all()   
        context = {
            'locations' : locations
        }    
        return render(request, 'create_cluster.html', context)


@login_required
def cluster_edit(request, id):
    if Cluster.objects.filter(id=id).exists():
        locations = Location.objects.all()
        cluster = Cluster.objects.get(id=id);

        context = {
            'locations':locations,
            'cluster':cluster
        }
        return render(request, 'cluster_edit.html', context)
    else:
        return redirect('clusters')



@login_required
def cluster_update(request):
    cluster_id = request.POST['cluster_id']
    cluster_name = request.POST['cluster_name']
    location_id = request.POST['location_id']
    
    cluster = Cluster.objects.get(id=cluster_id);

    cluster.name = cluster_name
    cluster.location = Location.objects.get(id=location_id)

    cluster.save()

    return redirect('clusters')

@login_required
def cluster_delete(request, id):
    if Cluster.objects.filter(id=id).exists():
        cluster = Cluster.objects.get(id=id)
        cluster.delete()

        return redirect('clusters')
    else:
        return redirect('clusters')
    
@login_required
def create_node(request):
    if request.method == 'POST':
        node_name = request.POST['node_name']
        cluster_id = request.POST['cluster_id']

        cluster = Cluster.objects.get(id=cluster_id)

        new_node = Node(name=node_name, cluster=cluster, battery=30, fault=False, headship=False)
        new_node.save()

        return redirect('nodes')
    else:
        clusters = Cluster.objects.all();
        return render(request, 'create_node.html', {'clusters' : clusters})
        
@login_required
def node_edit(request, id):
    if Node.objects.filter(id=id).exists():
        node = Node.objects.get(id=id)
        clusters = Cluster.objects.all()

        context = {
            'node' : node,
            'clusters' : clusters
        }

        return render(request, 'node_edit.html', context)
    else:
        return redirect('nodes')
    
@login_required
def node_update(request):
    if request.method == 'POST':
        node_id = request.POST['node_id']
        node_name = request.POST['node_name']
        cluster_id = request.POST['cluster_id']
        battery = request.POST['battery']
        if 'fault' in request.POST and  request.POST['fault']=='on':
            fault = True
        else:
            fault = False
            
        # get node by id
        node = Node.objects.get(id=node_id)
        node.name = node_name
        node.cluster = Cluster.objects.get(id=cluster_id)
        node.battery = battery
        node.fault = fault

        # save updated node
        node.save()

        return redirect('nodes')
    
@login_required
def node_delete(request, id):
    if Node.objects.filter(id=id).exists():
        node = Node.objects.get(id=id)
        node.delete()
        return redirect('nodes')
    else:
        return redirect('nodes')  
    
@login_required
def node_recharge(request, id):
    recharge = random.randint(70, 100)
    
    node = Node.objects.get(id=id)
    node.battery = recharge   
    node_cluster = node.cluster
    node.save()

    #determine headship in the node cluster
    mycluster_dict = {}
    nodes = Node.objects.filter(cluster=node_cluster)  
    
    for node in nodes:
        if node.fault == True:
            continue
        mycluster_dict.update({node.id:node.battery})
        node.headship = False
        node.save()
    
    if mycluster_dict:
        highest = max(mycluster_dict, key=mycluster_dict.get)    
        win_node = Node.objects.get(id=highest)
        win_node.headship = True
        win_node.save() 

    return redirect('recharge')


@login_required
def recharge_allnodes(request):
    nodes = Node.objects.all()

    counter = 0

    for node in nodes:
        recharge = random.randint(70,100)
        node.battery = recharge        
        node.save()        
        counter = counter + 1
    
    
    clusters = Cluster.objects.all()
    for cluster in clusters:
        nodes = Node.objects.filter(cluster=cluster)
        
        mycluster_dict = {}
        for node in nodes:
            if node.fault == True:
                continue
            mycluster_dict.update({node.id:node.battery})
            node.headship = False
            node.save()
        
        if mycluster_dict:
            highest = max(mycluster_dict, key=mycluster_dict.get)
        
            win_node = Node.objects.get(id=highest)
            win_node.headship = True
            win_node.save()
         

    return redirect('recharge')


def node_repair(request, id):
    node = Node.objects.get(id=id)
    node.fault = False
    node_cluster = node.cluster
    node.save()

    # determine headship in node cluster
    mycluster_dict = {}
    nodes = Node.objects.filter(cluster=node_cluster)  
    
    for node in nodes:
        if node.fault == True:
            continue
        mycluster_dict.update({node.id:node.battery})
        node.headship = False
        node.save()
    
    if mycluster_dict:
        highest = max(mycluster_dict, key=mycluster_dict.get)    
        win_node = Node.objects.get(id=highest)
        win_node.headship = True
        win_node.save() 

    return redirect('faults')
    
def generate_fault(request):
    nodes = Node.objects.all()

    counter = 0

    for node in nodes:
        fault = random.choice([True, False])
        node.fault = fault       
        node.save()        
        counter = counter + 1
    
    
    clusters = Cluster.objects.all()
    for cluster in clusters:
        nodes = Node.objects.filter(cluster=cluster)
        
        mycluster_dict = {}
        for node in nodes:
            if node.fault == True:
                continue
            mycluster_dict.update({node.id:node.battery})
            node.headship = False
            node.save()
        
        if mycluster_dict:
            highest = max(mycluster_dict, key=mycluster_dict.get)
        
            win_node = Node.objects.get(id=highest)
            win_node.headship = True
            win_node.save()
         

    return redirect('faults')


@login_required
def vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles.html', {'vehicles':vehicles})
    

@login_required
def register_vehicle(request):
    if request.method=='POST':
        make = request.POST['make']
        model = request.POST['model']
        color = request.POST['color']
        plateno = request.POST['plateno']
        owner = request.POST['owner']

        new_vehicle = Vehicle.objects.create(make=make, model=model, color=color, plateno=plateno, owner=owner)
        new_vehicle.save()

        return redirect('vehicles')

    else:
        return render(request, 'register_vehicle.html')


def traffic_details(request, id):
    sim_identifier = id
    traffic = Traffic.objects.filter(identifier=id)
    context = {
        'sim_identifier' : sim_identifier,
        'traffic' : traffic
    }
    return render(request, 'traffic_details.html', context)

def vehicle_delete(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.delete()
    return redirect('vehicles')

def logout(request):
    auth.logout(request)
    return redirect('/')



