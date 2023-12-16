import logging
import numpy as np
import buffer 
import minimal
import argcomplete

class CancelEcho(buffer.Buffering):
        
    def unbuffer_next_chunk(self):
        chunk = self.buffer[self.played_chunk_number % self.cells_in_buffer]
        return chunk

    def record_io_and_play(self, indata, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.CHUNK_NUMBERS
        min_length = min(len(indata), len(outdata))
        cancelled_signal = [indata[i] - self.attenuation * outdata[i + self.delay] 
                            for i in range(min_length - self.delay)]
        cancelled_signal = np.concatenate((indata[:self.delay], cancelled_signal))
        cancelled_signal = np.array(cancelled_signal)
        cancelled_signal = cancelled_signal.astype(np.uint16)
        packed_chunk = self.pack(self.CHUNK_NUMBERS, cancelled_signal)

        self.send(packed_chunk)
        chunk = self.unbuffer_next_chunk()
        self.play_chunk(outdata, chunk)

    def play_chunk(self, DAC, chunk):
        super().play_chunk(DAC, chunk)

if __name__ == "__main__":
    minimal.parser.description = __doc__
    minimal.args = minimal.parser.parse_known_args()[0]
    if minimal.args.show_stats or minimal.args.show_samples:
        intercom = buffer.Buffering__verbose()
    else:
        intercom = CancelEcho(50, 0.2)
    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
        intercom.print_final_averages()

