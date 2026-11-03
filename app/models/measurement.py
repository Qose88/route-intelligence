from datetime import datetime
from sqlalchemy import DateTime, Float,ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Measurement(Base):
    __tablename__ = "measurements"
# Unique identifier for each measurement
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    probe_id: Mapped[int] = mapped_column(
       ForeignKey("probes.id"),
       nullable=False,
    )
#destination id of the measurement
    destination_id: Mapped[int] = mapped_column(
       ForeignKey("destinations.id"),
       nullable=False,
    )
#measurement type (ping, traceroute, etc.)
    measurement_type : Mapped[str]=mapped_column(
       String(50),
       nullable=False,
    )
#timestamp of the measurement
    timestamp: Mapped[datetime] = mapped_column(
       DateTime,
       nullable=False,
    )
#packet sent
    packet_sent: Mapped[int | None] = mapped_column(
      Integer,
      nullable=True,
    )
#packet received
    packet_received: Mapped[int | None] = mapped_column(
      Integer,
      nullable=True,
    )
#packet loss
    packet_loss: Mapped[float | None] = mapped_column(
      Float,
      nullable=True,
    )
#latency_minimum
    latency_min: Mapped[float | None] = mapped_column(
      Float,
      nullable=True,
    )
#latency_average
    latency_avg: Mapped[float | None] = mapped_column(
      Float,
      nullable=True,
    )
#latency_maximum
    latency_max: Mapped[float | None] = mapped_column(
      Float,
      nullable=True,
    )
#jitter
    jitter: Mapped[float | None] = mapped_column(
      Float,
      nullable=True,
    )
#status
    status: Mapped[str | None] = mapped_column(
      String(30),
      nullable=True,
    )
#raw output of the measurement
    raw_output: Mapped[str | None] = mapped_column(
      Text,
      nullable=True,
    )




