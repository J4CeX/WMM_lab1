import sys
import numpy as np
import matplotlib.pyplot as plt
import time


def excercise_one_a():
    N = 8        # Liczba próbek
    T = 2        # Okres sygnału s(t) = cos(pi*t) f = 0.5Hz, T = 1/f = 2
    fs = N / T   # Częstotliwość próbkowania (4 Hz)
    dt = 1 / fs  # Krok czasowy (0.25 s)

    t = np.arange(N) * dt
    s = np.cos(np.pi * t)

    Xk = np.fft.fft(s)
    f_axis = np.fft.fftfreq(N, dt)  # Oś częstotliwości

    # Widmo amplitudowe i fazowe
    module = np.abs(Xk)
    phase = np.angle(Xk)

    energy_time = np.sum(s**2)
    energy_fourier = np.sum(module**2) / N

    print("--- Weryfikacja Twierdzenia Parsevala ---")
    print(f"Suma kwadratów w dziedzinie czasu: {energy_time:.4f}")
    print(f"Suma kwadratów w dziedzinie częstotliwości (znormalizowana): "
          f"{energy_fourier:.4f}")
    print(f"Różnica: {abs(energy_time - energy_fourier)}")

    plt.figure(figsize=(12, 10))

    # Wykres sygnału spróbkowanego
    plt.subplot(3, 1, 1)
    plt.stem(t, s, basefmt=" ", linefmt='b', markerfmt='bo')
    plt.plot(np.linspace(0, T, 100), np.cos(np.pi * np.linspace(0, T, 100)),
             'r--', alpha=0.3)
    plt.title(f'Sygnał spróbkowany $s(t) = \cos(\pi t)$ dla $N={N}$')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)

    # Widmo amplitudowe
    plt.subplot(3, 1, 2)
    plt.stem(f_axis, module, basefmt=" ", linefmt='g', markerfmt='go')
    plt.title('Widmo amplitudowe $|X[k]|$')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Moduł')
    plt.grid(True)

    # Widmo fazowe
    plt.subplot(3, 1, 3)
    phase_clean = np.where(module > 1e-10, phase, 0)
    plt.stem(f_axis, phase_clean, basefmt=" ", linefmt='m', markerfmt='mo')
    plt.title('Widmo fazowe $\\arg(X[k])$')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Faza [rad]')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('1a_fft_analysis.png', dpi=300)
    plt.show()


def excercise_one_b():
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
    plt.savefig('1b_fft_complexity.png', dpi=300)
    plt.show()


def excercise_two(N=48, A=2):
    n = np.arange(N)
    n0_values = [0, int(N/4), int(N/2), int(3*N/4)]

    fig, axes = plt.subplots(len(n0_values), 3, figsize=(15, 12))
    fig.suptitle(f'Wpływ przesunięcia $n_0$ na widmo (N={N}, A={A})',
                 fontsize=16)

    for i, n0 in enumerate(n0_values):
        # Generowanie sygnału i przesunięcie kołowe
        s_base = A * np.cos(2 * np.pi * n / N)
        s_shifted = np.roll(s_base, n0)

        # Obliczenia FFT
        Xk = np.fft.fft(s_shifted)
        # Normalizacja osi częstotliwości (od -0.5 do 0.5)
        freqs = np.fft.fftfreq(N)

        # Widmo amplitudowe i fazowe
        amp = np.abs(Xk)
        phase = np.angle(Xk)

        # Tłumienie "szumu" fazowego dla prążków o zerowej amplitudzie
        phase[amp < 1e-10] = 0

        # Dziedzina czasu
        axes[i, 0].stem(n, s_shifted, linefmt='b', markerfmt='bo', basefmt=" ")
        axes[i, 0].set_title(f'Sygnał $s(n - {n0})$')
        axes[i, 1].set_ylabel('Amplituda')
        axes[i, 0].grid(True, alpha=0.3)

        # Widmo amplitudowe
        axes[i, 1].stem(freqs, amp, linefmt='g', markerfmt='go', basefmt=" ")
        axes[i, 1].set_title(f'Widmo amplitudowe (n0={n0})')
        axes[i, 1].grid(True, alpha=0.3)

        # Widmo fazowe
        axes[i, 2].stem(freqs, phase, linefmt='m', markerfmt='mo', basefmt=" ")
        axes[i, 2].set_title(f'Widmo fazowe (n0={n0})')
        axes[i, 2].set_ylim(-np.pi-0.5, np.pi+0.5)
        axes[i, 2].set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
        axes[i, 2].set_yticklabels(['-$\pi$', '-$\pi$/2', '0',
                                    '$\pi$/2', '$\pi$'])
        axes[i, 2].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('2_time_shift_analysis.png', dpi=300)
    plt.show()


