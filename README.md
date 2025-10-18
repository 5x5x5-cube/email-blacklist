# API de Lista Negra

Microservicio para gestionar listas negras de correos electrónicos en el sistema. Construido con Flask y PostgreSQL siguiendo un patrón de arquitectura limpia.

## Características

- ✅ Agregar correos electrónicos a una lista negra global
- ✅ Verificar si un correo electrónico está en la lista negra
- ✅ Seguimiento automático de direcciones IP (soporta Elastic Beanstalk)
- ✅ Autenticación con Bearer token
- ✅ Diseño de API RESTful
- ✅ Arquitectura limpia con patrón de repositorio

## Stack Tecnológico

- **Python 3.10+**
- **Flask 3.0**: Micro framework web
- **Flask-SQLAlchemy**: ORM para operaciones de base de datos
- **Flask-RESTful**: Desarrollo de API REST
- **Flask-Marshmallow**: Serialización/deserialización de objetos
- **Flask-JWT-Extended**: Manejo de tokens JWT
- **Flask-CORS**: Soporte para Cross-Origin Resource Sharing
- **PostgreSQL 14**: Base de datos relacional
- **Poetry**: Gestión de dependencias
- **Docker & Docker Compose**: Contenedorización

## Estructura del Proyecto

```
blacklist_app/
├── src/
│   ├── db/
│   │   ├── database.py              # Configuración de BD y gestión de sesiones
│   │   └── models.py                # Modelos SQLAlchemy (tabla Blacklist)
│   ├── models/
│   │   ├── blacklist.py             # Esquemas Marshmallow para validación
│   │   └── errors.py                # Excepciones personalizadas
│   ├── repositories/
│   │   └── blacklist_repository.py  # Capa de acceso a datos
│   ├── services/
│   │   └── blacklist_service.py     # Capa de lógica de negocio
│   ├── routes/
│   │   └── blacklist_router.py      # Endpoints de la API (Blueprint)
│   ├── middleware/
│   │   └── auth_middleware.py       # Autenticación con Bearer token
│   ├── utils/
│   │   └── validation.py            # Utilidades de validación (IP, UUID)
│   └── main.py                      # Inicialización de la aplicación Flask
├── tests/
│   ├── unit/                        # Pruebas unitarias
│   └── integration/                 # Pruebas de integración
├── .env                             # Variables de entorno (no en git)
├── .env.example                     # Plantilla de variables de entorno
├── docker-compose.yml               # Contenedor PostgreSQL
├── Dockerfile                       # Contenedor de la aplicación
├── Makefile                         # Comandos de automatización
└── pyproject.toml                   # Dependencias de Poetry
```

## Inicio Rápido

### Prerequisitos

- Python 3.10 o superior
- Docker y Docker Compose
- Poetry (se instalará con make setup)

### 1. Instalar Dependencias

```bash
# Instalar Poetry y dependencias del proyecto
make setup
```

### 2. Configurar Entorno

El archivo `.env` ya está configurado con:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/blacklist_db
BEARER_TOKEN=6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ
FLASK_ENV=development
FLASK_DEBUG=1
```

> **Nota:** El bearer token es generado aleatoriamente y guardado en `.env`. ¡Manténlo seguro!

### 3. Iniciar PostgreSQL

```bash
# Iniciar PostgreSQL en Docker
make docker-compose-up

# O manualmente
docker compose up -d
```

Esto iniciará PostgreSQL en el puerto **5433** (para evitar conflictos con instancias existentes de PostgreSQL).

### 4. Ejecutar la Aplicación

```bash
# Ejecutar aplicación Flask localmente con recarga automática
make run
```

La API estará disponible en: **http://localhost:5001**

> **¿Puerto 5001?** Usamos el puerto 5001 en lugar del 5000 porque macOS Control Center usa el puerto 5000.

## Comandos de Desarrollo

### Comandos Make

```bash
# Configuración e Instalación
make setup          # Instalar Poetry y todas las dependencias
make install        # Instalar solo dependencias

# Ejecución
make run            # Ejecutar aplicación Flask localmente (con recarga automática)

# Pruebas
make test           # Ejecutar todas las pruebas
make test-unit      # Ejecutar solo pruebas unitarias
make test-cov       # Ejecutar pruebas con reporte de cobertura

# Docker
make docker-compose-up       # Iniciar PostgreSQL
make docker-compose-down     # Detener PostgreSQL
make docker-compose-build    # Reconstruir e iniciar todos los servicios

# Imagen Docker
make docker-build   # Construir imagen Docker
make docker-run     # Ejecutar contenedor Docker

# Limpieza
make clean          # Eliminar archivos de caché y artefactos
```

### Ejecutar Pruebas

```bash
# Todas las pruebas
make test

# Solo pruebas unitarias
make test-unit

