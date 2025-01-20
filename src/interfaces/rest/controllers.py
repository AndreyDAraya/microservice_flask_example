from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from

from src.application.use_cases.user_use_cases import CreateUserDTO, UpdateUserDTO, UserUseCases
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

api = Blueprint('api', __name__)
user_repository = SQLAlchemyUserRepository()
user_use_cases = UserUseCases(user_repository)

@api.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Crear un nuevo usuario',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'}
                },
                'required': ['email', 'password', 'first_name', 'last_name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente'
        },
        400: {
            'description': 'Datos inválidos'
        }
    }
})
def create_user():
    """Crea un nuevo usuario"""
    data = request.get_json()
    try:
        user_dto = CreateUserDTO(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user = user_use_cases.create_user(user_dto)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError:
        return jsonify({'error': 'Datos inválidos'}), 400

@api.route('/users', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'summary': 'Obtener todos los usuarios',
    'responses': {
        200: {
            'description': 'Lista de usuarios'
        },
        401: {
            'description': 'No autorizado - Token JWT inválido o expirado'
        }
    },
    'security': [{'Bearer': []}]
})
def get_users():
    """Obtiene todos los usuarios"""
    print("Obteniendo todos los usuarios")
    print("Token JWT:", get_jwt_identity())
    users = user_use_cases.get_all_users()
    print("Usuarios:", users)
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active
    } for user in users])

@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'summary': 'Obtener un usuario por ID',
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario encontrado'
        },
        404: {
            'description': 'Usuario no encontrado'
        }
    },
    'security': [{'Bearer': []}]
})
def get_user(user_id):
    """Obtiene un usuario por su ID"""
    try:
        user = user_use_cases.get_user(user_id)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active
        })
    except ValueError:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@api.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'summary': 'Actualizar un usuario',
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'type': 'integer',
            'required': True
        },
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {'type': 'string', 'example': 'John'},
                    'last_name': {'type': 'string', 'example': 'Doe'}
                },
                'required': ['first_name', 'last_name']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario actualizado'
        },
        404: {
            'description': 'Usuario no encontrado'
        }
    },
    'security': [{'Bearer': []}]
})
def update_user(user_id):
    """Actualiza un usuario"""
    try:
        data = request.get_json()
        user_dto = UpdateUserDTO(
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user = user_use_cases.update_user(user_id, user_dto)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active
        })
    except ValueError:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except KeyError:
        return jsonify({'error': 'Datos inválidos'}), 400

@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'summary': 'Eliminar un usuario',
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        204: {
            'description': 'Usuario eliminado'
        },
        404: {
            'description': 'Usuario no encontrado'
        }
    },
    'security': [{'Bearer': []}]
})
def delete_user(user_id):
    """Elimina un usuario"""
    try:
        user_use_cases.delete_user(user_id)
        return '', 204
    except ValueError:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@api.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Iniciar sesión y obtener token JWT',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'example': 'test@example.com'},
                    'password': {'type': 'string', 'example': 'test123'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'Token JWT para usar en el header Authorization con formato: Bearer {token}'
                    }
                }
            }
        },
        401: {
            'description': 'Credenciales inválidas'
        }
    }
})
def login():
    """Inicia sesión y retorna un token JWT"""
    data = request.get_json()
    try:
        user = user_repository.get_by_email(data['email'])
        if user and user.password == data['password']:  # En una implementación real, verificar hash
            access_token = create_access_token(identity=str(user.id))
            return jsonify({'access_token': f'{access_token}'})
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except KeyError:
        return jsonify({'error': 'Datos inválidos'}), 400