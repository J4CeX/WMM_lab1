import numpy as np
import matplotlib.pyplot as plt

def exercise_three():
    # Parametry bazowe
    A = 3
    N = 10
    n0_multipliers = [0, 1, 4, 9]  # Mnożniki dla N0 = {0, 1N, 4N, 9N}

    fig, axes = plt.subplots(len(n0_multipliers), 3, figsize=(15, 12))
    fig.suptitle('Wpływ dopełniania zerami (Zero-Padding) na widmo', fontsize=16)

    for i, mult in enumerate(n0_multipliers):
        N0 = mult * N

        # 1. Generowanie jednego okresu sygnału podstawowego
        n_base = np.arange(N)
        s_base = A * (1 - (n_base % N) / N)

        # 2. Dopełnianie zerami
        s_padded = np.concatenate([s_base, np.zeros(N0)])
        total_N = len(s_padded)

        # 3. Obliczenia FFT
        Xk = np.fft.fft(s_padded)
        freqs = np.fft.fftfreq(total_N)

        amp = np.abs(Xk)
        phase = np.angle(Xk)
        phase[amp < 1e-10] = 0 # Czyszczenie szumu

        # --- Wykresy ---

        # Dziedzina czasu
        axes[i, 0].stem(range(total_N), s_padded, linefmt='b', markerfmt='bo', basefmt=" ")
        axes[i, 0].set_title(f'Sygnał (N0={N0}, Suma N={total_N})')
        axes[i, 0].grid(True, alpha=0.3)

        # Widmo amplitudowe
        # Używamy plot zamiast stem dla dużych N, żeby widzieć "ciągłość"
        if total_N > 20:
            axes[i, 1].plot(np.fft.fftshift(freqs), np.fft.fftshift(amp), 'g-')
        else:
            axes[i, 1].stem(np.fft.fftshift(freqs), np.fft.fftshift(amp), linefmt='g', markerfmt='go', basefmt=" ")
        axes[i, 1].set_title(f'Widmo amplitudowe')
        axes[i, 1].grid(True, alpha=0.3)

        # Widmo fazowe
        if total_N > 20:
            axes[i, 2].plot(np.fft.fftshift(freqs), np.fft.fftshift(phase), 'm-')
        else:
            axes[i, 2].stem(np.fft.fftshift(freqs), np.fft.fftshift(phase), linefmt='m', markerfmt='mo', basefmt=" ")
        axes[i, 2].set_title(f'Widmo fazowe')
        axes[i, 2].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('3_zero_padding_analysis.png', dpi=300)
    plt.show()

exercise_three()