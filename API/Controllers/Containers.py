import docker, datetime
from starlette.responses import JSONResponse
from Config import Configurações

CLIENT = docker.Client(base_url="tcp://{}:{}".format(Configurações.DOCKER_IP, Configurações.DOCKER_PORT))

async def ExecuteContainer(parametros):
    mensagem = []
    container = None
    container_imagem = None
    try:       
        param = await parametros.json()   
        container_imagem = param["image"]
    except:
        return JSONResponse({"Error": "Bad request - missing \"image\" on body"}, status_code=400)
    
    container_name = param["name"] if 'name' in param else None
    container_port = param["port"] if 'port' in param else None
    container_env  = {"User" : param["env"]  if 'env'  in param else None}

    if container_port != None:
        external_port, internal_port = container_port.split(":")
    try:
        #criacao do container
        container = CLIENT.create_container( image=container_imagem, 
                                                    detach=True, 
                                                    name=container_name,
                                                    host_config=CLIENT.create_host_config(port_bindings={internal_port:external_port}),
                                                    environment=container_env)
        
        if(container != None): # inicia o container
            CLIENT.start(container["Id"])
    except Exception as e:
        return JSONResponse({"Error":"Error ao criar o container com a imagem {0}. Excessão: {1}".format(container_imagem, e)}, status_code=500)   

    if container != None:
        mensagem.append({"Status":"Container criado com o ID: {0}".format(container["Id"])})

    return JSONResponse(mensagem, status_code=200)

def GetContainerByID(parametros):
    container_id = parametros.path_params['container_id']
    container_obj = None
    mensagem = []

    try:
        containers = CLIENT.containers()
        for container in containers:
            if container["Id"] == container_id:
                container_obj = container
                break
    except Exception as e :
        return JSONResponse({"Error":"Error geting container {0} ".format(e)}, status_code=404)

    mensagem.append(
        {
            "Id": container_obj["Id"],
            "Image": container_obj["Image"],
            "Name": container_obj["Names"][0],            
            "Created": container_obj["Created"],
            "State": container_obj["State"],
            "Staus": container_obj["Status"],
            "Ports": container_obj["Ports"],
            "NetworkPorts": container_obj["NetworkSettings"]["Networks"]
        }
    )
    
    return JSONResponse(mensagem, status_code=200)

def GetContainerList(parametros):
    containers = None
    mensagem = []

    try:
        containers = CLIENT.containers()
        for container_obj in containers:  
            mensagem.append(
                {
                    "Id": container_obj["Id"],
                    "Image": container_obj["Image"],
                    "Name": container_obj["Names"][0],            
                    "Created": container_obj["Created"],
                    "State": container_obj["State"],
                    "Status": container_obj["Status"],
                    "Ports": container_obj["Ports"],
                    "NetworkPorts": container_obj["NetworkSettings"]["Networks"]
                }
            )
    except Exception as e :
        return JSONResponse({"Error":"Error listing all containers {0}.".format(e)}, status_code=404)
    
    return JSONResponse(mensagem, status_code=200)

def DeleteContainerbyID(parametros):
    container_id = parametros.path_params['container_id']
    bDeleted = False

    try:
        containers = CLIENT.containers()
        for container in containers:
            if(container["Id"] == container_id):
                CLIENT.stop(container)
                CLIENT.remove_container(container)
                bDeleted = True
                break
    except Exception as e :        
            return JSONResponse({"Error": "Error ao deletar o container '{0}'. Exception: '{1}'".format(container_id, e)}, status_code=500)          
    
    if(bDeleted):
        return JSONResponse({"Status": "Container deletado, ID: {0}.".format(container_id)}, status_code=200)
    else:
        return JSONResponse({"Error": "Container não encontrado - ID: '{0}'".format(container_id)}, status_code=404)

def DeleteContainers(parametros):
    containers = CLIENT.containers()
    mensagem = []
    for container in containers:
        container_del = container
        CLIENT.stop(container)
        CLIENT.remove_container(container)
        mensagem.append({"Deleting container": "{0}".format(container_del["Id"]), "Name": "{0}".format(container_del["Names"][0])})

    return JSONResponse({"Deleted":mensagem}, status_code=200)