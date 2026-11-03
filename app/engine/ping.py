from app.engine.mikrotik_telnet import MikroTikTelnet
import re


def parse_routeros_ping(raw_output: str) -> dict:
    result = {
        "packet_sent": None,
        "packet_received": None,
        "packet_loss": None,
        "latency_min": None,
        "latency_avg": None,
        "latency_max": None,
    }

    packet_match = re.search(
        r"sent=(\d+)\s+"
        r"received=(\d+)\s+"
        r"packet-loss=([\d.]+)%",
        raw_output,
        re.IGNORECASE,
    )

    if packet_match:
        result["packet_sent"] = int(packet_match.group(1))
        result["packet_received"] = int(packet_match.group(2))
        result["packet_loss"] = float(packet_match.group(3))

    rtt_match = re.search(
        r"min-rtt=(\d+)ms(\d+)us\s+"
        r"avg-rtt=(\d+)ms(\d+)us\s+"
        r"max-rtt=(\d+)ms(\d+)us",
        raw_output,
        re.IGNORECASE,
    )

    if rtt_match:
        result["latency_min"] = (
            int(rtt_match.group(1))
            + int(rtt_match.group(2)) / 1000
        )

        result["latency_avg"] = (
            int(rtt_match.group(3))
            + int(rtt_match.group(4)) / 1000
        )

        result["latency_max"] = (
            int(rtt_match.group(5))
            + int(rtt_match.group(6)) / 1000
        )

    return result


class PingEngine:

    def __init__(self, router: MikroTikTelnet):
        self.router = router

    def measure(
        self,
        destination: str,
        count: int = 5,
    ) -> dict:

        command = (
            f"/ping {destination} count={count}"
        )

        raw_output = self.router.send_command(
            command
        )

        result = parse_routeros_ping(
            raw_output
        )

        result["destination"] = destination
        result["raw_output"] = raw_output

        return result