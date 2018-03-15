class RepositoryException(Exception):
    pass


class EntityNotFound(RepositoryException):
    pass


class DuplicateEntity(RepositoryException):
    pass
