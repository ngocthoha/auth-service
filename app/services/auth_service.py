from enum import Enum
from typing import Dict, List, Set

from app.models.user import RoleEnum


class ResourceEnum(str, Enum):
    USERS = "users"
    SETTINGS = "settings"
    SERVICES = "services"


class ActionEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LIST = "list"


# Role-based access control matrix
# Define which roles can perform which actions on which resources
RBAC_MATRIX: Dict[RoleEnum, Dict[ResourceEnum, Set[ActionEnum]]] = {
    RoleEnum.ADMIN: {
        ResourceEnum.USERS: {
            ActionEnum.CREATE, ActionEnum.READ, ActionEnum.UPDATE, 
            ActionEnum.DELETE, ActionEnum.LIST
        },
        ResourceEnum.SETTINGS: {
            ActionEnum.READ, ActionEnum.UPDATE
        },
        ResourceEnum.SERVICES: {
            ActionEnum.CREATE, ActionEnum.READ, ActionEnum.UPDATE, 
            ActionEnum.DELETE, ActionEnum.LIST
        },
    },
    RoleEnum.USER: {
        ResourceEnum.USERS: {
            ActionEnum.READ
        },
        ResourceEnum.SETTINGS: {
            ActionEnum.READ
        },
        ResourceEnum.SERVICES: {
            ActionEnum.READ, ActionEnum.LIST
        },
    },
    RoleEnum.SERVICE: {
        ResourceEnum.USERS: {
            ActionEnum.READ, ActionEnum.LIST
        },
        ResourceEnum.SERVICES: {
            ActionEnum.READ
        },
    },
}


class AuthorizationService:
    @staticmethod
    def is_authorized(role: RoleEnum, resource: ResourceEnum, action: ActionEnum) -> bool:
        """
        Check if a role is authorized to perform an action on a resource
        """
        if role not in RBAC_MATRIX:
            return False
            
        if resource not in RBAC_MATRIX[role]:
            return False
            
        return action in RBAC_MATRIX[role][resource]
        
    @staticmethod
    def get_permitted_actions(role: RoleEnum, resource: ResourceEnum) -> List[ActionEnum]:
        """
        Get all actions that a role can perform on a resource
        """
        if role not in RBAC_MATRIX or resource not in RBAC_MATRIX[role]:
            return []
            
        return list(RBAC_MATRIX[role][resource])
        
    @staticmethod
    def get_permitted_resources(role: RoleEnum) -> List[ResourceEnum]:
        """
        Get all resources that a role has access to
        """
        if role not in RBAC_MATRIX:
            return []
            
        return list(RBAC_MATRIX[role].keys()) 