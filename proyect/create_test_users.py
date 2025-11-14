#!/usr/bin/env python3
"""
Script para crear usuarios de prueba en la aplicación.
Uso: python create_test_users.py
"""

import sys
import os

# Asegurar que el proyecto está en sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.auth import register_user, list_all_users

def main():
    print("🔐 Creando usuarios de prueba...\n")
    
    # Usuario de prueba 1
    usuario1 = "demo"
    email1 = "demo@example.com"
    password1 = "demo123456"
    
    print(f"📝 Registrando usuario: {usuario1}")
    result1 = register_user(usuario1, email1, password1)
    print(f"   Resultado: {result1['message']}\n")
    
    # Usuario de prueba 2
    usuario2 = "admin"
    email2 = "admin@example.com"
    password2 = "admin123456"
    
    print(f"📝 Registrando usuario: {usuario2}")
    result2 = register_user(usuario2, email2, password2)
    print(f"   Resultado: {result2['message']}\n")
    
    # Listar usuarios
    print("📋 Usuarios registrados:")
    usuarios = list_all_users()
    for i, user in enumerate(usuarios, 1):
        print(f"   {i}. {user['username']} ({user['email']})")
        print(f"      Registrado: {user['created_at'][:10]}")
        if user['last_login']:
            print(f"      Último acceso: {user['last_login'][:10]}")
    
    print("\n✅ Usuarios de prueba creados exitosamente!")
    print(f"\n🚀 Credenciales de prueba:")
    print(f"   Usuario: {usuario1}")
    print(f"   Contraseña: {password1}")
    print(f"\n   Usuario: {usuario2}")
    print(f"   Contraseña: {password2}")

if __name__ == '__main__':
    main()