def excercise_three():
    A = 3
    N = 10
    n0_multipliers = [0, 1, 4, 9]  # Mnożniki dla N0 = {0, 1N, 4N, 9N}

    fig, axes = plt.subplots(len(n0_multipliers), 3, figsize=(15, 12))
    fig.suptitle('Wpływ dopełniania zerami (Zero-Padding) na widmo',
                 fontsize=16)

    for i, mult in enumerate(n0_multipliers):
        N0 = mult * N

        # Generowanie jednego okresu sygnału podstawowego
        n_base = np.arange(N)
        s_base = A * (1 - (n_base % N) / N)

        # Dopełnianie zerami
        s_padded = np.concatenate([s_base, np.zeros(N0)])
        total_N = len(s_padded)

        # Obliczenia FFT
        Xk = np.fft.fft(s_padded)
        freqs = np.fft.fftfreq(total_N)

        amp = np.abs(Xk)
        phase = np.angle(Xk)
        phase[amp < 1e-10] = 0  # Czyszczenie szumu

        # Dziedzina czasu
        axes[i, 0].stem(range(total_N), s_padded, linefmt='b', markerfmt='bo',
                        basefmt=" ")
        axes[i, 0].set_title(f'Sygnał (N0={N0}, Suma N={total_N})')
        axes[i, 0].grid(True, alpha=0.3)

        # Widmo amplitudowe
        # Używamy plot zamiast stem dla dużych N, żeby widzieć "ciągłość"
        if total_N > 20:
            axes[i, 1].plot(np.fft.fftshift(freqs), np.fft.fftshift(amp), 'g-')
        else:
            axes[i, 1].stem(np.fft.fftshift(freqs), np.fft.fftshift(amp),
                            linefmt='g', markerfmt='go', basefmt=" ")
        axes[i, 1].set_title('Widmo amplitudowe')
        axes[i, 1].grid(True, alpha=0.3)

        # Widmo fazowe
        if total_N > 20:
            axes[i, 2].plot(np.fft.fftshift(freqs), np.fft.fftshift(phase),
                            'm-')
        else:
            axes[i, 2].stem(np.fft.fftshift(freqs), np.fft.fftshift(phase),
                            linefmt='m', markerfmt='mo', basefmt=" ")
        axes[i, 2].set_title('Widmo fazowe')
        axes[i, 2].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('3_zero_padding_analysis.png', dpi=300)
    plt.show()


def excercise_four():
    fs = 48000  # Częstotliwość próbkowania [Hz]
    A1, f1 = 0.1, 3000
    A2, f2 = 0.4, 4000
    A3, f3 = 0.8, 10000

    N1 = 2048
    N2 = int(1.5 * N1)  # 3072

    def solve_for_N(N, title):
        # Generowanie czasu i sygnału
        t = np.arange(N) / fs
        s = A1*np.sin(2*np.pi*f1*t) + A2*np.sin(2*np.pi*f2*t) + A3*np.sin(
            2*np.pi*f3*t)

        # Obliczenie FFT (widmo)
        # RFFT używamy dla sygnałów rzeczywistych - dostajemy tylko dodatnie
        # częstotliwości
        S_fft = np.fft.rfft(s)
        freqs = np.fft.rfftfreq(N, 1/fs)

        # Widmowa gęstość mocy (PSD)
        # Skalowanie: |S|^2 / N
        psd = (np.abs(S_fft)**2) / N

        # Obliczenie mocy średniej (zgodnie z tw. Parsevala lub
        # w dziedzinie czasu)
        # Moc średnia to średnia kwadratów wartości sygnału
        power_time = np.mean(s**2)

        plt.figure(figsize=(10, 4))
        # Skala logarytmiczna lepiej pokazuje wyciek
        plt.semilogy(freqs / 1000, psd)
        plt.title(f"PSD dla N = {N} ({title})")
        plt.xlabel("Częstotliwość [kHz]")
        plt.ylabel("Moc")
        plt.grid(True)
        plt.xlim(0, 15)  # Skupiamy się na zakresie częstotliwości
        plt.savefig(f'4_psd_{title}.png', dpi=300)
        plt.show()

        return power_time, N

    print(f"{'N':<10} | {'Moc średnia':<15}")
    print("-" * 30)

    for N_val, label in [(N1, "N1"), (N2, "N2")]:
        p_avg, n = solve_for_N(N_val, label)
        print(f"{n:<10} | {p_avg:<15.6f}")

    df1 = fs / N1
    df2 = fs / N2
    print(f"\nRozdzielczość widmowa dla N1: {df1:.2f} Hz")
    print(f"Rozdzielczość widmowa dla N2: {df2:.2f} Hz")


def main(excercise):
    if excercise == "1a":
        excercise_one_a()
    elif excercise == "1b":
        excercise_one_b()
    elif excercise == "2":
        excercise_two()
    elif excercise == "3":
        excercise_three()
    elif excercise == "4":
        excercise_four()
    elif excercise == "all":
        excercise_one_a()
        excercise_one_b()
        excercise_two()
        excercise_three()
        excercise_four()
    else:
        print("Excercises are: 1a, 1b, 2, 3, 4 or all")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 1:
        main(None)
