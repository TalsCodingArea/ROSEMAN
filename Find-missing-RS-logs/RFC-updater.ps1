#DECLERATIONS
$rfcInstallerPath = "C:\DDA\station\log\rfc-installer.log"
$chPath = "C:\DDA\station\CH.PRM"
$procPath = "C:\DDA\station\RFC_PROC"
$iniPath =  "C:\DDA\station\RFC_3000"
$prmPath = "C:\DDA\station\STATION.PRM"
#END DECLERATIONS

#Step 1: Check for "FUEL4" line on the CH.PRM file
$chContent = Get-Content -Path $chPath
$managerFlag = $false
for ($i = 0; $i -lt $chContent.Length; $i++) {
    if ($chContent[$i] -match "MANAGER" -and $managerFlag -eq $false) {  #Checks if we are on the MANAGER section
        $managerFlag = $true
        break
    }
    if ($chContent[$i] -match "MANAGER" -and $managerFlag -eq $true) { #Skip all the MANAGER lines
        continue
    }
    if ($chContent[$i] -eq "" -and $managerFlag -eq $true) { #Skip all the empty lines after the manager section
        continue
    }
    if (-not($chContent[$i] -eq "") -and $managerFlag -eq $true){ #The first non empty line after the manager section
        if ($chContent[$i] -match "FUEL4") {
            Write-Output "FUEL4 line found on CH.PRM file"
            break
        }
        $chContent = $chContent[0..$i-1] + "210705 FUEL4" + "`r`n" + $chContent[$i..$chContent.Length - 1] #Add the FUEL4 line
    }
}

#Step 2: Validate process 20 and process 30 on RFC_PROC
$procContent = Get-Content -Path $procPath
$newLines = @()
for ($i = 0; $i -lt $procContent.Length; $i++) {
    if ($procContent[$i] -match "PROCESS 20") { 
        $i++
        if ($procContent[$i] -match "^//") { #If the lineafter process 20 is commented
            $i = $i + 3
            $newLines += 0
            continue
        }
        else { #Change the lines to be commented
            $newLines += 1
            $newLines += $i
            $newLines += "//" + $procContent[$i]
            $i++
            $newLines += "//" + $procContent[$i]
            $i++
            $newLines += "//" + $procContent[$i]
            $i++
            $newLines += "//" + $procContent[$i]
        }
        continue
    }
    if ($procContent[$i] -match "PROCESS 30") {
        $i++
        if ($procContent[$i] -match "^//") { #Remove the comment if the line after process 30 is commented
            $newLines[0] += 1
            $newLines += $i
            $procContent[$i].replace("//", "")
            $i++
            $procContent[$i].replace("//", "")
            $i++
            $procContent[$i].replace("//", "")
            $i++
            $procContent[$i].replace("//", "")
            break
        }
        break
    }
}
#Settin the new lines
if ($newLines[0] -eq 1) {
    for ($i = 2; $i -lt 6; $i++) {
        $procContent[$newLines[1]] = $newLines[$i]
        $newLines[1]++
    }
}
elseif ($newLines[0] -eq 2) {
    for ($i = 7; $i -lt 11; $i++) {
        $procContent[$newLines[6]] = $newLines[$i]
        $newLines[6]++
    }
}
Set-Content -Path $procPath -Value $procContent

#Step 3: Validate RFC_3000
$iniContent = Get-Content -Path $iniPath
for ($i = 0; $i -lt $iniContent.Length; $i++) {
    if ($iniContent[$i] -match "^Company") {
        if ($iniContent[$i] -match "fuel4") {
            Write-Output "fuel4 line found on RFC_3000 file"
            break
        }
        else {
            $iniContent[$i] += ",fuel4"
            Write-Output "Added 'fuel4' to Company line on RFC_3000 file"
            break
        }
    }
}
Set-Content -Path $iniPath -Value $iniContent

#Step 4: Validate STATION.PRM
$prmContent = Get-Content -Path $prmPath
for ($i = 1; $i -lt $prmContent.Length; $i++) {
    if (-not($prmContent[$i].Substring(73, 2) -match "8")) {
        continue
    }
    else {
        $tmp = [int]$prmContent[$i].Substring(73, 2) + 8
        $prmContent[$i] = $prmContent[$i].Substring(0, 73) + $tmp + $prmContent[$i].Substring(75)
    }
}
Set-Content -Path $prmPath -Value $prmContent