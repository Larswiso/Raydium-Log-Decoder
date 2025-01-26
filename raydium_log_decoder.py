import base64
from struct import unpack
from typing import Union
import struct

class LogParser:
    def __init__(self):
        # Define structures for different log types
        self.structures = {
            0: self._init_structure,
            1: self._deposit_structure,
            2: self._withdraw_structure,
            3: self._swap_base_in_structure,
            4: self._swap_base_out_structure,
        }

    def _decode_data(self, data: bytes, structure: list):
        """Decode data based on the provided structure."""
        decoded_data = {}
        offset = 0
        for key, fmt in structure:
            size = struct.calcsize(fmt)
            value = unpack(fmt, data[offset:offset + size])[0]
            decoded_data[key] = value
            offset += size
        return decoded_data

    def _init_structure(self):
        return [
            ("logType", "B"),
            ("time", "Q"),
            ("pcDecimals", "B"),
            ("coinDecimals", "B"),
            ("pcLotSize", "Q"),
            ("coinLotSize", "Q"),
            ("pcAmount", "Q"),
            ("coinAmount", "Q"),
            ("market", "32s"),
        ]

    def _deposit_structure(self):
        return [
            ("logType", "B"),
            ("maxCoin", "Q"),
            ("maxPc", "Q"),
            ("base", "Q"),
            ("poolCoin", "Q"),
            ("poolPc", "Q"),
            ("pcAmount", "Q"),
            ("poolLp", "Q"),
            ("calcPnlX", "d"),
            ("calcPnlY", "d"),
            ("deductCoin", "Q"),
            ("deductPc", "Q"),
            ("mintLp", "Q"),
        ]

    def _withdraw_structure(self):
        return [
            ("logType", "B"),
            ("withdrawLp", "Q"),
            ("userLp", "Q"),
            ("poolCoin", "Q"),
            ("poolPc", "Q"),
            ("poolLp", "Q"),
            ("calcPnlX", "d"),
            ("calcPnlY", "d"),
            ("outCoin", "Q"),
            ("outPc", "Q"),
        ]

    def _swap_base_in_structure(self):
        return [
            ("logType", "B"),
            ("amountIn", "Q"),
            ("minimumOut", "Q"),
            ("direction", "Q"),
            ("userSource", "Q"),
            ("poolCoin", "Q"),
            ("poolPc", "Q"),
            ("outAmount", "Q"),
        ]

    def _swap_base_out_structure(self):
        return [
            ("logType", "B"),
            ("maxIn", "Q"),
            ("amountOut", "Q"),
            ("direction", "Q"),
            ("userSource", "Q"),
            ("poolCoin", "Q"),
            ("poolPc", "Q"),
            ("directIn", "Q"),
        ]

    def parse(self, log: str) -> Union[dict, None]:
        """Parse a base64-encoded log string."""
        if not log:
            return None
        
        # Remove the "ray_log: " prefix
        
        
        # Decode the Base64-encoded data
        data = base64.b64decode(log)
        
        # Extract the logType
        log_type = unpack("B", data[:1])[0]
        
        # Get the structure for the logType
        structure_fn = self.structures.get(log_type)
        if not structure_fn:
            return None
        
        structure = structure_fn()
        decoded_data = self._decode_data(data, structure)
        
        # Map logType to a name
        names = {
            0: "init",
            1: "deposit",
            2: "withdraw",
            3: "swapBaseIn",
            4: "swapBaseOut",
        }
        
        return {
            "name": names.get(log_type, "unknown"),
            "data": decoded_data
        }

# Example usage
if __name__ == "__main__":
    parser = LogParser()
    example_log = "A4F5VwkHAwAAmTbmAgAAAAABAAAAAAAAAIF5VwkHAwAA/vqNhAQAAACaA/CDAREDAJ2lbgQAAAAA"  # Replace with a valid Base64-encoded log
    parsed_log = parser.parse(example_log)
    print(parsed_log)
