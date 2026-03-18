import numpy as np
import matplotlib.pyplot as plt
import time


def excercise_two():
    # Dobór wartości N - od 2^10 do 2^21
    l_values = np.arange(10, 22)
    n_sizes = 2**l_values
    times = []

    # Pusty przebieg FFT, żeby uniknąć wpływu pierwszego wywołania na pomiary
    _ = np.fft.fft(np.random.rand(1024))

    print("Rozpoczynam pomiary czasowe...")

    for N in n_sizes:
        # Losowy sygnał o długości N
        signal = np.random.rand(N)

        # Pomiar czasu (uśredniony z kilku prób)
        start_time = time.time()
        for _ in range(5):
            _ = np.fft.fft(signal)
        end_time = time.time()

        avg_time = (end_time - start_time) / 5
        times.append(avg_time)
        print(f"N = {N:10} | Czas: {avg_time:.6f} s")

    # 2. Wykres
    plt.figure(figsize=(10, 6))
    plt.plot(n_sizes, times, 'o-', label='Czas wykonania FFT')

    theo_trend = n_sizes * np.log2(n_sizes)
    theo_trend = theo_trend * (times[-1] / theo_trend[-1])
    plt.plot(n_sizes, theo_trend, '--', alpha=0.5,
             label='Trend teoretyczny O(N log N)')

    plt.xscale('log', base=2)
    plt.xlabel('Liczba próbek N (skala log2)')
    plt.ylabel('Czas obliczeń [s]')
    plt.title('Złożoność obliczeniowa FFT w funkcji liczby próbek')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig('1b fft_complexity.png', dpi=300)
    plt.show()
