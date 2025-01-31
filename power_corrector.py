import tkinter.messagebox
from pathlib import Path
import numpy as np
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, IntVar, Label
from Circuitos import calculator

def main(): #Function of the code.
    def close_window():    #Closes the window if X is pressed.
        window.destroy()

    def answer(mode, voltage, frequency, desired_pf, a_value, b_value):    #Calculation and display of results.
        #The calculation is done by calculator.py.
        answer = calculator.main(mode, voltage, frequency, desired_pf, a_value, b_value)    #Sending data.
        answer = str(answer)

        #Insert the result into the blank space.
        display.config(text="\n" + answer)

    def variables():    #Variable analysis, error-catching and conversion to float.
        #Error-catching: The user does not enter values in some input.
        if "" in [entry_voltage.get(), entry_frequency.get(), entry_a_value.get(), entry_b_value.get(), entry_p_factor.get()]:
            tkinter.messagebox.showerror("ERROR", "ENTER VALUES ON ALL ENTRIES!")
        else:
            #Error-catching: some value is not numeric.
            try:
                #Converting entered values to floats.
                #Error-catching: Converting commas to periods for Python interpretation.
                voltage = float(entry_voltage.get().replace(",", "."))
                frequency = float(entry_frequency.get().replace(",", "."))
                desired_pf = float(entry_p_factor.get().replace(",", "."))
                a = float(entry_a_value.get().replace(",", "."))
                b = float(entry_b_value.get().replace(",", "."))
                #Error-catching: The desired power factor must be between 0 and 1.
                if desired_pf > 1 or desired_pf < 0:
                    tkinter.messagebox.showerror("ERROR", "POWER FACTOR MUST BE BETWEEN 0 AND 1!")
                else:
                    #Error catching: The user enters 0 in some meaningless field.
                    if voltage <= 0:
                        tkinter.messagebox.showerror("ERROR", "CHECK VOLTAGE INPUT!")
                    elif frequency <= 0:
                        tkinter.messagebox.showerror("ERROR", "CHECK OSCILLATION FREQUENCY INPUT!")
                    elif a <= 0:
                        tkinter.messagebox.showerror("ERROR", "CHECK RESISTANCE INPUT!")
                    else:
                        #The user can choose between polar or rectangular input impedance.
                        if opt.get() == 1:    #Polar option.
                            if tipo_a.get() == 2:    #The user entered polar with radians, we transformed to degrees.
                                b = np.rad2deg(b)
                            #Error catching: User enters an angle outside of the first and fourth quadrants.
                            if b > 90 or b < -90:
                                tkinter.messagebox.showerror("ERROR", "THE ANGLE MUST BE IN THE FIRST OR FOURTH QUADRANT!")
                            #Sending values to a function that performs the calculation and display.
                            else:
                                answer(0, voltage, frequency, desired_pf, a, b)
                        else:    #Rectangular option.
                            #Sending values to a function that performs the calculation and display.
                            answer(1, voltage, frequency, desired_pf, a, b)
            except ValueError:
                tkinter.messagebox.showerror("ERROR", "VALUES ENTERED MUST BE NUMERIC!")

    def summon():    #Changes to the GUI when the user selects options (polar or rectangular, radians or angles).
        if opt.get() == 1:    #User chooses to enter impedance in polar form.
            canvas.itemconfigure(polar, state="normal")
            canvas.itemconfigure(polarsymb, state="normal")
            canvas.itemconfigure(rect, state="hidden")
            canvas.itemconfigure(rectsymb, state="hidden")
            rad_button.place(x=(s_width / 2 + 20) + 170, y=234.0, width=50, height=30)
            deg_button.place(x=(s_width / 2 + 20) + 120, y=234.0, width=50, height=30)
            select_deg()
        else:    #User chooses to enter impedance in rectangular form.
            rad_button.place_forget()
            deg_button.place_forget()
            canvas.itemconfigure(rad, state="hidden")
            canvas.itemconfigure(polar, state="hidden")
            canvas.itemconfigure(deg, state="hidden")
            canvas.itemconfigure(polarsymb, state="hidden")
            canvas.itemconfigure(rect, state="normal")
            canvas.itemconfigure(rectsymb, state="normal")

    def select_deg():    #If user enters polar with angle in degrees, GUI changes.
        tipo_a.set(1)    #Variable for angle in degrees.
        deg_button.config(relief="sunken", bg="#B8DBD9", fg="#000000")
        rad_button.config(relief="raised", bg="#263270", fg="#FFFFFF")
        canvas.itemconfigure(deg, state="normal")
        canvas.itemconfigure(rad, state="hidden")

    def select_rad():    #If user enters polar with angle in radians, GUI changes.
        tipo_a.set(2)    #Variable for angle in radians.
        rad_button.config(relief="sunken", bg="#B8DBD9", fg="#000000")
        deg_button.config(relief="raised", bg="#263270", fg="#FFFFFF")
        canvas.itemconfigure(deg, state="hidden")
        canvas.itemconfigure(rad, state="normal")

    #Creating the GUI.
    window = Tk()
    opt = IntVar()    #Choice variable between polar and rectangular, we start with polar.
    opt.set(1)
    tipo_a = IntVar()    #Variable for the type of angle entered.
    tipo_a.set(1)

    #The GUI is created with the size of the user's screen.
    window.overrideredirect(True)    #Remove the top options bar and adjust the screen.
    s_width = window.winfo_screenwidth()
    s_height = window.winfo_screenheight()
    window.geometry(f"{s_width}x{s_height}")

    #The GUI canvas is created.
    canvas = Canvas(window, bg="#3A7FF6", height=s_height, width=s_width, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    #The create rectangle creates colored spaces for better visualization.
    canvas.create_rectangle((s_width / 2 - 20) - 419, 15.0, s_width / 2 - 20, 370.0, fill="#AA8F66", outline="")
    canvas.create_rectangle((s_width / 2 - 34) - 390, 73.0, s_width / 2 - 34, 84.0, fill="#000000", outline="")
    canvas.create_rectangle((s_width / 2 - 34) - 390, 212.0, s_width / 2 - 34, 223.0, fill="#000000", outline="")
    canvas.create_rectangle((s_width / 2 + 20), 15.0, (s_width / 2 + 41) + 412, 370.0, fill="#263270", outline="")
    canvas.create_rectangle((s_width / 2 - 20) - 419, 402.0, s_width / 2 - 20, 585.0, fill="#B8DBD9", outline="")
    canvas.create_rectangle((s_width / 2 + 41), 73.0, (s_width / 2 + 41) + 377, 84.0, fill="#000000", outline="")
    canvas.create_rectangle((s_width / 2 + 41), 212.0, (s_width / 2 + 41) + 377, 223.0, fill="#000000", outline="")
    canvas.create_rectangle((s_width / 2 - 20) - 419, 607.0, (s_width / 2 + 41) + 412, 618.0, fill="#080808",outline="")

    #The create text creates titles as a guide for the user to know where to enter the values.
    canvas.create_text((s_width / 2 - 20) - 405, 35.0, anchor="nw", text="Fuente", fill="#000000", font=("Roboto Bold", 24 * -1))
    canvas.create_text((s_width / 2 - 34) - 380, 95.0, anchor="nw", text="voltage", fill="#000000", font=("Roboto Bold", 24 * -1))
    canvas.create_text((s_width / 2 - 34) - 380, 234.0, anchor="nw", text="frequency", fill="#000000", font=("Roboto Bold", 24 * -1))
    canvas.create_text((s_width / 2 + 20) + 21, 35.0, anchor="nw", text="Impedancia", fill="#FFFFFF", font=("Roboto Bold", 24 * -1))
    polar = canvas.create_text((s_width / 2 + 20) + 43, 234.0, anchor="nw", text="Polar", fill="#FFFFFF", font=("Roboto Bold", 24 * -1))
    rect = canvas.create_text((s_width / 2 + 20) + 43, 234.0, anchor="nw", text="Rectangular", fill="#FFFFFF", font=("Roboto Bold", 24 * -1))
    rectsymb = canvas.create_text((s_width / 2 + 20) + 197, 294.0, anchor="nw", text="+ j", fill="#FFFFFF", font=("Inter", 24 * -1))
    polarsymb = canvas.create_text((s_width / 2 + 20) + 197, 294.0, anchor="nw", text="∠", fill="#FFFFFF", font=("Inter", 24 * -1))
    canvas.create_text((s_width / 2 - 20) - 405, 421.0, anchor="nw", text="Factor de potencia deseado", fill="#000000", font=("Roboto Bold", 24 * -1))
    deg = canvas.create_text((s_width / 2 + 20) + 382, 294.0, text="°", fill="#FFFFFF", font=("Inter", 24 * -1))
    rad = canvas.create_text((s_width / 2 + 20) + 397, 307.5, text="rad", fill="#FFFFFF", font=("Inter", 23 * -1))
    canvas.itemconfigure(rad, state="hidden")

    #Initially, the polar text and symbol are displayed and the rectangular ones are hidden.
    canvas.itemconfigure(polar, state="normal")
    canvas.itemconfigure(polarsymb, state="normal")
    canvas.itemconfigure(rect, state="hidden")
    canvas.itemconfigure(rectsymb, state="hidden")

    #Inputs for each of the variables that the user must enter.

    #1. Supply voltage.
    entry_voltage = Entry(bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0, font=("Helvetica", 15))
    entry_voltage.place(x=(s_width / 2 - 20) - 370, y=129.0, width=321.0, height=59.0)

    #2. Voltage oscillation frequency.
    entry_frequency = Entry(bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0, font=("Helvetica", 15))
    entry_frequency.place(x=(s_width / 2 - 20) - 370, y=273.0, width=321.0, height=59.0)

    #3. Impedance value a (amplitude in polar mode, actual value in rectangular mode).
    entry_a_value = Entry(bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0, font=("Helvetica", 15))
    entry_a_value.place(x=(s_width / 2 + 20) + 55, y=279.0, width=129.029, height=59.0)

    #4. Impedance b value (angle in polar mode, imaginary value in rectangular mode).
    entry_b_value = Entry(bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0, font=("Helvetica", 15))
    entry_b_value.place(x=(s_width / 2 + 20) + 244, y=279.0, width=129.029, height=59.0)

    #5. Power factor desired by the user.
    entry_p_factor = Entry(bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0, font=("Helvetica", 15))
    entry_p_factor.place(x=(s_width / 2 - 20) - 370, y=488.0, width=321.0, height=59.0)

    #Text output for the results display.
    display = Label(canvas, bd=0, bg="#F1F5FF", fg="#000716", font=("Helvetica", 15))
    display.place(x=s_width / 2 - 786 / 2, y=655, width=786, height=59)

    #Buttons to select impedance mode.
    polar_opt = Radiobutton(text="Ingresar en forma polar", font=("Helvetica", 16), fg="#FFFFFF", bg="#263270", value=1, variable=opt, command=summon)
    polar_opt.place(x=(s_width / 2 + 20) + 25, y=100.0)
    rect_opt = Radiobutton(text="Ingresar en forma rectangular", font=("Helvetica", 16), fg="#FFFFFF", bg="#263270", value=2, variable=opt, command=summon)
    rect_opt.place(x=(s_width / 2 + 20) + 25, y=150.0)

    #Buttons to select between radians and degrees.
    deg_button = Button(text="DEG",relief="sunken", bg="#B8DBD9", fg="#000000", font=("Helvetica", 16), command=select_deg)
    deg_button.place(x=(s_width / 2 + 20) + 120, y=234.0, width=50, height=30)
    rad_button = Button(text="RAD", bg="#263270", fg="#FFFFFF", font=("Helvetica", 16), command=select_rad)
    rad_button.place(x=(s_width / 2 + 20) + 170, y=234.0, width=50, height=30)

    #An exit button is created to close the window, run close_window().
    exit_button = Button(canvas, text="✕", fg="white", bg="red", command=close_window)
    exit_button.place(x=s_width - 26, y=s_height - (s_height - 5))

    #Start calculation button, run variables().
    run_button = Button(text="Run", command=variables, relief="flat", font=("Arial", 20, "bold"), fg="blue", bg="white")
    run_button.place(x=(s_width / 2 + 20) + 83, y=451.0, width=253.449, height=98.0)

    #pack.forget() makes sure to remove objects so that there are no duplicates or crashes when switching aspects.
    canvas.pack_forget()

    window.mainloop() #GUI mainloop.
if __name__  == "__main__":
    main()
