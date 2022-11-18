
#Jupyter Lab environment based on official tensorflow-gpu latest image  
  
Steps  
  
``` bash  
cd to the location of this readme  
```  
  
##Use if you have an NVIDIA GPU
``` bash  
sudo docker pull tensorflow/tensorflow:latest-gpu  
sudo docker build -f jupyter/gpuDockerfile -t tf-jupyter-lab .  
```  
  
##Use for cpu only
``` bash  
sudo docker pull tensorflow/tensorflow:latest  
sudo docker build -f jupyter/cpuDockerfile -t tf-jupyter-lab .  
```  
  
##to launch a container
``` bash  
sudo docker run -it --gpus all -p 14532:14532 -v ./data:/tf tf-jupyter-lab  
```  
  
access env through browser localhost:14532   
copy paste token from terminal  



#db swarm  
##postgres
``` bash  
sudo docker pull postgres  
sudo docker build -f postgres/Dockerfile -t postgresgis .  
```  

##PGAdmin  
``` bash  
sudo docker pull dpage/pgadmin4  
```  

##Start db swarm
``` bash  
sudo docker-compose -f docker-swarm.yaml up -d  
```  


