from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from API.Controllers import Containers, Imagens

# Rotas das APIs
rotas = [
    #Imagems
    Route('/Images', Imagens.CreateImagem, name="CreateImagem", methods=["POST"]),
    Route('/Images', Imagens.GetImagemList, name="GetImagemList", methods=["GET"]),
    Route('/Images/{image_id:str}', Imagens.GetImagemByID, name="GetImagemByID", methods=["GET"]),
    Route('/Images/{image_id:str}', Imagens.DeleteImagemByID, name="DeleteImagemByID", methods=["DELETE"]),
    Route('/Images', Imagens.DeleteImagens, name="DeleteImagens", methods=["DELETE"]),

    #Containers
    Route('/Containers', Containers.ExecuteContainer, name="ExecuteContainer", methods=["POST"]),
    Route('/Containers', Containers.GetContainerList, name="GetContainerList", methods=["GET"]),
    Route('/Containers/{container_id:str}', Containers.GetContainerByID, name="GetContainerByID", methods=["GET"]),
    Route('/Containers/{container_id:str}', Containers.DeleteContainerbyID, name="DeleteContainerbyID", methods=["DELETE"]),
    Route('/Containers', Containers.DeleteContainers, name="DeleteContainers", methods=["DELETE"]),        
]

#Middleware para a liberação do CORS
middleware = [Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])]

#Print Startup
def Startup():
    print('Serviço iniciado!')

#Iniciação do Serviço via Starlette
app = Starlette(debug=True, on_startup=[Startup], routes=rotas, middleware=middleware)