#DECLERATIONS
$rfcInstallerPath = "C:\DDA\station\log\rfc-installer.log"
$chPath = "C:\DDA\station\CH.PRM"
$procPath = "C:\DDA\station\RFC_PROC.INI"
$iniPath =  "C:\DDA\station\RFC_3000.INI"
$prmPath = "C:\DDA\station\STATION.PRM"
#END DECLERATIONS

#Step 1: Check for "FUEL4" line on the CH.PRM file
$chContent = Get-Content -Path $chPath
$managerFlag = $false
$linesToAdd = "210705 FUEL4" + "`n"
for ($i = 0; $i -lt $chContent.Length; $i++) {
    if ($chContent[$i] -match "MANAGER" -and $managerFlag -eq $false) {  #Checks if we are on the MANAGER section
        $managerFlag = $true
        continue
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
        $chContent = $chContent[0..($i-1)] + "210705 FUEL4" + "`n" + $chContent[$i..($chContent.Length - 1)] #Add the FUEL4 line
        break
    }
}
Set-Content -Path $chPath -Value $chContent
Write-Output "Step 1 completed"

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
            for($j=0; $j -lt 4; $j++) {
                $procContent[$i] = "//" + $procContent[$i]
                $i++
            }
        Write-Output "Added the comments for process 20"
        continue
        }
    }
    if ($procContent[$i] -match "PROCESS 30") {
        $i++
        if ($procContent[$i] -match "^//") { #Remove the comment if the line after process 30 is commented
            for($j=0; $j -lt 5; $j++) {
                $procContent[$i] = $procContent[$i].Substring(2)
                $i++
            }
            Write-Output "Removed the comment from process 30"
            break
        }
        break
    }
}
Set-Content -Path $procPath -Value $procContent
Write-Output "Step 2 completed"

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
Write-Output "Step 3 completed"

#Step 4: Validate STATION.PRM
$prmContent = Get-Content -Path $prmPath
for ($i = 1; $i -lt $prmContent.Length; $i++) {
    if(-not(($prmContent[$i].Substring(73, 2)) -match "\d")){
        Write-Output "line $i does not have an integer"
        continue #Skip the lines that doesn't have a transaction number
    }
    else{
        $Spc = [int]($prmContent[$i].Substring(73, 2))
        if ($Spc -eq 8) {
            continue
        }
        else {
            $Spc = $Spc + 8
            $prmContent[$i] = $prmContent[$i].Substring(0, 73) + $spc + $prmContent[$i].Substring(75)
            Write-Output "The line is updated"
        }
    }
}
Set-Content -Path $prmPath -Value $prmContent
Write-Output "The new content has been set"
Write-Output "Step 4 completed"
Start-Sleep -Seconds 5