#Chemistry Unit Conversion Calculator

##Changes:  
###v1.1a
- Fixed issue where Molarity would still calculate incorrectly when the units are swapped. Hopefully this is the last time this needs to be fixed.
- Changed "Volume" when Molarity is selected to "Volume (Solution)" for more clarity
- Fixed bug where "x10^23 atoms" would be cut off in the input frame


###v1.1:
- Changed the text near the rounding slider from "Decimal:" to "Round to:" and "Decimals" for more clarity
- Changed the term "Concentration" to "Molarity" for more clarity
- No longer crashes if missing placeholder.jpg (lol)
- Added "Rounded-to-zero" indicator in the form of astericks in front of a number that has been rounded to zero if it's real value isn't
- Clicking the swap checkbox on a unit that has the indictor will remove it. This is done to avoid getting a non-number in the Alt-value entry
- Added text for information on the indicator if the indicator appears
  
###v1.0:
- It works
- Concentration now calculates moles by multiplying concentration with volume, which is the correct way. Formerly calculates moles by dividing concentration with volume, which is just wrong in every way

##Introduction:  
molCalc.pyw is a unit conversion calculator for Chemistry (more specifically Stoichiometry).
The units molCalc.pyw supports are Moles, Mass, Volume (at STP), Particles and Molarity. Once a unit type is selected and a value is given,
the calculator will convert it into every other unit mentioned earlier. Under the Mass and Molarity units in the Output Frame, additional "Alt-Values" entries
are present. You may change these values to get different results. If none are given, they will default to 1. 
If you would like to calculate for their "Alt-Value" instead, for example, if you would like to calculate for Molecular Weight (g/mol) instead of Mass (g).
You can tick the Swap Checkbox to calculate for Molecular Weight instead.
  
##Calculation:  
The Calculation of this program is relatively simple and comes from the fact that all units can be easily converted into moles and moles can be easily converted
back to each unit.  
Begin by converting input unit into moles:
- n = n
- n = g/m
- n = v/22.4 *(v @STP)*
- n = N/6.02 *(keep in mind that the unit for particles this calculator uses is x10^23 atoms)*
- n = cv
  
Then moles is converted into each unit respectively:
- n = n
- g = n\*m
- v = n\*22.4
- N = n\*6.02
- c = n/v
  
If the swap checkbox is ticked, the following equations are used instead:
- m = n/g
- v = n/c
  
Here's a good image to visualize the calculation:  
https://d20khd7ddkh5ls.cloudfront.net/img_5bd217010b9e-1.jpeg




