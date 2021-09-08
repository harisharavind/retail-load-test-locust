# retail-load-test-locust
A sample app which serves as a load-test for a basic retail platform using locust

The below details lets you to setup and run locust from scratch; 

# Prerequisite
- Python 3.7 
- Kubernetes
- Docker

# locust version
1.4.4

Please note that starting 1.0 locust has breaking changes.
To get to know about it, please refer to their official documentation at https://docs.locust.io/en/stable/changelog.html#changelog-1-0

# Setup
1. **Clone or Download this project** to your preferred directory
2. **Build the docker image.** The following command could be used:
```sh
docker build -t synctest:0.5.7 .
```
3. **Tag the image** for AWS ECR custom location
```sh
docker tag synctest:0.5.7 **.amazonaws.com/custom:synctest:0.5.7
```
4. **Push the image** to AWS ECR custom location
```sh
docker push **.amazonaws.com/custom:synctest:0.5.7
```
5. **Create a new namespace** "syncloadtest". From the location in which the project files are downloaded, goto /ymls/ folder.
```sh
k create -f create-ns.yml
```
6. **Create cluster role and role binding** for the new namespace.  This assigns read-only permission on services, pods, namespaces.
```sh
k apply -f create-clusterrole-ns.yml
```
8. **Deploy locust master profile.** From the /ymls/ folder execute the master deployment yml
```sh
k create -f create-deployment-master.yml
```
9. **Deploy locust worker profile.** From the /ymls/ folder execute the worker deployment yml
```sh
k create -f create-deployment-worker.yml
```
10. **Port forward master.** This will expose the locust ui on 8089 to your preferred port and to run the load test.
```sh
kubectl port-forward {master pod name} 8089:8089 -n syncloadtest
```
