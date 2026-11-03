from datetime import datetime

from app.database import SessionLocal
from app.repositories.measurement import MeasurementRepository


def main():
    db = SessionLocal()

    try:
        repo = MeasurementRepository(db)

        measurement = repo.create(
            probe_id=1,
            destination_id=1,
            measurement_type="ping",
            timestamp=datetime.now(),
            packet_sent=5,
            packet_received=5,
            packet_loss=0.0,
            latency_min=3.457,
            latency_avg=4.002,
            latency_max=4.949,
            status="success",
            raw_output="TEST RAW OUTPUT",
        )

        print("=== MEASUREMENT CREATED ===")
        print(f"ID              : {measurement.id}")
        print(f"Probe ID        : {measurement.probe_id}")
        print(f"Destination ID  : {measurement.destination_id}")
        print(f"Type            : {measurement.measurement_type}")
        print(f"Packet Loss     : {measurement.packet_loss}%")
        print(f"Latency Avg     : {measurement.latency_avg} ms")
        print(f"Status          : {measurement.status}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