# Con cobertura
make test-cov
```

## Base de Datos

### Información de Conexión

| Configuración | Valor |
|---------------|-------|
| **Host** | `localhost` |
| **Puerto** | `5433` |
| **Base de datos** | `blacklist_db` |
| **Usuario** | `postgres` |
| **Contraseña** | `postgres` |
| **Cadena de conexión** | `postgresql://postgres:postgres@localhost:5433/blacklist_db` |

### Esquema de Base de Datos

**Tabla Blacklist**

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | String (UUID) | Primary Key, Indexed | Identificador único |
| email | String (255) | Unique, Indexed, Not Null | Dirección de correo |
| app_uuid | String (UUID) | Indexed, Not Null | Identificador de aplicación |
| blocked_reason | String (255) | Nullable | Razón del bloqueo |
| ip_address | String (45) | Not Null | Dirección IP del solicitante |
| created_at | DateTime | Not Null, Default: now() | Marca de tiempo |

## Endpoints de la API

### Autenticación

Todos los endpoints (excepto `/blacklists/ping`) requieren autenticación con Bearer token:

```
Authorization: Bearer {{TOKEN}}
```

### Resumen de Endpoints

| Método | Endpoint | Auth Requerida | Descripción |
|--------|----------|----------------|-------------|
| GET | `/blacklists/ping` | ❌ No | Health check |
| POST | `/blacklists` | ✅ Sí | Agregar correo a lista negra |
| GET | `/blacklists/<email>` | ✅ Sí | Verificar si correo está en lista negra |

### POST /blacklists

Agregar un correo electrónico a la lista negra global.

**Petición:**
```bash
curl -X POST http://localhost:5001/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ" \
  -d '{
    "email": "spammer@example.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Actividad de spam detectada"
  }'
```

**Respuesta (201):**
```json
{
  "message": "Email spammer@example.com added to blacklist successfully",
  "id": "437116b6-d37d-43c5-be98-173b138e226e",
  "email": "spammer@example.com",
  "created_at": "2025-10-13T18:59:28.773314"
}
```

**Cuerpo de la Petición:**

| Campo | Tipo | Requerido | Long. Máx. | Descripción |
|-------|------|-----------|------------|-------------|
| email | string | ✅ Sí | - | Dirección de correo válida |
| app_uuid | string | ✅ Sí | - | Formato UUID válido |
| blocked_reason | string | ⚪ Opcional | 255 | Razón del bloqueo |

### GET /blacklists/<email>

Verificar si un correo electrónico está en la lista negra.

**Petición:**
```bash
curl http://localhost:5001/blacklists/spammer@example.com \
  -H "Authorization: Bearer 6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ"
```

**Respuesta (200):**
```json
{
  "is_blacklisted": true,
  "email": "spammer@example.com",
  "blocked_reason": "Actividad de spam detectada"
}
```

### GET /blacklists/ping

Endpoint de health check (no requiere autenticación).

**Petición:**
```bash
curl http://localhost:5001/blacklists/ping
```

**Respuesta (200):**
```json
{
  "message": "pong"
}
```

## Manejo de Errores

La API retorna códigos de estado HTTP estándar:

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos de petición inválidos o error de validación |
| 401 | Unauthorized | Autenticación faltante o inválida |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | El recurso ya existe (correo duplicado) |
| 500 | Internal Server Error | Error del servidor |

**Formato de Respuesta de Error:**
```json
{
  "error": "Tipo de Error",
  "message": "Mensaje de error detallado",
  "details": {
    "campo": ["Detalles del error de validación"]
  }
}
```

## Pruebas

### Estructura de Pruebas

```
tests/
├── unit/              # Pruebas unitarias (aisladas, sin dependencias externas)
```

### Ejecutar Pruebas

```bash
# Todas las pruebas
make test

# Solo pruebas unitarias (rápido)
make test-unit

# Con reporte de cobertura
make test-cov
```

## Arquitectura

Este proyecto sigue los principios de **Arquitectura Limpia**:

```
┌─────────────────────────────────────┐
│      Routes (Capa de API)           │  ← Flask Blueprints
├─────────────────────────────────────┤
│   Middleware (Capa de Auth)         │  ← Autenticación Bearer Token
├─────────────────────────────────────┤
│  Services (Lógica de Negocio)       │  ← Reglas de negocio core
├─────────────────────────────────────┤
│ Repositories (Acceso a Datos)       │  ← Operaciones de base de datos
├─────────────────────────────────────┤
│  Models (Capa de Base de Datos)     │  ← Modelos SQLAlchemy
└─────────────────────────────────────┘
```

**Beneficios:**
- ✅ Separación de responsabilidades
- ✅ Fácil de probar (cada capa puede probarse independientemente)
- ✅ Mantenible y escalable
- ✅ Lógica de negocio independiente de la base de datos
