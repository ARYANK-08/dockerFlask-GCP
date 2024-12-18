- microservices : services are fine grained and protocols are lightweight
- monolithic arc : built as a single unit, deployed as a single unit, duplicated on each server, 3 tier architecture [web -> business-> data]
- microservices : big system into smallers parts with each responsibility, scccales eacch service independently, each microservices can have its own language/db
- while deploying monolithic - whole system needs to be deployed wherreas in microservices small units
- from mono to micro : break your application/system in small units

microsercvices != magic pixie dust [benefits]
- improved fault isolation 
- easy to understand hence smaller and faster deployements and easy to scale
drawbacks
- multiple databases
- latency issues
- multiple point of failures
- security

cloud native:
- containers, service meshes, microsevices, immutable infra, declarative apis
- speed and agility 
- application arch : clean code using domain driven design -> microservices principle -> kubernetes pattern
- pets vs cattle mentality : 
    - infrastructure becomes immutable and disposable
    - provisioned in minutes and destroyed on demand
    - never updated or repaired but reprovisioned

1. containerization : docker containers
2. ci/cd : 
3. orhcestration and application definition : kubernetees
4. analysis and observability
5. service proxy
6. networeking security and policy

containers :
what is a container ? : a unit of software deployment
it contains code, runtime, system tools, system libraries

why use containers?
- move faster by deploying smaller units
- fit more into same server host
- faster to delpoy using cicd
- isolation 

virtualized ?
virtual machines : runs the hardware with os(virtualize the hardware) 
booting time : 

container : virutalize the os
compared to VM : container doesnt have to boot bcs it used host os kernel it starts in seconds


vMS vs Containers:
- large footprint
- slow to boot 
- ideal for long running tasks

containers:
- lightweight
- quick to start(it doesnt have to boot)
- portable
- ideal for short lived task

Density:

Containers are made of layers:
base os (windows/linux)->customizations->applications
eg : docker pull microsoft/dotnet
each downloads individully with id
you can only write the top layer
below layers are read only

container registry :  centralized container repository
think github for containers
docker hub : hhub.docker.com
cloud providers :aws, azure, digitral ocean

Orchestrator : whiplash example (taklu guy )
- manage :
    - infrastructure
    - containers 
    - deployement
    - scaling
    - failover
    - health monitoring
    - app upgrades, zero downtime deployements

- install your own :
    - kubernetes, swarm, service fabric 

- what is docker ?
    -> provides open source container runtime runs of mac windoews linux
    -> CLI -> dockerfile format to build containers
    -> windows lets you create windows/linux containers

- docker pull [imageName] : pull an imager from a registry
- docker run [imageName] : run containers
- docker run -d [imageNAme] : detached mode
- docker start [containerName] : start stopped containers
- dockers ps : list running containers
- docker ps -a : list running and stopped containers
- docker stop [containerName] : stopc containers
- docker kill [containerName] : kills containers
- docker image inspect [imageName] : get image info

docker run --memory="256m" nginx : max memory
docker run --cpus=".5" nginx : max cpu

runnign  a container 
```
# pull and run an nginx server
docker run --publish 80:80 --name webserver nginx

docker ps #list running containers

docker stop webserver

docker rm webserver

cleanup : docker system prune -a 
```

pull and run a nginx server

docker run -d -p 8080:80 --name webserver nginx
docker ps


docker build -t [name:tag] . 
docker tag [imageName] [name:tag]

used >p command pallete to create flask image automatically creates docker file
run it and build containers

- containres are ephemerouss and stateless 
ephemerous -> short lived
you usally dont store data in containers
non persisten data :
 locally on a writable layer
 its the default just write to fs when containers are destroyed so the data inside them
persisten data:
 stored outside container in a volume , volume is mapped to a logical folder
volumes : maps folder on the host to locatical folder in container


persistent data:
volumes 
docker create volume [volumneName]
dockker volume ls
docker volume insped [volumeName]
docker volume rn [volumeName]


YAML - yaml aint markup language
used by docker compose and kubernetes
key : value
a_number_value: 100

docker compose 
- multi container apps 
frontend backend redis (multiple docker run)
docker comopose : define and run multi containers application using single yaml files
    docker-compose | docker compose

docker compose build
docker compose start
docker compose stop
docker compose up -d 
docker compose ps
docker compose rm
docker compose down
docker compose logs
docker compose exec [container] bash



docker compose build
Run the app
docker compose up -d
When the app will run, launch the voting app in your browser http://localhost:5000

List the containers
docker compose ps
Look at the db container logs
docker compose logs -f web-fe
Compose V2 commands
LS will list the current projects

docker compose ls
Let's try to deploy a second version
docker compose up -d
This fails because we can only run an app a single time

Deploy a second version using a different project name
Let's now use a project name to see if we can deploy a second version

