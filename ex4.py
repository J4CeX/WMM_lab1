import numpy as np
import matplotlib.pyplot as plt


def excercise_four():
    # --- DANE WEJŚCIOWE ---
    fs = 48000  # Częstotliwość próbkowania [Hz]
    A1, f1 = 0.1, 3000
    A2, f2 = 0.4, 4000
    A3, f3 = 0.8, 10000

    N1 = 2048
    N2 = int(1.5 * N1)  # 3072


    def solve_for_N(N, title):
        # 1. Generowanie czasu i sygnału
        t = np.arange(N) / fs
        s = A1*np.sin(2*np.pi*f1*t) + A2*np.sin(2*np.pi*f2*t) + A3*np.sin(2*np.pi*f3*t)

        # 2. Obliczenie FFT (widmo)
        # RFFT używamy dla sygnałów rzeczywistych - dostajemy tylko dodatnie częstotliwości
        S_fft = np.fft.rfft(s)
        freqs = np.fft.rfftfreq(N, 1/fs)

        # 3. Widmowa gęstość mocy (PSD)
        # Skalowanie: |S|^2 / N
        psd = (np.abs(S_fft)**2) / N

        # 4. Obliczenie mocy średniej (zgodnie z tw. Parsevala lub w dziedzinie czasu)
        # Moc średnia to średnia kwadratów wartości sygnału
        power_time = np.mean(s**2)

        # Wykres
        plt.figure(figsize=(10, 4))
        plt.semilogy(freqs / 1000, psd) # Skala logarytmiczna lepiej pokazuje wyciek
        plt.title(f"PSD dla N = {N} ({title})")
        plt.xlabel("Częstotliwość [kHz]")
        plt.ylabel("Moc")
        plt.grid(True)
        plt.xlim(0, 15)  # Skupiamy się na zakresie naszych częstotliwości
        plt.savefig(f'4_psd_{title}.png', dpi=300)
        plt.show()

        return power_time, N


    print(f"{'N':<10} | {'Moc średnia':<15}")
    print("-" * 30)

    for N_val, label in [(N1, "N1"), (N2, "N2")]:
        p_avg, n = solve_for_N(N_val, label)
        print(f"{n:<10} | {p_avg:<15.6f}")

    # --- ANALIZA TEORETYCZNA DO PODPUNKTU B ---
    df1 = fs / N1
    df2 = fs / N2
    print(f"\nRozdzielczość widmowa dla N1: {df1:.2f} Hz")
    print(f"Rozdzielczość widmowa dla N2: {df2:.2f} Hz")


if __name__ == "__main__":
    excercise_four()