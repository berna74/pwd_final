# Sistema de Administración - Club de Tenis

Sistema completo de gestión para un club de tenis, desarrollado con Flask (backend) y Vue.js (frontend).

## 🎾 Funcionalidades

### Módulos Principales

1. **Socios**
   - Gestión completa de socios del club
   - Información personal (nombre, apellido, DNI, email, teléfono)
   - Fecha de inscripción
   - Asignación de cancha preferida
   - Asignación de instructor
   - Categorías múltiples por socio

2. **Canchas**
   - Administración de canchas disponibles
   - Tipo de superficie (polvo de ladrillo, césped, cemento, sintética)
   - Indicador de cancha techada

3. **Instructores**
   - Gestión de instructores del club
   - Especialidades (técnica, táctica, principiantes, etc.)
   - Información de contacto

4. **Categorías**
   - Tipos de membresía (Junior, Senior, Veterano, etc.)
   - Descripciones personalizables

## 🛠️ Tecnologías

### Backend
- **Flask** - Framework web Python
- **MySQL** - Base de datos
- **mysql-connector-python** - Conector de base de datos
- **Flask-CORS** - Manejo de CORS

### Frontend
- **Vue.js 3** - Framework JavaScript
- **TypeScript** - Tipado estático
- **Pinia** - State management
- **Vue Router** - Navegación
- **Axios** - Cliente HTTP
- **Vite** - Build tool

## 📦 Instalación

### Backend

1. Navegar al directorio del backend:
```bash
cd app/backend
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (crear archivo `.env`):
```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=club_tenis_db
DB_PORT=3306
```

5. Inicializar la base de datos:
```bash
python db_init.py
```

6. Ejecutar el servidor:
```bash
python run.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. Navegar al directorio del frontend:
```bash
cd app/frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar la URL del backend en `src/plugins/axios.ts` si es necesario

4. Ejecutar el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 🗃️ Estructura de la Base de Datos

### Tablas

- **SOCIOS**: Información de los socios del club
- **CANCHAS**: Canchas disponibles
- **INSTRUCTORES**: Instructores del club
- **CATEGORIAS**: Tipos de membresía
- **SOCIO_CATEGORIA**: Relación muchos a muchos entre socios y categorías

### Relaciones

- Un socio tiene una cancha preferida (muchos a uno)
- Un socio tiene un instructor asignado (muchos a uno)
- Un socio puede tener múltiples categorías (muchos a muchos)

## 🚀 API Endpoints

### Socios
- `GET /socios/` - Listar todos los socios
- `GET /socios/<id>` - Obtener un socio por ID
- `POST /socios/` - Crear un nuevo socio
- `PUT /socios/<id>` - Actualizar un socio
- `DELETE /socios/<id>` - Eliminar un socio

### Canchas
- `GET /canchas/` - Listar todas las canchas
- `GET /canchas/<id>` - Obtener una cancha por ID
- `POST /canchas/` - Crear una nueva cancha
- `PUT /canchas/<id>` - Actualizar una cancha
- `DELETE /canchas/<id>` - Eliminar una cancha

### Instructores
- `GET /instructores/` - Listar todos los instructores
- `GET /instructores/<id>` - Obtener un instructor por ID
- `POST /instructores/` - Crear un nuevo instructor
- `PUT /instructores/<id>` - Actualizar un instructor
- `DELETE /instructores/<id>` - Eliminar un instructor

### Categorías
- `GET /categorias/` - Listar todas las categorías
- `GET /categorias/<id>` - Obtener una categoría por ID
- `POST /categorias/` - Crear una nueva categoría
- `PUT /categorias/<id>` - Actualizar una categoría
- `DELETE /categorias/<id>` - Eliminar una categoría

## 📝 Datos de Ejemplo

El sistema incluye datos de ejemplo al inicializar la base de datos:

- 6 canchas con diferentes superficies
- 5 instructores con distintas especialidades
- 7 categorías de socios
- 8 socios de ejemplo

## 🔧 Desarrollo

### Estructura del Proyecto

```
app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   └── conect_db.py
│   │   └── modules/
│   │       ├── socios/
│   │       ├── canchas/
│   │       ├── instructores/
│   │       └── categoria/
│   ├── db_init.py
│   ├── db_rollback.py
│   ├── run.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── socios/
    │   │   ├── canchas/
    │   │   ├── instructores/
    │   │   └── categorias/
    │   ├── interfaces/
    │   ├── router/
    │   ├── stores/
    │   ├── views/
    │   └── App.vue
    └── package.json
```

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos.

## 👥 Autor

Proyecto adaptado de un sistema de gestión de inventario a un sistema de administración de club de tenis.
