from dataclasses import dataclass


@dataclass()
class Account:
    id: int
    title: str
    user: str
    site: str
    password: str


@dataclass()
class Admin:
    user: str
    password: str
