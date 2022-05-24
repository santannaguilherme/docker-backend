import docker, datetime
from starlette.responses import JSONResponse
from Config import Configurações

CLIENT = docker.Client(base_url="tcp://{}:{}".format(Configurações.DOCKER_IP, Configurações.DOCKER_PORT))

async def CreateImagem(parametros):
    imagemCriada = None
    mensagem = []
    try:
        parm = await parametros.json()
    except:
        return JSONResponse({"Status":"O corpo da mensagem esta vazio!"}, status_code=400)

    try:
        tag = parm["tag"] if ('tag' in parm) and (parm["tag"])  else 'latest'
        imagemCriada = CLIENT.pull(parm["name"], tag=tag)
    except Exception as e:
        return JSONResponse({"Error": "Error não conhecido: {0}".format(e.args[0])}, status_code=500)   
    
    if imagemCriada != None:
        mensagem.append({"Status":"Baixado nova imagem '{0}', versão: '{1}'".format(parm["name"], tag)})

    return JSONResponse(mensagem, status_code=200)

def GetImagemByID(parametros):
    imagem_id = parametros.path_params['image_id']
    mensagem = None
    try:
        imagens = CLIENT.images()
        for imagem in imagens:
            try:
                if(imagem["Id"].split(":")[1] == imagem_id):
                    nome, tag = imagem["RepoTags"][0].split(":")
                    mensagem = {
                        "Id": imagem["Id"].split(":")[1],
                        "Tag": tag,
                        "Name": nome,
                        "Created": imagem["Created"]
                    }                    
                    break
            except Exception as e :
                return JSONResponse("Error ao ler as imagens: {0}".format(e), status_code=500)
        
    except Exception as e :
        return JSONResponse({"Error":"Error inesperado, {0}".format(e)}, status_code=500)
    
    return JSONResponse(mensagem, status_code=200)

def GetImagemList(parametros):
    imagens = None
    mensagem = []

    try:
        imagens = CLIENT.images()
    except Exception as e :
        return JSONResponse({"Error":"Error ao listar as imagens {0} ".format(e)}, status_code=500)

    for image in imagens:
        try:
            nome, tag = image["RepoTags"][0].split(":")
            mensagem.append(
                {
                    "Id": image["Id"].split(":")[1],
                    "Tag": tag,
                    "Name": nome,
                    "Created": image["Created"]
                }
            )
        except :
            return JSONResponse({"Error":"Error ao ler os dados das imagens {0} ".format(e)}, status_code=500)
        
    
    return JSONResponse(mensagem, status_code=200)

def DeleteImagemByID(parametros):
    imagem_id = parametros.path_params['image_id']
    del_imagem = None

    imagens = CLIENT.images()
    for imagem in imagens:
        try:
            if(imagem["Id"].split(":")[1] == imagem_id):
                del_imagem = imagem
                CLIENT.remove_image(imagem, force=True)
        except Exception as e :
            return JSONResponse({"Error":"Error ao deletar a imagem: {0}. Excessão: {1}".format(imagem_id, e)}, status_code=500)

    if(del_imagem != None):
        return JSONResponse({"Imagem deletada": del_imagem["RepoTags"]}, status_code=200)
    else:
        return JSONResponse({"Imagem não encontrada": imagem_id}, status_code=404)

def DeleteImagens(parametros):
    imagens = CLIENT.images()
    mensagem = []
    for imagem in imagens:
        name_tag = imagem["RepoTags"][0]
        print("Deleting image: {0}".format(name_tag))
        CLIENT.remove_image(imagem, force=True)
        mensagem.append(name_tag)

    return JSONResponse({"Deleted":mensagem}, status_code=200)
