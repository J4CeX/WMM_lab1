import numpy as np
import matplotlib.pyplot as plt


def exercise_one():
    N = 8        # Liczba próbek
    T = 2        # Okres sygnału s(t) = cos(pi*t) f = 0.5Hz, T = 1/f = 2
    fs = N / T   # Częstotliwość próbkowania (4 Hz)
    dt = 1 / fs  # Krok czasowy (0.25 s)

    t = np.arange(N) * dt
    s = np.cos(np.pi * t)

    Xk = np.fft.fft(s)
    f_axis = np.fft.fftfreq(N, dt)  # Oś częstotliwości

    # Widmo amplitudowe i fazowe
    modul = np.abs(Xk)
    faza = np.angle(Xk)

    energia_czas = np.sum(s**2)
    energia_fouriera = np.sum(modul**2) / N

    print("--- Weryfikacja Twierdzenia Parsevala ---")
    print(f"Suma kwadratów w dziedzinie czasu: {energia_czas:.4f}")
    print(f"Suma kwadratów w dziedzinie częstotliwości (znormalizowana): "
          f"{energia_fouriera:.4f}")
    print(f"Różnica: {abs(energia_czas - energia_fouriera)}")

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
    plt.stem(f_axis, modul, basefmt=" ", linefmt='g', markerfmt='go')
    plt.title('Widmo amplitudowe $|X[k]|$')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Moduł')
    plt.grid(True)

    # Widmo fazowe
    plt.subplot(3, 1, 3)
    faza_clean = np.where(modul > 1e-10, faza, 0)
    plt.stem(f_axis, faza_clean, basefmt=" ", linefmt='m', markerfmt='mo')
    plt.title('Widmo fazowe $\\arg(X[k])$')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Faza [rad]')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
