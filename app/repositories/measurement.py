from datetime import datetime

from sqlalchemy.orm import Session

from app.models.measurement import Measurement


class MeasurementRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        probe_id: int,
        destination_id: int,
        measurement_type: str,
        timestamp: datetime,
        packet_sent: int | None = None,
        packet_received: int | None = None,
        packet_loss: float | None = None,
        latency_min: float | None = None,
        latency_avg: float | None = None,
        latency_max: float | None = None,
        jitter: float | None = None,
        status: str | None = None,
        raw_output: str | None = None,
    ) -> Measurement:

        measurement = Measurement(
            probe_id=probe_id,
            destination_id=destination_id,
            measurement_type=measurement_type,
            timestamp=timestamp,
            packet_sent=packet_sent,
            packet_received=packet_received,
            packet_loss=packet_loss,
            latency_min=latency_min,
            latency_avg=latency_avg,
            latency_max=latency_max,
            jitter=jitter,
            status=status,
            raw_output=raw_output,
        )

        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)

        return measurement
