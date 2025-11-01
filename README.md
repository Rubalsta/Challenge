
### TAREAS PARA EL CHALLENGE

1. Configuración Inicial
- Crear estructura de carpetas del proyecto
- Configurar requirements.txt con dependencias
- Crear archivo de variables de entorno
- Inicializar git y crear .gitignore

2. Base de Datos y Mixins
- Implementar TimestampMixin para created_at y updated_at
- Implementar SoftDeleteMixin para borrado lógico
- Configurar SQLAlchemy con soporte asíncrono
- Crear Base para los modelos

3. Modelos
- Crear modelo User
- Crear modelo Post con relación 1:N a User
- Crear modelo Comment con relación 1:N a Post
- Crear modelo Tag con relación N:M a Post
- Implementar tabla intermedia para Post-Tag

4. Migraciones con Alembic
- Inicializar Alembic
- Crear migración inicial con modelos base
- Crear segunda migración agregando nuevos campos o relaciones

5. Schemas Pydantic
- Schemas para User con validaciones de email
- Schemas para Post con validaciones de longitud
- Schemas para Comment
- Schemas para Tag
- Schemas de respuesta con relaciones

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

