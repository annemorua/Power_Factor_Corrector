import numpy as np

def main(mode, voltage, frequency, desired_pf, a_value, b_value):    #Main function of the code.
    if mode == 0:
        #If the user entered polar mode, no changes should be made to the variables.
        angle = b_value
        amplitude = a_value
    else:
        #If the user entered rectangular mode, the conversion to polar is performed for ease.
        angle = np.rad2deg(np.arctan(b_value / a_value))
        amplitude = np.sqrt(a_value ** 2 + b_value ** 2)
    power_factor = np.cos(np.deg2rad(angle))    #Power factor calculation.
    S = float(voltage ** 2) / float(amplitude)   #Apparent power.
    P = S * power_factor    #Real power.
    Q = S * np.sin(np.deg2rad(angle))    #Reactive power.
    #If the current power factor is equal to or better than the desired one, the rest of the calculation is stopped.
    if power_factor > float(desired_pf):
        return "The current power factor is better than desired."
    elif power_factor == float(desired_pf):
        return "You already have your desired power factor."
    elif angle > 0:    #Inductive case, a capacitor must be added.
        #We solve in advantages.
        angle_n_a = np.rad2deg(-np.arccos(desired_pf))    #New angle in advantages.
        Q_na = P * np.tan(np.deg2rad(angle_n_a))
        Q_xna = Q_na - Q
        Xna = voltage ** 2 / Q_xna    #Capacitor reactance needed.
        C_a = -1 / (2 * np.pi * frequency * Xna) * 10 ** 6    #Calculation of capacitance value.

        #We solve in disadvantages. The variables are different so that all calculations are saved.
        angle_n_b = np.rad2deg(np.arccos(desired_pf))    #New angle in disadvantages.
        Q_nb = P * np.tan(np.deg2rad(angle_n_b))
        Q_xnb = Q_nb - Q
        Xnb = voltage ** 2 / Q_xnb    #Capacitor reactance needed.
        C_b = -1 / (2 * np.pi * frequency * Xnb) * 10 ** 6    #Calculation of capacitance value.

        #Results are returned to power_corrector.py.
        return f"A capacitor must be added between [{C_b:.4f}, {C_a:.4f}]µF"

    else:    #Capacitive case, an inductor must be added.
        #We solve in advantages.
        angle_n_a = np.rad2deg(-np.arccos(desired_pf))    #New angle in advantages.
        Q_na = P * np.tan(np.deg2rad(angle_n_a))
        Q_xna = Q_na - Q
        Xna = voltage ** 2 / Q_xna #Capacitor reactance needed.
        L_a = Xna / (2 * np.pi * frequency) * 10 ** 3    #Calculation of inductance value.

        #We solve in delay. The variables are different so that all calculations are saved.
        angle_n_b = np.rad2deg(np.arccos(desired_pf))    #New angle in disadvantages.
        Q_nb = P * np.tan(np.deg2rad(angle_n_b))
        Q_xnb = Q_nb - Q
        Xnb = voltage ** 2 / Q_xnb    #Capacitor reactance needed.
        L_b = Xnb / (2 * np.pi * frequency) * 10 ** 3    #Calculation of inductance value.

        #Results are returned to power_corrector.py.
        return f"An inductor must be added between [{L_b:.4f}, {L_a:.4f}]mH"

if __name__ == "__main__":
    main(0,120,60,0.9,1323,-88.7)    #Test values in case of starting this code individually.
