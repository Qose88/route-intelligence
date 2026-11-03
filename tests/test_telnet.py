import os

from app.engine.mikrotik_telnet import MikroTikTelnet


router = MikroTikTelnet(
    host="192.168.1.101",
    port=23,
    username="adi.admin",
    password=os.environ["MIKROTIK_PASSWORD"],
)


try:
    router.connect()

    output = router.send_command(
        "/ping 8.8.8.8 count=5"
    )

    print("\n===== RAW OUTPUT =====")
    print(output)

finally:
    router.close()