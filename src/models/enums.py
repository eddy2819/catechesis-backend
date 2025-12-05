from enum import Enum

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

