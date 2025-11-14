import os
import json
import hashlib
import hmac
import re
from pathlib import Path
from datetime import datetime

# Ruta del archivo de usuarios
USERS_FILE = 'data/users.json'

def validate_password_strength(password: str) -> dict:
    """
    Validar fortaleza de la contraseña.
    Requiere:
    - Mínimo 8 caracteres
    - Al menos 1 mayúscula
    - Al menos 1 minúscula
    - Al menos 1 número
    - Al menos 1 carácter especial (!@#$%^&*)
    
    Retorna: {'valid': bool, 'message': str}
    """
    errors = []
    
    if len(password) < 8:
        errors.append('mínimo 8 caracteres')
    
    if not re.search(r'[A-Z]', password):
        errors.append('al menos 1 mayúscula (A-Z)')
    
    if not re.search(r'[a-z]', password):
        errors.append('al menos 1 minúscula (a-z)')
    
    if not re.search(r'[0-9]', password):
        errors.append('al menos 1 número (0-9)')
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        errors.append('al menos 1 carácter especial (!@#$%^&*)')
    
    if errors:
        error_msg = ', '.join(errors)
        return {'valid': False, 'message': f'La contraseña debe tener: {error_msg}'}
    
    return {'valid': True, 'message': 'Contraseña válida'}

def hash_password(password: str) -> str:
    """Hashear contraseña con SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def ensure_users_file():
    """Crear archivo de usuarios si no existe."""
    Path('data').mkdir(exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

def user_exists(username: str) -> bool:
    """Verificar si un usuario existe."""
    ensure_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    return username in users

def register_user(username: str, email: str, password: str) -> dict:
    """
    Registrar un nuevo usuario.
    Retorna: {'success': bool, 'message': str}
    """
    ensure_users_file()
    
    # Validaciones
    if len(username) < 3:
        return {'success': False, 'message': 'El usuario debe tener al menos 3 caracteres'}
    
    # Validar fortaleza de contraseña
    pwd_validation = validate_password_strength(password)
    if not pwd_validation['valid']:
        return {'success': False, 'message': pwd_validation['message']}
    
    if '@' not in email or '.' not in email:
        return {'success': False, 'message': 'Email inválido'}
    
    # Leer usuarios actuales
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    # Verificar si el usuario ya existe
    if username in users:
        return {'success': False, 'message': 'El usuario ya existe'}
    
    # Verificar si el email ya está registrado
    for user_data in users.values():
        if user_data['email'] == email:
            return {'success': False, 'message': 'El email ya está registrado'}
    
    # Crear nuevo usuario
    users[username] = {
        'email': email,
        'password_hash': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    
    # Guardar usuarios
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return {'success': True, 'message': f'Usuario "{username}" registrado exitosamente'}

def login_user(username: str, password: str) -> dict:
    """
    Verificar credenciales de login.
    Retorna: {'success': bool, 'message': str, 'user': str}
    """
    ensure_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if username not in users:
        return {'success': False, 'message': 'Usuario o contraseña incorrectos'}
    
    user_data = users[username]
    password_hash = hash_password(password)
    
    if user_data['password_hash'] != password_hash:
        return {'success': False, 'message': 'Usuario o contraseña incorrectos'}
    
    # Actualizar último login
    user_data['last_login'] = datetime.now().isoformat()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return {'success': True, 'message': f'Bienvenido {username}', 'user': username}

def get_user_info(username: str) -> dict:
    """Obtener información del usuario."""
    ensure_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if username not in users:
        return None
    
    user_data = users[username]
    return {
        'username': username,
        'email': user_data['email'],
        'created_at': user_data['created_at'],
        'last_login': user_data['last_login'],
        'is_admin': user_data.get('is_admin', False)
    }

def update_password(username: str, old_password: str, new_password: str) -> dict:
    """Cambiar contraseña de un usuario."""
    ensure_users_file()
    
    # Validar fortaleza de contraseña
    pwd_validation = validate_password_strength(new_password)
    if not pwd_validation['valid']:
        return {'success': False, 'message': pwd_validation['message']}
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if username not in users:
        return {'success': False, 'message': 'Usuario no encontrado'}
    
    user_data = users[username]
    
    # Verificar contraseña anterior
    if user_data['password_hash'] != hash_password(old_password):
        return {'success': False, 'message': 'La contraseña anterior es incorrecta'}
    
    # Actualizar contraseña
    user_data['password_hash'] = hash_password(new_password)
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return {'success': True, 'message': 'Contraseña actualizada exitosamente'}


def is_admin(username: str) -> bool:
    """Verifica si el usuario es administrador."""
    ensure_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if username not in users:
        return False
    return users[username].get('is_admin', False)


def set_user_admin(username: str, make_admin: bool) -> dict:
    """Asigna o remueve permisos de administrador a un usuario.

    Retorna {'success': bool, 'message': str}.
    """
    ensure_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if username not in users:
        return {'success': False, 'message': 'Usuario no encontrado'}
    users[username]['is_admin'] = bool(make_admin)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    return {'success': True, 'message': f'Usuario "{username}" actualizado is_admin={make_admin}'}

def list_all_users() -> list:
    """Listar todos los usuarios (sin contraseñas)."""
    ensure_users_file()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    return [
        {
            'username': username,
            'email': user_data['email'],
            'created_at': user_data['created_at'],
            'last_login': user_data['last_login']
        }
        for username, user_data in users.items()
    ]
