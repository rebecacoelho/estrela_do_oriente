from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="|Estrela do Oriente| API",
        default_version="v1",
        description="""
        ## Autenticação e Permissões

        - Para acessar os endpoints desta API é necessário autenticação JWT.
        - Apenas **usuários autenticados como superusuário** ou aqueles que possuem um
          objeto **Diretor** vinculado ao seu usuário terão permissão de **CRUD** sobre Alunos.
        - Usuários comuns podem se registrar via `/register/`, mas não terão acesso aos endpoints de Alunos
          até serem promovidos a **Diretor**.
        - Recomenda-se logar com um usuário superusuário para criar e gerenciar diretores.

        ### Fluxo sugerido:
        1. Criar usuário normal via `/register/` ou `createsuperuser`.
        2. Promover esse usuário criando um objeto `Diretor` vinculado a ele.
        3. Usar o token JWT desse Diretor para acessar os endpoints de `Alunos`.

        ### Endpoints Principais
        - `/api/alunos/`: CRUD de Alunos (Acesso restrito a Diretores e Superusuários)
        - `/api/documentos/`: CRUD de Documentos (Acesso restrito a Diretores e Superusuários)
        - `/api/responsaveis/`: CRUD de Responsáveis (Acesso restrito a Diretores e Superusuários)
        - `/api/diretores/`: CRUD de Diretores (Acesso restrito a Superusuários)
        - `/api/register/`: Registro de novos usuários (Acesso público)
        - `/api/token/`: Obtenção de token JWT (Acesso público)
        - `/api/token/refresh/`: Refresh de token JWT (Acesso público)
        ## Documentação Interativa
        - Swagger UI: `/api/swagger/`
        - ReDoc: `/api/redoc/`
        
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@EstrelaDoOriente.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)