docker compose -p test up -d
This fails because the localhost port 5000 is already assigned.

Change the ports value from

- "5000:80"
to

- "5001:80"
Deploy again
docker compose -p test up -d
How many versions do we have running?

docker compose ls
Cleanup
docker compose down
docker compose ls
docker compose -p test down
docker compose ls




```
yaml
version: "3"
services:
  web-fe:
    build:
      context: .
    command: gunicorn --bind 0.0.0.0:5000 main:app
    ports:
      - "5001:5000"
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PASSWORD=yourpasswordhere
  redis:
    image: "redis:alpine"
    ports:
      - "6371:6379"
    environment:
      - REDIS_PASSWORD=yourpasswordhere
```
```
dockerfile
FROM python:alpine
WORKDIR /code
ADD main.py requirements.txt /code/
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

```

docker compose features
resource limits
```
resources:
  limites:
  cpus: '0.50'
  memory: 150M
reservations:
  cpus: '0.25'
  memory: 20M

eNVIRONNMENT VARIABLES:

```
db:
  image: "postgres:${POSTGRES_VERSION}"

```
NETWORKING
```
services:
  web:
    image: nginx:alpine
    ports: 
     - "8000:80"
  db:
    image: postgres
    ports:
     - "5432"
```
[web][db]
web can communicate with db 
reach from outside -> 8000 port , db can reach web using port 80
web can use db with port 5432

to configure restrictions to who sees who
```
networks:
  frontend:
  backend:
```

dependence:
```
app:
  image: myapp
  depends:on:
    - db

db:
  image: postgres
  networks:
    - back-tier
```
compose will start db first bcs app depends on db

named volumes:

restart policy:
no :
- default restart policy
- doestn restart contasiner under any circumstances
always:
- always restarts the container until its removal

container registeries: central repo fopr container imagfes
pvt/public 
default is hub.docker.com
aws ecr(elastic container registry)

docker pull theimage:latest

push/pull images to docker hub

docker login -u <username> -p <password>
docker tag
docker push



push image to docker hub
docker build -t aryanthedockerman/flask:v1 .
docker push aryanthedockerman/flask:v1
docker build -t aryanthedockerman/flask:v2 .

----


K8s aka kubernetes
- leading container orchestration tool
- vendor neutral : runs on all cloud providers

what can k8s can do?
- service discovery and load balacning
- automated rollouts and rollbacks
- storage orchestration : local or cloud based
- self healing
- secret and config management

what cant k8s dp?
- doesnt deploy source code
- doesnt build your application
- doestn provide application level services
  : message buses, databases caches etcc

K8s architecture:
  master(control) worker nodes
  cluster->node->pod

run k8s locally
- required virtualization
  docker desktop
  microk8s
  minikube
- runs over docker desktop
  kind
- limited to 1 node : docker desktop
- multiple nodes : microk8s, kind, minikube

on windows:
docker desktop is only way to run both linux and windows currently
WSL


exposes a rest api (only point of communication)
define desired state in yaml eg : x no of instancees run
kubectl coomunicates with apiserver

k8s context:
a context is a group of access paramets to a k8s cluster
contains kubernetes cluter, user, namespace
the current context is the clsuter that is currentyl the default for uibetctl
all kubctl commands run against the cluster


kubectl config curent-context
kubetctl config get-context
kubectl config use-context [contextName]
kubectl config delete-context [contextName]


kubectx - quickly switch context
- instead of typing kubectl config use-context minikube
- kubectx [contextNAme]
- choco install kubectx-ps


kubectl config current-context : minikube

 kubectl config get-contexts
CURRENT   NAME             CLUSTER          AUTHINFO         NAMESPACE
          docker-desktop   docker-desktop   docker-desktop   
*         minikube         minikube         minikube         default

kubectl config use-context docker-desktop
kubectl config rename-context [old-name] [new-name]
kubectl config delete-context [contextName]


the declarative vs imperative way to create kubernetes
declarative :
- using kubectl and yaml defining the resources you need 
- reporoducible reperatedble can be saved in source control
- its like data that can b parsed and modified

imperative :
- kubectl issue a series of commands to create resources
- its like code


imperative way:
kubectl run mynginx --image=nginx --port=80
kubectl create deploy mynginx --image=nginx --port=80 --replicas=3
kubectl create service nodeport myservice --targetport = 8080
kubectl delete pod nginx

yaml file:
- root level reqd properites
    - apiVersion : 
    - kind: type of object
    -metadata.name : unique name for the object
    -matadata.namespace
    -spec: object specifications or desired state

pod definition
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    type: front-end
  spec:
    containers:
    - name: nginx-container
      image: nginx
```

create an object using YAML
- kubectl create -f [YAML file]

