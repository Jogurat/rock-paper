import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.choice import Choice


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(unique=True)

    player_matches: Mapped[list["PlayerMatch"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )

    matches: Mapped[list["Match"]] = relationship(
        "Match",
        secondary="player_matches",
        back_populates="players",
        overlaps="player_matches",
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    completed: Mapped[bool] = mapped_column(default=False)

    player_matches: Mapped[list["PlayerMatch"]] = relationship(
        back_populates="match", cascade="all, delete-orphan"
    )

    players: Mapped[list["Player"]] = relationship(
        "Player",
        secondary="player_matches",
        back_populates="matches",
        overlaps="player_matches",
    )

    winner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("players.id")
    )
    winner: Mapped["Player"] = relationship(foreign_keys=[winner_id])

    def add_player(self, player: "Player", move: "Choice"):
        self.player_matches.append(PlayerMatch(player=player, move=move))


class PlayerMatch(Base):
    __tablename__ = "player_matches"

    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("players.id"), primary_key=True
    )
    match_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matches.id"), primary_key=True
    )

    move: Mapped["Choice"]

    player: Mapped["Player"] = relationship(
        back_populates="player_matches", overlaps="matches, players"
    )
    match: Mapped["Match"] = relationship(
        back_populates="player_matches", overlaps="players, matches"
    )
