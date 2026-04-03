class DomainError(Exception):
    """Base class for domain errors"""
    pass

class QuizNotFoundError(DomainError):
    pass

class QuestionNotFoundError(DomainError):
    pass

class QuizPermissionError(DomainError):
    pass

class DatabaseError(DomainError):
    pass