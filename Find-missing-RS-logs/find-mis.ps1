#DECLERATIONS
$date = xxxx #Change this to the desired date (ddmm)
$shift = x #Change this to the desired shift (A, B, C)
$missingTran = @()
$tmp = -1
$firstTran = 0
$dlgPath = "C:\DDA\station\log"
$dlgFiles = Get-ChildItem -Path $dlgPath -Filter "*.dlg" -Recurse
$rsPath = "C:\DDA\station\data\RS" + $date + "24.D1" + $shift
$rsContent = Get-Content -Path $rsPath
$numOfLines = (Get-Content $rsPath | Measure-Object -Line).Lines
$startIndex = 39 #The first index after "rec =" on the dlg file"
#END DECLERATIONS

for ($i = 1; $i -lt $numOfLines; $i++) {
    $line = $rsContent[$i]
    $tranNum = $line.Substring(40 - 1, 52 - 40 + 1)
    if(-not($tranNum -match "^\d+$")){
        continue #Skip the lines that doesn't have a transaction number
    }
    else{
        $tranNum = [int]$tranNum
    }
    $firstTran = $tranNum #Set the first transaction number
    #ADD SCRIPT TO CHECK MATCH FROM PREVIOUS TRANSACTION NUMBER
    if($tmp -lt 0){
        $tmp = $tranNum+1 #Set the next expected transaction number
        continue
    } elseif ($tmp == $tranNum) { #If the expected transaction number is found
        $tmp = $tranNum+1
        continue
    } else { #If the expected transaction number is not found
        $missingTran += $tmp #Add the missing transaction number to the missing transaction array
        $missingTran[$i] += $i + [Math]::Floor($i/2) #Add the line number of the missing transaction number to the missing transaction array
        $tmp = $tranNum+1
    }
}
#Back up the RS file
# Rename the existing file
Rename-Item -Path "C:\DDA\station\data\RS" + $date + "24.D1" + $shift -NewName "old-rs" + $date + "24.D1" + $shift

# Create a new file with the same content
Get-Content $rsPath + "-old" | Set-Content -Path $rsPath

#Replace the missing transaction numbers with the corresponding lines from the dlg files
for($i = 0; $i -lt $missingTran.Length; $i = $i+2){
    foreach ($file in $dlgFiles) {
        $lines = Get-Content -Path $file.FullName
        foreach ($line in $lines) {
            # Check if line contains the specific integer and the string "rec ="
            if ($line -match "rec =" -and $line -match $missingTran[$i]) {
                $sourceLine = $line.Substring($startIndex)
                $rsContent = $rsContent[0..$missingTran[$i+1]] + $sourceLine + $rsContent[$missingTran[$i+1]..$rsContent.Length - 1]
            }
        }
    }
}