creating new manifest: kuberetes.io/docs 
use templates
use kubectl commands --dry-run=clinet -o yaml >deploy.yaml

imperative:
kubectl create deployment mynginx1 --image=nginx 
declarative:
kubectl create -f deploy-example.yaml
kubectl delete  deploy mynginx1


NameSpaces:
- allow to group resources eg: dev,test,prod [multiple environment deployment]
- objects in one namespace can acccess objects in a different one[objectname.prod.svc.cluster.local]
- deleting a namespace will delete all its child objects

namespace definition:
apiVersion: v1
kind: Namespace
metadatA:
  name: prod
  #(namespace prod is defined)

pod definition
apiVersion: v1
kind: Pod
metadata:
  name:
  namespace:
spec:
  contrainers:
    -name : 
    image: 


kubectl get namepsace
kubectl get ns
kubectl config set-context --curent --namespace=[nameSpaceNAme]
kubectl create ns [namespaceName]
kubectl delete ns [nameSpacename]
kubetctl get pods --all-namespaces

kubectl get ns
kubectl get pods -n kube-system
NAME                                     READY   STATUS    RESTARTS   AGE
coredns-55cb58b774-27njj                 1/1     Running   0          38m
coredns-55cb58b774-p9tx6                 1/1     Running   0          38m
etcd-docker-desktop                      1/1     Running   0          38m
kube-apiserver-docker-desktop            1/1     Running   0          38m
kube-controller-manager-docker-desktop   1/1     Running   0          38m
kube-proxy-c99jk                         1/1     Running   0          38m
kube-scheduler-docker-desktop            1/1     Running   0          38m
storage-provisioner                      1/1     Running   0          38m
vpnkit-controller                        1/1     Running   0          38m

kubectl config set-context --curent --namespace=kube-system
kubectl get pods


masternode
a node is physical or virtual machine
a grp of nodes form cluster
master node is called conmtrol plane

master components 
dont run containers on master node
etcd -> key value datastore for cluster state data
apisever is only component communicating with etcd

kube-apiserver
  REST interface
  save state to etcd datastore
  all client interact with it never directly to the datastore

etcd
  act as the cluster datastore for storing state
  key-value store
  not a db or a datastore for applications to use
  single source of truth

kube control manager
  controller of controllers
  it runs node controller, replication, endpoint, controllers, service acac and token ctontrollers

cloud control manager:
  interact with the cloud providers controller
  node : for checking cloud provider to determine if a node has been deletd in cloud
  route : for setting up routes in cloud infra
  service: for creating, updating and deleting cloud provider load balancers
  volume: for creating, attaching, and mounting volumes and interacting w vloud provider to orchestrate volumnes

kube scheduler:
  watches newly created pods that have no node assigned and selectrs a node to run on 

add ons:
  DNS
  WEB UI DASHboard
  cluster lvevl logging


worker nodes:
container runtime kubelet kuve proxy [necessary to run pod]

kubelet manages pods lifecycle [running healthy]

kubeproxy : netowrk proxy manages netwrok rules and nodes

container runtime : cri moby

nodes pool: group of vms all with same size
cluster can have multipe node pools each can host diff sizes of vms

pods:
smallest unit of work of k8s
represents unti of deployement
pods can run one or more containers
containers within a pod share : ip address space, mounted volumes
containers within a pod can communicate via : localhost, ipc
encapsulates and applications container
pods are ephemeral
deploying a pod is an atomic opn it succeed or not
if a pod fails its replaced witha  new one with a new ip address
you dont update a pod you replace with an updated version
you scale by addming more pods not more containers
pods are like cattles

node ccan run many poods, pods can run mmultiple containers
usually one main worker(app logic), sidecard or helper pattern container
-------



pod lifecycle
api server etc schedule kubelet runtime

pod state 
high level summary of where pod is in lifecycle
  pending : accepted but not yet created
  running: bounding to a node
  succeeded: exited with status 0
  faild: all containers exit and at lesat one exited with non zero status
  crashloopbackoff: started,crashed,strartedagain,tehn gcrashed again

:give real world scnarios for crashloopbackoff

defining and running pods
yaml
```
kind: Pod
image: nginx
containerPort: 80
protocol tcp
env:
command
```

kubectl create -f [pod-definition.yml]
kubectl run [podname] --image=busbox -- bin/sh -c "sleep 3600"
kubectl get pods
kubectl get pods -o wide
kubectl describe pod [podname]
kubectl get pod [podname] -o yaml > file.yaml
kubectl exect -it [podname] --sh
kubectl delete -f [pod-definition.yml]
kubectl delete pod [podname]



kubectl run mybox --image=busybox -it -- /bin/sh


init containers:
my app has a depency on [db,api,file] but i dont want to clutter it with infra code
initalize a pod before an application container runs


