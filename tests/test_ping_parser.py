from app.engine.ping import parse_routeros_ping


raw_output = """
  SEQ HOST                                     SIZE TTL TIME       STATUS
    0 8.8.8.8                                    56 115 4ms360us
    1 8.8.8.8                                    56 115 5ms14us
    2 8.8.8.8                                    56 115 7ms16us
    3 8.8.8.8                                    56 115 4ms29us
    4 8.8.8.8                                    56 115 5ms653us

    sent=5 received=5 packet-loss=0% min-rtt=4ms29us avg-rtt=5ms214us
   max-rtt=7ms16us
"""


result = parse_routeros_ping(raw_output)

print("=== PARSED RESULT ===")
print(result)
assert result["packet_sent"] == 5
assert result["packet_received"] == 5
assert result["packet_loss"] == 0.0

assert result["latency_min"] == 4.029
assert result["latency_avg"] == 5.214
assert result["latency_max"] == 7.016

print("PASS: ping parser")