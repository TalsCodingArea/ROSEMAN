#DECLERATIONS
$date = xxxx #Change this to the desired date (ddmm)
$shift = x #Change this to the desired shift (A, B, C)
$dateInput = Read-Host -Prompt "Enter the date in the format DDMMYY"
$shiftInput = Read-Host -Prompt "Enter the shift (A, B, C ...)"
$missingTran = @()
$tmp = -1
$firstTran = 0
$dlgPath = "C:\DDA\station\log"
$dlgFiles = Get-ChildItem -Path $dlgPath -Filter "*dlg*" -Recurse
$rsPath = "C:\DDA\station\data\RS" + $dateInput + ".D1" + $shiftInput
$rsContent = Get-Content -Path $rsPath
$numOfLines = (Get-Content $rsPath | Measure-Object -Line).Lines
$startIndex = 39 #The first index after "rec =" on the dlg file"
$count = 0
#END DECLERATIONS

for ($i = 1; $i -lt $numOfLines; $i++) {
    $line = $rsContent[$i]
    $tranNum = $line.Substring(45 - 1, 52 - 45 + 1)
    if(-not($tranNum -match "\d")){
        continue #Skip the lines that doesn't have a transaction number
    }
    else{
        $tranNum = $tranNum -replace '\D', '' #Remove all non-numeric characters
        $tranNum = [int]$tranNum
    }
    #ADD SCRIPT TO CHECK MATCH FROM PREVIOUS TRANSACTION NUMBER
    if($tmp -lt 0){
        $firstTran = $tranNum #Set the first transaction number
        $tmp = $tranNum+1 #Set the next expected transaction number
        continue
    } elseif ($tmp -eq $tranNum) { #If the expected transaction number is found
        $tmp++
        continue
    } else { #If the expected transaction number is not found
        $missingTran += $tmp #Add the missing transaction number to the missing transaction array
        $missingTran += $i + ˙$count
        $count++
        $tmp++
    }
}
#Back up the RS file
# Rename the existing file
$backUpName = "RS" + $dateInput + ".D1" + $shiftInput + "-old"
Rename-Item -Path $rsPath -NewName $backUpName
$backUpPath = "C:\DDA\station\data\" + $backUpName

# Create a new file with the same content
Get-Content $backUpPath | Set-Content -Path $rsPath

#Replace the missing transaction numbers with the corresponding lines from the dlg files
for($i = 0; $i -lt $missingTran.Length; $i = $i+2){
    foreach ($file in $dlgFiles) {
        $lines = Get-Content -Path $file.FullName
        foreach ($line in $lines) {
            # Check if line contains the specific integer and the string "rec ="
            if ($line -match "rec =" -and $line -match $missingTran[$i]) {
                $sourceLine = $line.Substring($startIndex)
                $newContent = $rsContent[0..$missingTran[$i+1]]
                $newContent += $sourceLine
                $newContent += $rsContent[($missingTran[$i+1]+1)..($rsContent.Count - 1)]
                $rsContent = $rsContent[0..$missingTran[$i+1]] + $sourceLine + $rsContent[$missingTran[$i+1]..$rsContent.Length - 1]
            }
        }
    }
}
Set-Content -Path $rsPath -Value $rsContent
