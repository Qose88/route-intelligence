from app.database import SessionLocal
from app.models.customer import Customer
from app.models.probe import Probe
from app.models.destination import Destination


def main():
    db = SessionLocal()

    try:
        customer = Customer(
            name="Customer Test",
            description="Customer untuk integration test",
        )
        db.add(customer)
        db.flush()

        probe = Probe(
            customer_id=customer.id,
            name="Probe MikroTik Test",
            type="mikrotik",
            hostname="MikroTik-DUMMY",
            location="Lab",
            status="active",
        )
        db.add(probe)

        destination = Destination(
            name="Google DNS",
            category="network",
            description="8.8.8.8",
            status="active",
        )
        db.add(destination)

        db.commit()

        print("=== SEED DATA ===")
        print(f"Customer ID   : {customer.id}")
        print(f"Probe ID      : {probe.id}")
        print(f"Destination ID: {destination.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()