```
initContainers:
  name:
  image:
  command:

```

give flask app and yaml covering all the concepts above and explain in comments

Labels : key value pairs
  app: 
  type:

selectors: use label to filter/select objects
compare it w sql query
nodeSelector:
  disktype: superfast
select * from nodes where disktype=superfast



deploy a app
deploy a service
check ip of pod
kubectl get po -o wide
kubectl get ep myservice 
enpoints : same ip address
kubectl port-forward service/myservice 8080:80
show sample code : labels must match app.yaml service.yaml



multi container pods:
main worker and helper workers (sending data to db, writing log files)

give real world examples of these patterns below

sidecar pattern:
app : write to log file
sidecar : copy log files to persistent storage
super clean code

adapter:
app  : writes complex monitoring op
adapter : simplify monitoring op for srevice

ambassador:
app : needs to write to persist data to a db
ambassador : knows how to write to a db -> db


pod definition for multi container pods

kubectl create -f [pod-def.yml]
kubectl exec -it [podname] -c [containername] -- sh
kubectl logs [podname] -c [containername]


networking concepts [explain with real world examples scenarios]
all container within a pod can communicate with each other
alll pods can communicate with each other
all nodes can communicate with all pods
pods are gicen an ip address(ephermeral)
services are given a persistent ip

pod netwroking explain 
acces via service
load balancer->srvice -> pod1 2 3

create two-containers.yaml
port80
port81

connect to the container


workloads:
workload is an application running on kubereetes
pod : reperesents a set of running containeres
replicaset
deployment
daemonset
job cronjob

replicaset: manage and debug replicas
desired no of instances are running
self healing : 
replaces a pod if it fails

define a replicaset

deploments vs pods
pods dont :
    self heal
    scale
    updates
    rollback
deployements can:
    manage a single pod templates
    you can create a deployment for each microservice
        frontend
        backend
        imageprocessor
        credit card processor

deployements create replicatesets in the bg
but dont interact with replicateserts directly

deployements :rolling updates and roillbacks
replicatsets: self healing and scalability

deployements :
replicas: no of pod instances
kind : deployementsx
strategy : rolling update ,recreate: 


daemonset
- ensures all nodes run an instance of a pod
- as nodes are added to cluster pods are added to them
- typical uses:
    running a cluster storage daemon
    running a logs collection deamon on every node
    running a node monitoring deamon on every node


stateful set:
scaling a db
more instances
for pods that must p[ersists or maintain state
typiocal uses:
    stable, uniq netowrk identifiers
    stable, databases using persisten storage
ordered destruction
clusterip : none
name :mysql

wawrnings:
containers are stateless by design
stateful sets ofers a solution for satetful scneaiors

  


job cron job


rollingupdate
 explain with real world scnariors

rolling update issues


services
accesing pods




⭐️ 4:21:13 Services
⌨️ What are services?
⌨️ ClusterIP Concepts
⌨️ ClusterIP Hands-On
⌨️ NodePort Concepts
⌨️ NodePort Hands-On
⌨️ Load Balancer Concepts
⌨️ Load Balancer on Docker Desktop Hands-On
L4 Load balacning:
operates on tcp(transport layer)
unable to make decision based on content
simple algorithms such as round robin routing

L7 LB:
operates at application layers(http,smpt)
able to make decisions based on the actual content of each message
more intelligent load balacning decisions and content optimizations

⭐️ 4:44:03 Storage & Persistence
⌨️ Storage & Persistence Concepts
⌨️ The Static Way
⌨️ The Static Way Hands-On
⌨️ The Dynamic Way

⭐️ 5:03:48 Application Settings
⌨️ ConfigMaps Concepts
⌨️ ConfigMaps Hands-On
⌨️ Secrets Concepts
⌨️ Secrets Hands-On

⭐️ 5:22:24 Observalibilty
⌨️ Startup, Readiness and Liveness Probes Concepts
⌨️ Probes Hands-On

⭐️ 5:30:46 Dashboards 
⌨️ Dashboards Options
⌨️ Lens Hands-On
⌨️ K9s Hands-On

⭐️ 5:47:36 Scaling
⌨️ Auto Scaling Pods using the Horizontal Pod Autoscaler
⌨️ Auto Scaling Pods Hands-On


scaling pods
horizontal pods autoscaling
uses k8s metric server
pods must have requests and limits defined
hpa checks the metris server every 30seconds
and scale acc to min and max no of replicas defined
cooldown/delay
prevent racing conditions
once a change has been made hpa waits
by default the delay on scale up events is 3minutes and delay on scale dwon is 5 minutes
whats racing conditions?
yaml
limits are mandory : request:resoruces memrtoyr crpu 64mi 250m
min and max replicates #   f l a s k _ g c p _ d o c k e r 
 
 
