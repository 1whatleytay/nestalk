from typing import Optional

# Protobuf needs a way to tell apart one message from the next in a socket stream.
# This is a really simply (not too performant) delimiter to tell them apart.


class Delimiter:
    size = None
    buffer = bytearray()

    def push(self, data: bytes):
        self.buffer.extend(data)

    def pop_bytes(self, count: int) -> bytearray:
        result = self.buffer[:count]

        self.buffer = self.buffer[count:]

        return result

    def pop(self) -> Optional[bytearray]:
        if self.size is None:
            if len(self.buffer) >= 8:
                result = self.pop_bytes(8)

                self.size = int.from_bytes(result, 'big')
            else:
                return None

        if len(self.buffer) < self.size:
            return None

        result = self.pop_bytes(self.size)
        self.size = None

        return result
