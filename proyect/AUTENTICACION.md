# 🔐 Sistema de Autenticación y Gestión de Usuarios

## Descripción General

El Analizador de Tiros de la UEFA Champions League ahora incluye un **sistema completo de autenticación y gestión de usuarios** que protege los datos y proporciona una experiencia personalizada.

## 🎯 Características Principales

### 1. **Registro de Nuevos Usuarios**
- Crear una nueva cuenta con usuario, email y contraseña
- Validaciones automáticas:
  - Usuario mínimo 3 caracteres
  - **Contraseña mínimo 8 caracteres**
  - **Contraseña requiere 1 MAYÚSCULA**
  - **Contraseña requiere 1 minúscula**
  - **Contraseña requiere 1 número**
  - **Contraseña requiere 1 carácter especial (!@#$%^&*)**
  - Email válido (contiene @ y punto)
  - Validación de email único (no pueden existir dos cuentas con el mismo email)
  - Validación de usuario único (no pueden existir dos cuentas con el mismo usuario)

### 2. **Inicio de Sesión**
- Acceso seguro con usuario y contraseña
- Mensajes de error claros para credenciales incorrectas
- Registro automático del último acceso

### 3. **Gestión de Perfil**
- Ver información personal:
  - Usuario
  - Email registrado
  - Fecha de registro
  - Último acceso
- Cambiar contraseña de forma segura
- Validación de contraseña anterior

### 4. **Seguridad**
- Contraseñas hasheadas con SHA-256
- Protección contra fuerza bruta (validaciones en cliente)
- Archivo de usuarios protegido (.gitignore)
- Session state seguro en Streamlit

## 📂 Estructura de Archivos

```
data/
├── users.json          # Base de datos de usuarios (hasheadas)
└── sample_shots.csv    # Dataset de análisis

src/
├── auth.py             # Módulo de autenticación
├── app.py              # Aplicación principal
├── data.py             # Análisis de datos
└── visuals.py          # Visualizaciones
```

## 🔑 Módulo de Autenticación (`src/auth.py`)

### Funciones Principales

#### `hash_password(password: str) -> str`
Hashea una contraseña usando SHA-256.

```python
from src.auth import hash_password
hashed = hash_password("micontraseña123")
```

#### `register_user(username: str, email: str, password: str) -> dict`
Registra un nuevo usuario.

```python
from src.auth import register_user

result = register_user("juanperez", "juan@email.com", "mipass123")
# Retorna: {'success': bool, 'message': str}
```

#### `login_user(username: str, password: str) -> dict`
Verifica credenciales y devuelve información de usuario.

```python
from src.auth import login_user

result = login_user("juanperez", "mipass123")
# Retorna: {'success': bool, 'message': str, 'user': str}
```

#### `get_user_info(username: str) -> dict`
Obtiene información del usuario (sin contraseña).

```python
from src.auth import get_user_info

info = get_user_info("juanperez")
# Retorna: {'username': str, 'email': str, 'created_at': str, 'last_login': str}
```

#### `update_password(username: str, old_password: str, new_password: str) -> dict`
Cambia la contraseña de un usuario.

```python
from src.auth import update_password

result = update_password("juanperez", "mipass123", "nuevapass456")
# Retorna: {'success': bool, 'message': str}
```

#### `list_all_users() -> list`
Lista todos los usuarios registrados (sin contraseñas).

```python
from src.auth import list_all_users

usuarios = list_all_users()
# Retorna: [{'username': str, 'email': str, 'created_at': str, 'last_login': str}, ...]
```

## 🚀 Flujo de Uso

### Primer Acceso
1. Abrir la aplicación en `http://localhost:8501`
2. Hacer clic en la pestaña **"📝 Registrarse"**
3. Completar:
   - **Usuario**: (ej: juanperez) - mínimo 3 caracteres
   - **Email**: (ej: juan@email.com) - debe ser válido y único
   - **Contraseña**: (ej: MiPass123!) - debe cumplir requisitos de seguridad:
     - Mínimo 8 caracteres
     - Al menos 1 MAYÚSCULA (A-Z)
     - Al menos 1 minúscula (a-z)
     - Al menos 1 número (0-9)
     - Al menos 1 carácter especial (!@#$%^&*)
   - **Confirmar Contraseña**: debe coincidir exactamente
4. Hacer clic en **"✅ Registrarse"**
5. Aparecerá un mensaje de confirmación

### Login Subsecuentes
1. Abrir la aplicación
2. En la pestaña **"🔑 Iniciar Sesión"**:
   - Ingresar usuario
   - Ingresar contraseña
3. Hacer clic en **"✅ Iniciar Sesión"**
4. Se redirige automáticamente al panel de análisis

### Cambiar Contraseña
1. En la barra lateral izquierda, expandir **"⚙️ Opciones de Usuario"**
2. Expandir **"👤 Perfil (usuario)"**
3. Completar:
   - **Contraseña Actual**: contraseña anterior
   - **Nueva Contraseña**: nueva contraseña (mínimo 6 caracteres)
   - **Confirmar Nueva Contraseña**: confirmar
4. Hacer clic en **"Cambiar Contraseña"**

### Cerrar Sesión
1. Hacer clic en el botón **"👤 usuario (Salir)"** en la esquina superior derecha
2. Se redirige a la pantalla de login

## 📊 Estructura de `users.json`

```json
{
  "juanperez": {
    "email": "juan@email.com",
    "password_hash": "8b1a9953c4611296aaf7...",
    "created_at": "2025-11-12T15:30:45.123456",
    "last_login": "2025-11-12T16:45:30.987654"
  },
  "mariagarcia": {
    "email": "maria@email.com",
    "password_hash": "5d41402abc4b2a76b9719...",
    "created_at": "2025-11-12T14:20:10.654321",
    "last_login": "2025-11-12T15:10:20.111111"
  }
}
```

## ⚠️ Consideraciones de Seguridad

### Mejoras Implementadas
- ✅ Contraseñas hasheadas (SHA-256)
- ✅ Validación de entrada en cliente
- ✅ Archivo de usuarios en `.gitignore`
- ✅ Session state seguro en Streamlit
- ✅ Validaciones únicas (email y usuario)

### Recomendaciones para Producción
1. **HTTPS**: Implementar en servidor de producción
2. **Bcrypt**: Cambiar SHA-256 por bcrypt para mejor seguridad
3. **Base de Datos**: Migrar `users.json` a base de datos SQL con cifrado
4. **Rate Limiting**: Limitar intentos de login fallidos
5. **2FA**: Implementar autenticación de dos factores
6. **Auditoría**: Registrar todos los accesos e intentos fallidos
7. **Expiración de Sesión**: Implementar timeout automático

## 🔧 Configuración

### Variables de Entorno (Futura Expansión)
```bash
# .env
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=postgresql://usuario:pass@localhost/db
JWT_EXPIRATION=3600
```

## 📝 Ejemplo de Uso Completo

```python
from src.auth import register_user, login_user, get_user_info, update_password

# Registrar nuevo usuario
resultado = register_user("carlos2025", "carlos@ejemplo.com", "segura123")
print(resultado)
# {'success': True, 'message': 'Usuario "carlos2025" registrado exitosamente'}

# Intentar login
resultado = login_user("carlos2025", "segura123")
print(resultado)
# {'success': True, 'message': 'Bienvenido carlos2025', 'user': 'carlos2025'}

# Obtener información
info = get_user_info("carlos2025")
print(info)
# {'username': 'carlos2025', 'email': 'carlos@ejemplo.com', 'created_at': '...', 'last_login': '...'}

# Cambiar contraseña
resultado = update_password("carlos2025", "segura123", "nueva_segura456")
print(resultado)
# {'success': True, 'message': 'Contraseña actualizada exitosamente'}
```

## 🐛 Troubleshooting

### "El usuario ya existe"
- El nombre de usuario ya está registrado
- Solución: Usa otro nombre de usuario

### "El email ya está registrado"
- Otro usuario ya utiliza ese email
- Solución: Usa otro email o recupera tu cuenta

### "Usuario o contraseña incorrectos"
- Las credenciales no coinciden
- Solución: Verifica que escribiste correctamente usuario y contraseña

### "La contraseña debe tener al menos 6 caracteres"
- La contraseña es demasiado corta
- Solución: Usa una contraseña más larga

### "Las contraseñas no coinciden"
- Al cambiar contraseña, confirmación no coincide
- Solución: Asegúrate de escribir la misma contraseña en ambos campos

## 📞 Soporte

Para reportar problemas o sugerencias sobre el sistema de autenticación, contacta al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Última Actualización**: 12 de Noviembre de 2025  
**Autor**: GitHub Copilot
