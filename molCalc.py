import tkinter as tk

#// TODO: Add additional entry for Mass and Concentration for alt values
#// TODO: Add Calculate Button for Mass and Concentration EDIT: Only One Calculate Button is needed and I've updated it to consider alt values too
#// TODO: Add Swap Alt Value Checkbox
#// TODO: Make the Swap Alt Values Checkbox actually work
#//

root = tk.Tk()
root.title("MolCalc v1.0")
root.geometry("480x400")
root.resizable(False, False)

try:
    from PIL import ImageTk, Image
    PROGRAM_ICON = ImageTk.PhotoImage(Image.open("placeholder.jpg"))
    root.iconphoto(True, PROGRAM_ICON)
except ModuleNotFoundError:
    pass    # Don't wanna download software without the user knowing. This one's not important anyway.


class UnitType:
    def __init__(self, name, unit, alt_name, alt_unit, converfactor):
        self.name = name
        self.unit = unit
        self.alt_name = alt_name
        self.alt_unit = alt_unit
        self.converfactor = converfactor
    
def Calculate():
    global OUTPUT_VALUES
    OUTPUT_VALUES = []
    value = input_entry.get()

    # If the second box is required, store its value in alt_value
    if current_unit_type.converfactor == None:
        alt_value = input_entry_alt.get()
        try: 
            alt_value = float(alt_value)
        except ValueError:
            return ShowOutput(["", "", "", "", ""])

    try:
        value = float(value)
    except ValueError:
        return ShowOutput(["", "", "", "", ""])
    
    # ! kms for naming variables
    altput_value1 = output_entry_alt1.get() 
    altput_value2 = output_entry_alt2.get()

    # For Mass and Concentration, retreive the values of altput, if illegal, reset it to 1
    try:
        altput_value1 = float(altput_value1)
    except ValueError:
        altput_value1 = float(1.0)
        output_entry_alt1.delete(0, tk.END)
        output_entry_alt1.insert(0, 1)

    try:
        altput_value2 = float(altput_value2)
    except ValueError:
        altput_value2 = float(1.0)
        output_entry_alt2.delete(0, tk.END)
        output_entry_alt2.insert(0, 1)

    # Convert input value into moles
    if current_unit_type.converfactor == None:
        value = (value/alt_value)
    else:
        value = (value/current_unit_type.converfactor)

    # ! Horrendous code lol
    # Convert moles into each unit type and append to OUTPUT_VALUES list
    for unittype in RADIOBUTTON_OPTIONS:
        if unittype.converfactor == None:                   # If mass or concentration
            if unittype.name == "Mass":                         # If mass
                if state_checkbox1.get() == 1:                      # If swapped values for mass, the formula is reversed
                    value_new = (altput_value1/value)
                else:
                    value_new = (value*altput_value1)
            else:                                               # If concentration
                if state_checkbox2.get() == 1:                      # If swapped values for concentration, the formula is reversed
                    value_new = (altput_value2*value) # ? Turns out I messed up the concentration formula earlier so now this is what this part of the code looks like
                else:                                       
                    value_new = (value/altput_value2)
        else:                                               # Otherwise, carry on by multiplying with its conversion factor
            value_new = (value*unittype.converfactor)
        value_new = round(value_new, roundto.get())
        if roundto.get() == 0:
            value_new = int(value_new)
        OUTPUT_VALUES.append(value_new)

    ShowOutput(OUTPUT_VALUES)

def ShowOutput(OUTPUT_VALUES):
    # Inserts output from OUTPUT_VALUES into each entry
    for entry in OUTPUT_ENTRIES:
        entry_index = OUTPUT_ENTRIES.index(entry)
        entry["state"] = "normal"
        entry.delete(0, tk.END)
        entry.insert(0, OUTPUT_VALUES[entry_index])
        entry["state"] = "readonly"    


# When a Radio Button is pressed in the input
# current_unit_type holds the UnitType of the currently selected unit
def SetUnitType():
    global input_name
    global input_name_alt
    global input_unit
    global input_unit_alt
    global current_unit_type
    current_unit_type = RADIOBUTTON_OPTIONS[conversionid.get()]     
    
    input_name.destroy()
    input_name_alt.destroy()
    input_unit.destroy()
    input_unit_alt.destroy()
    input_name = tk.Label(input_frame, text=current_unit_type.name, width=10)
    input_name.grid(row=1, column=0, sticky="w")

    if current_unit_type.alt_name == None:
        input_name_alt = tk.Label(input_frame, text="N/A", width=15)
        input_entry_alt["state"] = "normal"
        input_entry_alt.delete(0, tk.END)
        input_entry_alt["state"] = "disabled"
    else:
        input_name_alt = tk.Label(input_frame, text=current_unit_type.alt_name, width=15)
        input_entry_alt["state"] = "normal"

    input_name_alt.grid(row=1, column=3, sticky="w")

    input_unit = tk.Label(input_frame, text=current_unit_type.unit, width=10, anchor="w")
    input_unit.grid(row=2, column=1, sticky="w")

    input_unit_alt = tk.Label(input_frame, text=current_unit_type.alt_unit, width=10, anchor="w")
    input_unit_alt.grid(row=2, column=4, sticky="w")

# Checkbox1 swaps g and g/mol
def ToggleAltValueOne():
    global output_unit_g
    global output_label_alt1
    global output_entry_g
    global output_entry_alt1

    output_unit_g.destroy()
    output_label_alt1.destroy()

    if state_checkbox1.get() == 1:
        output_unit_g = tk.Label(output_frame, text="g/mol", width=11, anchor="w")
        output_label_alt1= tk.Label(output_frame, text="g", width=5, anchor="w")
    else:
        output_unit_g = tk.Label(output_frame, text="g", width=11, anchor="w")
        output_label_alt1= tk.Label(output_frame, text="g/mol", width=5, anchor="w")

    # Swapping the values from both entries
    output_entry_g["state"] = "normal"
    
    intermediate_val = output_entry_g.get()
    output_entry_g.delete(0, tk.END)
    output_entry_g.insert(0, output_entry_alt1.get())
    output_entry_alt1.delete(0, tk.END)
    output_entry_alt1.insert(0, intermediate_val)

    output_entry_g["state"] = "readonly"

    output_unit_g.grid(row=1, column=2, sticky="w")
    output_label_alt1.grid(row=1, column=4, sticky="w")

# Checkbox1 swaps mol/L and L
def ToggleAltValueTwo():
    global output_unit_cv
    global output_label_alt2
    global output_entry_cv
    global output_entry_alt2

    output_unit_cv.destroy()
    output_label_alt2.destroy()

    if state_checkbox2.get() == 1:
        output_unit_cv = tk.Label(output_frame, text="L", width=11, anchor="w")
        output_label_alt2= tk.Label(output_frame, text="mol/L", width=5, anchor="w")
    else:
        output_unit_cv = tk.Label(output_frame, text="mol/L", width=11, anchor="w")
        output_label_alt2= tk.Label(output_frame, text="L", width=5, anchor="w")

    # Swapping the values from both entries
    output_entry_cv["state"] = "normal"
    
    intermediate_val = output_entry_cv.get()
    output_entry_cv.delete(0, tk.END)
    output_entry_cv.insert(0, output_entry_alt2.get())
    output_entry_alt2.delete(0, tk.END)
    output_entry_alt2.insert(0, intermediate_val)

    output_entry_cv["state"] = "readonly"

    output_unit_cv.grid(row=4, column=2, sticky="w")
    output_label_alt2.grid(row=4, column=4, sticky="w")




# Defining the units in the UnitType class, then putting them into RADIOBUTTON_OPTIONS list so its index can be accessed by the For Loop
Unit_mol = UnitType("Moles", "mol", None, None, 1)
Unit_g = UnitType("Mass", "g", "Molecular Weight", "g/mol", None)
Unit_v = UnitType("Volume", "L (@STP)", None, None, 22.4)
Unit_n = UnitType("Particles", "x10^23 atoms", None, None, 6.02)
Unit_cv = UnitType("Concentration", "mol/L", "Volume", "L", None)

RADIOBUTTON_OPTIONS = [Unit_mol, Unit_g, Unit_v, Unit_n, Unit_cv]

# Frame
input_frame = tk.LabelFrame(root, text="Input")
output_frame = tk.LabelFrame(root, text="Output")

# Radio Buttons
conversionid = tk.IntVar()

# For loop mentioned earlier
for unittype in RADIOBUTTON_OPTIONS: # // TODO: Somehow figure out a way to store the both_units tuple. tkinter only likes strings
    tk.Radiobutton(input_frame, text=unittype.name, variable=conversionid, value=RADIOBUTTON_OPTIONS.index(unittype), command=SetUnitType).grid(row=0, column=RADIOBUTTON_OPTIONS.index(unittype))

conversionid.set(0)

# Buttons in Input Frame
input_entry = tk.Entry(input_frame, width=10)
input_entry_alt = tk.Entry(input_frame, width=10, state="disabled")
calculation_button = tk.Button(root, text="Convert", command=Calculate)
#input_button = tk.Button(input_frame, text="honestly idk", command=Button)

# Entries in Output Frame
output_entry_mol = tk.Entry(output_frame, width=10, state="readonly")
output_entry_g = tk.Entry(output_frame, width=10, state="readonly")
output_entry_v = tk.Entry(output_frame, width=10, state="readonly")
output_entry_n = tk.Entry(output_frame, width=10, state="readonly")
output_entry_cv = tk.Entry(output_frame, width=10, state="readonly")

# Labels for units in Output Frame
output_unit_mol = tk.Label(output_frame, text="mol", width=11, anchor="w")
output_unit_g = tk.Label(output_frame, text="g", width=11, anchor="w")
output_unit_v = tk.Label(output_frame, text="L (@STP)", width=11, anchor="w")
output_unit_n = tk.Label(output_frame, text="x10^23 atoms", width=11, anchor="w")
output_unit_cv = tk.Label(output_frame, text="mol/L", width=11, anchor="w")

# Additional Labels and Entries for AltValues in Output Frame
output_entry_alt1 = tk.Entry(output_frame, width=10)
output_entry_alt2 = tk.Entry(output_frame, width=10)

output_label_alt1 = tk.Label(output_frame, text="g/mol", width=5, anchor="w")
output_label_alt2 = tk.Label(output_frame, text="L", width=5, anchor="w")

# Checkboxes in Output Frame
state_checkbox1 = tk.IntVar()
state_checkbox1.set(0)

state_checkbox2 = tk.IntVar()
state_checkbox2.set(0)

output_checkbox1 = tk.Checkbutton(output_frame, text="Swap", variable=state_checkbox1, onvalue=1, offvalue=0, command=ToggleAltValueOne)
output_checkbox2 = tk.Checkbutton(output_frame, text="Swap", variable=state_checkbox2, onvalue=1, offvalue=0, command=ToggleAltValueTwo)

# Rounding Slider in Output Frame
roundto = tk.IntVar()
roundto.set(2)

output_slider = tk.Scale(output_frame, from_=0, to=8, variable=roundto, orient="horizontal")


OUTPUT_ENTRIES = [output_entry_mol, output_entry_g, output_entry_v, output_entry_n, output_entry_cv]

# ? Originally wanted this to just be calling SetUnitType() but kept getting errors at .forget() so here's me rewriting it
# Show Labels in Input Frame
current_unit_type = RADIOBUTTON_OPTIONS[conversionid.get()]
input_name = tk.Label(input_frame, text=current_unit_type.name, width=10)
input_name.grid(row=1, column=0, sticky="w")

input_name_alt = tk.Label(input_frame, text="N/A", width=15)
input_name_alt.grid(row=1, column=3, sticky="w")

input_unit = tk.Label(input_frame, text=current_unit_type.alt_unit, width=10, anchor="w")
input_unit.grid(row=2, column=1, sticky="w")

input_unit_alt = tk.Label(input_frame, text=current_unit_type.alt_unit, width=10, anchor="w")
input_unit_alt.grid(row=2, column=4, sticky="w")

# Grid (You're welcome)
input_frame.grid(row=0, column=0, padx=20, pady=10)
output_frame.grid(row=2, column=0, padx=20, pady=10)
calculation_button.grid(row=1,column=0)

input_entry.grid(row=2, column=0)
input_entry_alt.grid(row=2, column=3)

output_entry_mol.grid(row=0, column=1, sticky="w")
output_entry_g.grid(row=1, column=1)
output_entry_v.grid(row=2, column=1)
output_entry_n.grid(row=3, column=1)
output_entry_cv.grid(row=4, column=1)

output_unit_mol.grid(row=0, column=2, sticky="w")
output_unit_g.grid(row=1, column=2, sticky="w")
output_unit_v.grid(row=2, column=2, sticky="w")
output_unit_n.grid(row=3, column=2, sticky="w")
output_unit_cv.grid(row=4, column=2, sticky="w")

output_entry_alt1.grid(row=1, column=3)
output_entry_alt2.grid(row=4, column=3)

output_checkbox1.grid(row=1, column=5)
output_checkbox2.grid(row=4, column=5)

output_label_alt1.grid(row=1, column=4)
output_label_alt2.grid(row=4, column=4)

tk.Label(output_frame, text="Decimals:").grid(row=6, column=1)
output_slider.grid(row=6, column=2)

for unittype in RADIOBUTTON_OPTIONS:
    tk.Label(output_frame, text=f"{unittype.name}: ", width=15, anchor="w").grid(row=RADIOBUTTON_OPTIONS.index(unittype), column=0)

# White Space
tk.Label(input_frame, text=" ").grid(row=3, column=0)
tk.Label(output_frame, text=" ").grid(row=5, column=0)
tk.Label(output_frame, text=" ").grid(row=7, column=0)

# Yeah
root.mainloop()
