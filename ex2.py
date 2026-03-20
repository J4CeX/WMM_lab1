import numpy as np
import matplotlib.pyplot as plt


def exercise_two(N=48, A=2):
    n = np.arange(N)
    n0_values = [0, int(N/4), int(N/2), int(3*N/4)]

    fig, axes = plt.subplots(len(n0_values), 3, figsize=(15, 12))
    fig.suptitle(f'Wpływ przesunięcia $n_0$ na widmo (N={N}, A={A})', fontsize=16)

    for i, n0 in enumerate(n0_values):
        # 1. Generowanie sygnału i przesunięcie kołowe
        s_base = A * np.cos(2 * np.pi * n / N)
        s_shifted = np.roll(s_base, n0)

        # 2. Obliczenia FFT
        Xk = np.fft.fft(s_shifted)
        # Normalizacja osi częstotliwości (od -0.5 do 0.5)
        freqs = np.fft.fftfreq(N)

        # Widmo amplitudowe i fazowe
        amp = np.abs(Xk)
        phase = np.angle(Xk)

        # Tłumienie "szumu" fazowego dla prążków o zerowej amplitudzie
        phase[amp < 1e-10] = 0

        # Kolumna 1: Dziedzina czasu
        axes[i, 0].stem(n, s_shifted, linefmt='b', markerfmt='bo', basefmt=" ")
        axes[i, 0].set_title(f'Sygnał $s(n - {n0})$')
        axes[i, 1].set_ylabel('Amplituda')
        axes[i, 0].grid(True, alpha=0.3)

        # Kolumna 2: Widmo amplitudowe
        axes[i, 1].stem(freqs, amp, linefmt='g', markerfmt='go', basefmt=" ")
        axes[i, 1].set_title(f'Widmo amplitudowe (n0={n0})')
        axes[i, 1].grid(True, alpha=0.3)

        # Kolumna 3: Widmo fazowe
        axes[i, 2].stem(freqs, phase, linefmt='m', markerfmt='mo', basefmt=" ")
        axes[i, 2].set_title(f'Widmo fazowe (n0={n0})')
        axes[i, 2].set_ylim(-np.pi-0.5, np.pi+0.5)
        axes[i, 2].set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
        axes[i, 2].set_yticklabels(['-$\pi$', '-$\pi$/2', '0', '$\pi$/2', '$\pi$'])
        axes[i, 2].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('2_time_shift_analysis.png', dpi=300)
    plt.show()


# Wywołanie funkcji
exercise_two()
