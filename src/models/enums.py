from enum import Enum



class UserRole(str, Enum):
    admin = "admin"
    parroco = "parroco"
    catequista = "catequista"
    secretario = "secretario"
    auxiliar = "auxiliar"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class CatechistRole(str, Enum):
    coordinador = "coordinador"
    catequista = "catequista"
    secretario = "secretario"
    auxiliar = "auxiliar"


class CatechistStatus(str, Enum):
    activo = "activo"
    inactivo = "inactivo"
    retirado = "retirado"


class StudentStatus(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class AttendanceStatus(str, Enum):
    presente = "presente"
    ausente = "ausente"
    justificado = "justificado"
    tarde = "tarde"

