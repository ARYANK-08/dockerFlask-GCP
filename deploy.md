1. create requiements.txt
2. create dockerfile 
```
dockerfile

FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /todo-app

# Copy requirements first for caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy all files into the working directory
COPY . .

# Command to run the application
CMD ["python", "app.py"]

```
3. deploying simple flask app 
take care of port : 8080 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)  # Hardcoded port 8080

if not configured : expected error
```
Revision 'flaskimg-00001-nqv' is not ready and cannot serve traffic. The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout. This can happen when the container port is misconfigured or if the timeout is too short. The health check timeout can be extended. Logs for this revision might contain more information. Logs URL: Open Cloud Logging  For more troubleshooting guidance, see https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start
```


4. create new project eg:  flaskdeploydocker 
get the project id which is adjacent to it 

5. enable cloud run api and cloud build -> requires billing acc

6. install gcloud cli
gcloud init
gcloud config set project flaskdockerdeploy


gcloud artifacts repositories create flaskdocker --repository-format=docker --location=europe-west4 --description="FlaskDockerAPP" --immutable-tags --async

gcloud auth configure-docker europe-west4-docker.pkg.dev

adds config file 
add service account permissions to iam click on edit and give
object storage viewer permission 


gcloud builds submit --tag europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/flaskimg:flasktagnew                         


deploy to cloud run 
click on deploy container-> sevice

Deploy one revision from an existing container image
select  container url from artifacts image


Allow unauthenticated invocations
Tick this if you are creating a public API or website.


connect  your github to allow cicd push to github artifacts image automation builkding using docker

and if you want to run locally on docker 


 docker build . --tag europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/otherimg:othertag                                                

 django_docker_kubernetes\docker_kubernetes> docker run -p 8080:8080 europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/otherimg:othertag 

 