import asyncio
import os
import telnetlib3


HOST = "192.168.1.101"
PORT = 23
USERNAME = "adi.admin"


async def main():
    password = os.environ["MIKROTIK_PASSWORD"]

    reader, writer = await telnetlib3.open_connection(
        host=HOST,
        port=PORT,
    )

    # Tunggu prompt login
    await reader.readuntil(b"Login:")

    writer.write(USERNAME + "\n")

    # Tunggu prompt password
    await reader.readuntil(b"Password:")

    writer.write(password + "\n")

    # Tunggu sampai masuk ke RouterOS
    await reader.readuntil(b">")

    # Jalankan ping
    writer.write("/ping 8.8.8.8 count=5\n")

    # Baca output sampai prompt RouterOS muncul kembali
    output = await reader.readuntil(">")

    print("=== RAW OUTPUT ===")
    print(output)

    writer.close()


if __name__ == "__main__":
    asyncio.run(main())