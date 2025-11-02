#### Eclesiastes 3:1 RV60


### TAREAS PARA EL CHALLENGE

1. Configuración Inicial
- Crear estructura de carpetas del proyecto
- Configurar requirements.txt con dependencias
- Crear archivo de variables de entorno
- Inicializar git y crear .gitignore

2. Base de Datos y Mixins
- Implementar TimestampMixin para created_at y updated_at (Realizaddo en database/mixins.py)
- Implementar SoftDeleteMixin para borrado lógico (Realizaddo en database/mixins.py .Marca los registros como borrados sin borrarlos)
- Configurar SQLAlchemy con soporte asíncrono (Configurado en database/sessio.py)
- Crear Base para los modelos (database/base.py)

3. Modelos
- Crear modelo User (Creado en models/user.py )
- Crear modelo Post con relación 1:N a User (Creado en models/post con la relacion 1:N con los Users)
- Crear modelo Comment con relación 1:N a Post (CreAdo en models/comment con la realcion 1:N con Post)
- Crear modelo Tag con relación N:M a Post (Creado aun sin la relacion )
- Implementar tabla intermedia para Post-Tag (Aun por hacerse)

4. Migraciones con Alembic
- Inicializar Alembic (Inicializado sin problemas, correcion de errores en los models)
- Crear migración inicial con modelos base(Creada con algunas relaciones, paso a hacer la segunda con las relaciones restantes)
- Crear segunda migración agregando nuevos campos o relaciones

5. Schemas Pydantic
- Schemas para User con validaciones de email (Realizado en app/schemas/user)
- Schemas para Post con validaciones de longitud (Realizado en app/schemas/post)
- Schemas para Comment (Listo en app/schemas/comment)
- Schemas para Tag(app/schemas/tag)(Realizado en app/schemas/tag)
- Schemas de respuesta con relaciones (aun falta)

6. Autenticación y Seguridad
- Implementar hash de contraseñas
- Crear sistema de tokens JWT
- Endpoint de registro de usuarios
- Endpoint de login
- Dependencia para verificar usuarios autenticados

7. Routers y Endpoints
- Router de autenticación
- Router de usuarios con CRUD completo
- Router de posts con CRUD completo
- Router de comments con CRUD completo
- Router de tags con CRUD completo
- Implementar paginación en listados
- Implementar sistema de permisos por propietario

8. Middleware
- Crear middleware para registrar tiempo de respuesta
- Integrar middleware en la aplicación

9. Configuración Principal
- Crear main.py con configuración de FastAPI
- Integrar todos los routers
- Configurar CORS si es necesario
- Configurar manejo de errores

10. Extras
- Implementar tests básicos
- Documentar endpoints importantes
- Verificar que soft delete funcione en queries

