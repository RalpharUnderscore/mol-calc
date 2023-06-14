import tkinter as tk
from PIL import ImageTk, Image

# TODO: Add additional entry for Mass and Concentration for alt values
# TODO: Add Calculate Button for Mass and Concentration
# TODO: Add Swap Alt Value Checkbox

root = tk.Tk()
root.title("MolCalc v1.0")
root.geometry("480x500")

PROGRAM_ICON = ImageTk.PhotoImage(Image.open("placeholder.jpg"))
root.iconphoto(True, PROGRAM_ICON)

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
    
    # Convert input value into moles
    if current_unit_type.converfactor == None:
        value = (value/alt_value)
    else:
        value = (value/current_unit_type.converfactor)

    # Convert moles into each unit type and append to OUTPUT_VALUES list
    for unittype in RADIOBUTTON_OPTIONS:
        if unittype.converfactor == None:
            value_new = (value*1)
        else:
            value_new = (value*unittype.converfactor)
        value_new = round(value_new, 4)
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

# Defining the units in the UnitType class, then putting them into RADIOBUTTON_OPTIONS list so its index can be accessed by the For Loop
Unit_mol = UnitType("Moles", "mol", None, None, 1)
Unit_g = UnitType("Mass", "g", "Molecular Weight", "g/mol", None)
Unit_v = UnitType("Volume", "L @ STP", None, None, 22.4)
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
calculation_button = tk.Button(root, text="Calculate", command=Calculate)
#input_button = tk.Button(input_frame, text="honestly idk", command=Button)

# Entries in Output Frame
output_entry_mol = tk.Entry(output_frame, width=10, state="readonly")
output_entry_g = tk.Entry(output_frame, width=10, state="readonly")
output_entry_v = tk.Entry(output_frame, width=10, state="readonly")
output_entry_n = tk.Entry(output_frame, width=10, state="readonly")
output_entry_cv = tk.Entry(output_frame, width=10, state="readonly")

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


for unittype in RADIOBUTTON_OPTIONS:
    tk.Label(output_frame, text=f"{unittype.name}: ", width=20, anchor="w").grid(row=RADIOBUTTON_OPTIONS.index(unittype), column=0)
    tk.Label(output_frame, text=unittype.unit, width=20, anchor="w").grid(row=RADIOBUTTON_OPTIONS.index(unittype), column=2)

# White Space
tk.Label(input_frame, text=" ").grid(row=3, column=0)
tk.Label(output_frame, text=" ").grid(row=5, column=0)

# Yeah
root.mainloop()