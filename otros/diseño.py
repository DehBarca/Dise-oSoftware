from dataclasses import dataclass
 
@dataclass(frozen=True)
class Usuario:
    id: str
    nombre: str
 
@dataclass(frozen=True)
class Plan:
    id: str
    nombre: str
    precio_mxn: float
    periodicidad: str  # "MENSUAL" | "ANUAL"
 
@dataclass
class Suscripcion:
    id: str
    usuario: Usuario
    plan: Plan
    activa: bool = False
 
    def activar(self) -> None:
        if self.activa:
            raise ValueError("La suscripción ya está activa")
        self.activa = True
 
    def cancelar(self) -> None:
        if not self.activa:
            raise ValueError("La suscripción ya está cancelada")
        self.activa = False