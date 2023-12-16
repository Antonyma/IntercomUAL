import argcomplete
import numpy as np
import math
import minimal
import logging

from scipy.fftpack import fft, ifft
from temporal_overlapped_DWT_coding import Temporal_Overlapped_DWT
from temporal_overlapped_DWT_coding import Temporal_Overlapped_DWT__verbose

class Advanced_ToH(Temporal_Overlapped_DWT):
    
    def calculate_quantization_steps(self, max_q):
        def calc(f):
            return 3.64 * (f / 1000) ** (-0.8) - 6.5 * math.exp((-0.6) * (f / 1000 - 3.3) ** 2) + 10 ** (-3) * (f / 1000) ** 4

        f = 22050
        average_SPLs = []

        for i in range(self.dwt_levels):
            mean = 0
            for j in np.arange(f / 2, f, 1):
                mean += calc(j)
            f = f / 2
            average_SPLs.insert(0, mean / f)
        mean = 0
        for j in np.arange(1, f, 1):
            mean += calc(j)
        average_SPLs.insert(0, mean / f)

        min_SPL, max_SPL = np.min(average_SPLs), np.max(average_SPLs)
        quantization_steps = [round((spl - min_SPL) / (max_SPL - min_SPL) * (max_q - 1) + 1) for spl in average_SPLs]

        return quantization_steps

    def simulate_quantization_noise(self, chunk_wavelet):
        qss_values = []

        for i in range(self.dwt_levels + 1):
            subband_wavelet = chunk_wavelet[self.slices[i]['d'][0]]

            # Apply FFT to each sub-band
            subband_fft = fft(subband_wavelet)

            # Filter each sub-band with ToH using FFT
            toh_curve = self.calculate_toh_curve(len(subband_fft))
            subband_fft_filtered = subband_fft * toh_curve

            # Apply inverse FFT to obtain the filtered sub-band
            subband_wavelet_filtered = ifft(subband_fft_filtered).real

            # Implement logic to determine if the noise is perceptible
            perceptible = self.is_noise_perceptible(subband_wavelet_filtered)

            if perceptible:
                break
            qss_values.append(1.0)  # Placeholder, replace with the actual QSS value
        return qss_values

    def is_noise_perceptible(self, subband_wavelet_filtered, threshold_snr=10.0):
        # Calcula la energía de la señal y del ruido
        signal_energy = np.sum(subband_wavelet_filtered**2)
        noise_energy = np.sum((subband_wavelet_filtered - subband_wavelet_filtered.mean())**2)

        # Calcula la relación señal-ruido (SNR)
        snr = 10 * np.log10(signal_energy / noise_energy)

        # Determina si el ruido es perceptible comparando con un umbral
        return snr < threshold_snr

    def calculate_toh_curve(self, length):
        # Tabla de curva ToH precalculada
        toh_curve = np.array([
            [-31.6, -27.2, -23.0, -19.1, -15.9, -13.0, -10.3, -8.1, -6.2, -3.6],
            [-31.6, -27.2, -23.0, -19.1, -15.9, -13.0, -10.3, -8.1, -6.2, -3.6],
        ])

        # Normaliza la curva ToH
        toh_curve -= np.min(toh_curve)
        toh_curve /= np.max(toh_curve)

        # Ajusta la longitud de la curva ToH para que coincida con la longitud de la señal de audio
        toh_curve = np.interp(np.linspace(0, 1, length), np.linspace(0, 1, len(toh_curve)), toh_curve)
        return toh_curve

class Advanced_ToH__verbose(Advanced_ToH, Temporal_Overlapped_DWT__verbose):
    pass

if __name__ == "__main__":
    minimal.parser.description = __doc__
    try:
        argcomplete.autocomplete(minimal.parser)
    except Exception:
        logging.warning("argcomplete not working :-/")
    minimal.args = minimal.parser.parse_known_args()[0]
    if minimal.args.show_stats or minimal.args.show_samples:
        intercom = Advanced_ToH__verbose()
    else:
        intercom = Advanced_ToH()
    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
        intercom.print_final_averages()
