$dateInput = Read-Host -Prompt "Enter the date in the format DD-MM--YY"
$shiftInput = Read-Host -Prompt "Enter the shift (A, B, C ...)"
$registerInput = Read-Host -Prompt "Enter the register number"
$rsPath = "C:\DDA\station\data\RS" + $dateInput + ".D" + $registerInput + $shiftInput