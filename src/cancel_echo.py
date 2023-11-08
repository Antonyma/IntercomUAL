import buffer
import numpy as np

class CancelEcho(buffer.Buffering):
    def __init__(self, delay=0, attenuation=0):
        super().__init__()
        self.delay = delay
        self.attenuation = attenuation

    def cancel_echo(self, signal):
        delayed_signal = np.roll(signal, self.delay)
        cancelled_signal = signal - self.attenuation * delayed_signal
        return cancelled_signal

    def estimate_delay(self, signal):
        correlation = np.correlate(signal, signal, mode='full')
        estimated_delay = np.argmax(correlation)
        return estimated_delay

    def estimate_attenuation(self, signal, delayed_signal):
        estimated_attenuation = np.mean(signal) / np.mean(delayed_signal)
        return estimated_attenuation

    def _record_io_and_play(self, indata, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.CHUNK_NUMBERS
        indata = self.cancel_echo(indata)
        packed_chunk = self.pack(self.chunk_number, indata)
        self.send(packed_chunk)
        chunk = self.unbuffer_next_chunk()
        self.play_chunk(outdata, chunk)

    def _read_io_and_play(self, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.CHUNK_NUMBERS
        read_chunk = self.read_chunk_from_file()
        read_chunk = self.cancel_echo(read_chunk)
        packed_chunk = self.pack(self.chunk_number, read_chunk)
        self.send(packed_chunk)
        chunk = self.unbuffer_next_chunk()
        self.play_chunk(outdata, chunk)
        return read_chunk
