from sqlalchemy.orm import DeclarativeBase;
from sqlalchemy import Enum;
from sqlalchemy import DateTime;
from datetime import datetime;
from sqlalchemy import JSON;
from sqlalchemy.dialects.mysql import INTEGER

class Base(DeclarativeBase): # Classe dentro do projeto que serve como intermediária; Aqui poderíamos alterar padrões para todos nossos models/classes específicas ao mesmo tempo 
    pass

class Consultation(Base):
    __tablename__ = "consulta"

    id: Mapped[int] = mapped_column(    # Mapped é uma estrutura/tipo fornecido pelo SQLAlchemy para indicar: "Este atributo Python está sendo mapeado para uma coluna/atributo persistido pelo ORM."
        INTEGER(unsigned=True),         # mapped_column() é uma função do SQLAlchemy usada para declarar as características da coluna que será mapeada para o banco.
        primary_key=True,               # unsigned: Esse inteiro não pode ter sinal negativo."
        autoincrement=True
    )

    indicador: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
    Enum("ip", "dominio", "hash"),
    nullable=False
    )

    fonte: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    dataConsulta: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False
    )

    resultado: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )