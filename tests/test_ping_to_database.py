from datetime import datetime

from app.database import SessionLocal
from app.engine.mikrotik_telnet import MikroTikTelnet
from app.engine.ping import PingEngine
from app.repositories.measurement import MeasurementRepository


ROUTER_HOST = "192.168.1.101"
ROUTER_PORT = 23

ROUTER_USERNAME = "adi.admin"
ROUTER_PASSWORD = "adiabadinanjaya"

DESTINATION = "8.8.8.8"

PROBE_ID = 1
DESTINATION_ID = 1


def main():
    router = MikroTikTelnet(
        host=ROUTER_HOST,
        port=ROUTER_PORT,
        username=ROUTER_USERNAME,
        password=ROUTER_PASSWORD,
    )

    db = SessionLocal()

    try:
        print("=== CONNECTING TO MIKROTIK ===")

        router.connect()

        print("Connected.")

        # Measurement Engine
        ping_engine = PingEngine(router)

        print()
        print("=== RUNNING PING ===")

        result = ping_engine.measure(
            destination=DESTINATION,
            count=5,
        )

        print()
        print("=== PING RESULT ===")
        print(result)

        # Persistence
        repository = MeasurementRepository(db)

        measurement = repository.create(
            probe_id=PROBE_ID,
            destination_id=DESTINATION_ID,
            measurement_type="ping",
            timestamp=datetime.now(),
            packet_sent=result["packet_sent"],
            packet_received=result["packet_received"],
            packet_loss=result["packet_loss"],
            latency_min=result["latency_min"],
            latency_avg=result["latency_avg"],
            latency_max=result["latency_max"],
            status="success",
            raw_output=result["raw_output"],
        )

        print()
        print("=== DATABASE RESULT ===")
        print(f"Measurement ID : {measurement.id}")
        print(f"Probe ID       : {measurement.probe_id}")
        print(f"Destination ID : {measurement.destination_id}")
        print(f"Packet Loss    : {measurement.packet_loss}%")
        print(f"Latency Avg    : {measurement.latency_avg} ms")
        print(f"Status         : {measurement.status}")

        print()
        print("================================")
        print("DAY 2 INTEGRATION TEST : PASS")
        print("================================")

    except Exception as e:
        print()
        print("================================")
        print("DAY 2 INTEGRATION TEST : FAILED")
        print("================================")
        print(f"Error: {e}")

        db.rollback()
        raise

    finally:
        router.close()
        db.close()


if __name__ == "__main__":
    main()
