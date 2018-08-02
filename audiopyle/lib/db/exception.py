class RepositoryException(Exception):
    """Generic repository exception"""
    pass


class EntityNotFound(RepositoryException):
    """Raised when calling for single entity and the entity was not found"""
    pass


class DuplicateEntity(RepositoryException):
    """Raised when doing insert and violating unique constraint"""
    pass
