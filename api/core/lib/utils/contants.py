from dataclasses import dataclass

@dataclass(frozen=True)
class DbParameters:
    HOST: str
    DATABASE: str
    USER: str
    PASSWORD: str