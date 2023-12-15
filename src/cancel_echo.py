
import numpy as np
from buffer import Buffering as Buffer 

class CancelEcho(Buffer):
    def __init__(self, delay, attenuation):
        self.attenuations = attenuation
        self.delay = delay
        super().__init__()

    def unbuffer_next_chunk(self):
        chunk = self.buffer[self.played_chunk_number % self.cells_in_buffer]
        return chunk

    def record_io_and_play(self, indata, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.chunk_number
        packed_chunk = self.pack(self.chunk_number, indata)
        # Echo chunk
        min_length = min(len(indata), len(outdata))
        cancelled_signal = [indata[i] - self.attenuation * outdata[i + self.delay] 
                            for i in range(min_length - indata)]
        cancelled_signal = np.concatenate((indata[:self.delay], cancelled_signal))
        cancelled_signal = np.array(cancelled_signal)
        cancelled_signal = cancelled_signal.astype(np.uint16)
        packed_chunk = self.pack(self.chunk_number, cancelled_signal)

        self.send(packed_chunk)
        chunk = self.unbuffer_next_chunk()
        self.play_chunk(outdata, chunk)

    def play_chunk(self, DAC, chunk):
        super().play_chunk(DAC, chunk)
