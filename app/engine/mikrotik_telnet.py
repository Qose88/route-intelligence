import socket
import time


class MikroTikTelnet:
    IAC = 255
    WILL = 251
    WONT = 252
    DO = 253
    DONT = 254

    DSR_QUERY = b"\x1b[6n"
    DSR_REPLY = b"\x1b[24;80R"

    def __init__(
        self,
        host: str,
        port: int = 23,
        username: str = "",
        password: str = "",
        timeout: float = 10.0,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.sock: socket.socket | None = None

    def _send(self, data: bytes) -> None:
        if self.sock is None:
            raise RuntimeError(
                "Telnet connection is not established"
            )

        self.sock.sendall(data)

    def _handle_telnet_negotiation(
        self,
        data: bytes,
    ) -> bytes:
        """
        Handle basic Telnet negotiation.

        MikroTik can send:

            IAC DO option
            IAC WILL option
            IAC DONT option
            IAC WONT option

        Route Intelligence does not need
        advanced Telnet terminal features,
        so unsupported options are rejected.
        """

        clean = bytearray()
        i = 0

        while i < len(data):

            # Normal data
            if data[i] != self.IAC:
                clean.append(data[i])
                i += 1
                continue

            # Incomplete Telnet command
            if i + 1 >= len(data):
                break

            command = data[i + 1]

            # Escaped IAC -> literal 255
            if command == self.IAC:
                clean.append(self.IAC)
                i += 2
                continue

            # Telnet negotiation
            if command in (
                self.WILL,
                self.WONT,
                self.DO,
                self.DONT,
            ):

                # Option byte not available yet
                if i + 2 >= len(data):
                    break

                option = data[i + 2]

                # Server asks client to enable option
                if command == self.DO:

                    self._send(
                        bytes(
                            [
                                self.IAC,
                                self.WONT,
                                option,
                            ]
                        )
                    )

                # Server says it will enable option
                elif command == self.WILL:

                    self._send(
                        bytes(
                            [
                                self.IAC,
                                self.DONT,
                                option,
                            ]
                        )
                    )

                # Server asks us to disable something
                elif command == self.DONT:
                    pass

                # Server says it disabled something
                elif command == self.WONT:
                    pass

                i += 3
                continue

            # Other Telnet command
            i += 2

        return bytes(clean)

    def _recv(
        self,
        timeout: float = 0.5,
    ) -> bytes:

        if self.sock is None:
            raise RuntimeError(
                "Telnet connection is not established"
            )

        self.sock.settimeout(timeout)

        try:
            data = self.sock.recv(8192)

        except socket.timeout:
            return b""

        except OSError:
            return b""

        if not data:
            return b""

        # Handle Telnet negotiation
        data = self._handle_telnet_negotiation(
            data
        )

        # Handle RouterOS terminal size query
        if self.DSR_QUERY in data:

            self._send(
                self.DSR_REPLY
            )

            data = data.replace(
                self.DSR_QUERY,
                b"",
            )

        return data

    def _wait_for(
        self,
        patterns: list[str],
        timeout: float = 10.0,
    ) -> tuple[str, str | None]:

        buffer = b""
        start = time.time()

        patterns_lower = [
            pattern.lower()
            for pattern in patterns
        ]

        while time.time() - start < timeout:

            chunk = self._recv()

            if not chunk:
                time.sleep(0.05)
                continue

            buffer += chunk

            text = buffer.decode(
                "utf-8",
                errors="replace",
            )

            text_lower = text.lower()

            for pattern_lower, pattern in zip(
                patterns_lower,
                patterns,
            ):

                if pattern_lower in text_lower:
                    return text, pattern

        text = buffer.decode(
            "utf-8",
            errors="replace",
        )

        return text, None

    def connect(self) -> bool:

        print(
            f"Connecting to "
            f"{self.host}:{self.port}..."
        )

        try:

            self.sock = socket.create_connection(
                (
                    self.host,
                    self.port,
                ),
                timeout=self.timeout,
            )

        except OSError as exc:

            raise ConnectionError(
                f"Unable to connect to "
                f"{self.host}:{self.port}: {exc}"
            ) from exc

        # Wait for RouterOS login prompt
        stage1, matched = self._wait_for(
            [
                "login:",
                "name:",
            ],
            timeout=self.timeout,
        )

        print(
            "Telnet initial response:",
            repr(stage1),
        )

        if matched is None:

            raise TimeoutError(
                "MikroTik did not send login prompt. "
                f"Received: {stage1!r}"
            )

        print(
            "Login prompt detected."
        )

        # RouterOS terminal modifier
        self._send(
            (
                self.username
                + "+ct80w"
                + "\r\n"
            ).encode()
        )

        # Wait for password prompt
        stage2, matched = self._wait_for(
            [
                "password:",
            ],
            timeout=self.timeout,
        )

        if matched is None:

            raise TimeoutError(
                "Password prompt not detected. "
                f"Received: {stage2!r}"
            )

        # Send password
        self._send(
            (
                self.password
                + "\r\n"
            ).encode()
        )

        # Wait for login result
        stage3, matched = self._wait_for(
            [
                "] >",
                "new password>",
                "invalid",
                "incorrect",
                "login failed",
                "bad password",
            ],
            timeout=self.timeout,
        )

        if matched is None:

            raise TimeoutError(
                "RouterOS login result not detected. "
                f"Received: {stage3!r}"
            )

        # Authentication failed
        if matched in (
            "invalid",
            "incorrect",
            "login failed",
            "bad password",
        ):

            raise RuntimeError(
                "MikroTik rejected username/password."
            )

        # RouterOS requests password change
        if matched == "new password>":

            print(
                "RouterOS requests password change. "
                "Cancelling with Ctrl+C..."
            )

            self._send(
                b"\x03"
            )

            stage3b, matched = self._wait_for(
                [
                    "] >",
                ],
                timeout=self.timeout,
            )

            if matched != "] >":

                raise RuntimeError(
                    "Could not reach RouterOS prompt "
                    "after cancelling password change."
                )

        # Successful login
        if matched == "] >":

            print(
                "Login successful."
            )

            # Remove leftover terminal output
            self._drain()

            return True

        raise RuntimeError(
            "Unexpected RouterOS login state."
        )

    def _drain(
        self,
        quiet_window: float = 0.5,
        max_total: float = 2.0,
    ) -> str:

        buffer = b""

        start = time.time()
        last_data = time.time()

        while time.time() - start < max_total:

            chunk = self._recv()

            if chunk:

                buffer += chunk
                last_data = time.time()

            if (
                time.time() - last_data
                >= quiet_window
            ):
                break

            time.sleep(0.05)

        return buffer.decode(
            "utf-8",
            errors="replace",
        )

    def send_command(
        self,
        command: str,
        timeout: float = 30.0,
    ) -> str:

        if self.sock is None:

            raise RuntimeError(
                "Telnet connection is not established"
            )

        # Send command
        self._send(
            (
                command
                + "\r\n"
            ).encode()
        )

        buffer = b""
        start = time.time()

        # RouterOS echoes the command like:
        #
        # [adi.admin@Mikrotik-DUMMY] > /ping 8.8.8.8 count=5
        #
        # The "] >" in that line is NOT the
        # completion prompt.
        echo_marker = (
            "] > "
            + command
        )

        echo_seen = False

        while time.time() - start < timeout:

            chunk = self._recv(
                timeout=0.5
            )

            if not chunk:
                continue

            buffer += chunk

            text = buffer.decode(
                "utf-8",
                errors="replace",
            )

            text_lower = text.lower()

            # -------------------------------------------------
            # STEP 1
            # Wait until RouterOS echoes our command.
            # -------------------------------------------------

            if not echo_seen:

                if (
                    echo_marker.lower()
                    in text_lower
                ):

                    echo_seen = True

                continue

            # -------------------------------------------------
            # STEP 2
            # Command echo has been received.
            #
            # Now search for the NEXT "] >" prompt.
            # -------------------------------------------------

            echo_position = (
                text_lower.find(
                    echo_marker.lower()
                )
            )

            if echo_position == -1:
                continue

            output_start = (
                echo_position
                + len(echo_marker)
            )

            output_after_echo = text[
                output_start:
            ]

            if "] >" in output_after_echo:

                return output_after_echo

        # Timeout
        text = buffer.decode(
            "utf-8",
            errors="replace",
        )

        raise TimeoutError(
            f"Command timeout: "
            f"{command!r}. "
            f"Received: {text!r}"
        )

    def close(self) -> None:

        if self.sock is not None:

            try:

                self.sock.close()

            finally:

                self.sock = None

        print(
            "Connection closed."
        )