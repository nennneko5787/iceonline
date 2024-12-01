# 日本サーバーと会話してみるテスト
# 有識者の皆様解析してください m(_ _)m

import asyncio


class UDPClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.on_response = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection established.")

    def datagram_received(self, data, addr):
        # 応答を受信
        print(f"Received: {data.hex()} from {addr}")
        if self.on_response:
            self.on_response.set_result(data)

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def connection_lost(self, exc):
        print("Socket closed")
        self.transport = None

    async def send_message(self, message, addr, timeout=5):
        if not self.transport:
            raise RuntimeError("Transport is not available.")

        self.on_response = self.loop.create_future()
        print(f"Sending: {message.hex()} to {addr}")
        self.transport.sendto(message, addr)

        try:
            response = await asyncio.wait_for(self.on_response, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            print("No response received (timeout).")
            return None


async def main():
    loop = asyncio.get_running_loop()
    host = "31.223.184.154"
    port = 5055

    # UDPクライアントを作成
    connect = loop.create_datagram_endpoint(
        lambda: UDPClientProtocol(loop), remote_addr=(host, port)
    )
    transport, protocol = await connect

    try:
        # 送信するパケットのリスト
        packets = [
            bytes.fromhex(
                """
                ff ff 00 01 00 00
                00 97 21 a0 0b 35 02 ff 01 04 00 00 00 2c 00 00
                00 01 00 00 04 b0 00 00 80 00 00 00 00 02 00 00
                00 00 00 00 00 00 00 00 13 88 00 00 00 02 00 00
                00 02
                """
            ),
            bytes.fromhex(
                """
                51 60 00 01 00 00
                01 0d 21 a0 0b 35 01 ff 00 04 00 00 00 14 00 00
                00 00 00 00 00 01 aa 9d ba 70
                """
            ),
            bytes.fromhex(
                """
                51 60 00 01 00 00
                01 60 21 a0 0b 35 06 00 01 04 00 00 00 35 00 00
                00 01 f3 00 01 08 1e 41 07 01 00 64 34 36 35 34
                36 62 62 2d 62 37 65 65 2d 34 31 37 62 2d 61 65
                63 38 2d 33 39 30 35 33 31 33 35
                """
            ),
        ]

        # 順次送信
        for i, packet in enumerate(packets, start=1):
            print(f"Sending packet {i}...")
            response = await protocol.send_message(packet, (host, port))
            if response:
                print(f"Response to packet {i}: {response.hex()}")
            else:
                print(f"No response for packet {i}.")

    finally:
        transport.close()


asyncio.run(main())
