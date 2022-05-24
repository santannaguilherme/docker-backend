# SmartTrack Docker

## Instalação:

[Obs]: Instale o python 3.6+ and pip, para realização das ferramentas abaixo e caso utilize o Windows, instalar o Docker Desktop e habilitar o "Expose daemon" nas configurações.

VirtualEnv:
```
pip install virtualenv
```

Criando um ambiente:
```
virtualenv -p python <Nome do Ambiente>
```

Inicializando o ambiente:
```
<Nome do Ambiente>\Scripts\activate.bat
```

Desligando o ambiente:
```
<Nome do Ambiente>\Scripts\deactivate.bat
```

## Dentro do ambiente, instale as ferramentas necessárrias:

Linux:
```
pip3 install -r requirements.txt
```

Instalando o Docker-py
```
pip3 install docker-py
```

Windows:
```
pip install -r requirements.txt
```

Instalando o Docker-py
```
pip install docker-py
```

## Executando a Aplicação dentro do Ambiente

Terminal:
```
uvicorn Application:app --port 8000 --reload
```