<h1 align="center">Welcome to my ROSEMAN directory 👋</h1>
This directory was created by in order to have a centerlized and orgenized location for all the automations I intend to create in order to make the workflow of the technical support at "ROSEMAN Enginnering" more effective! <br><br>
<p align="center">
  <a href="https://www.roseman.tech/">
    <img src="https://media.licdn.com/dms/image/C4E1BAQFJIo2QCTY_Sw/company-background_10000/0/1595165863888/roseman_engineering_cover?e=2147483647&v=beta&t=VffMSm77VKWzF46rZb_urH5Okf1McHxVT-b5RF2Xag0" alt="button" style="width:300px; height:100px; border-radius:50%; padding:10px;"/>
  </a>
</p>

## How to use this directory 🤔
The only part that is functional is the [Automations](https://github.com/TalsCodingArea/ROSEMAN/tree/main/Automation) folder

You can find an intire list of exe files you can run in any windows computer
<br><br>
<br><br>


## List of Automations 📓

This will have the list of every automation I create and the detailes about each one.
<br><br>

### DLG-merge 🤲🏻🙏🏻
**Input** - The automation will ask you for a date, shift and how many pumps are in the station

**Output** - If the pump and nozzle have been opened and/or closed properly and if so it will create a new file that has all the proccesses that are related to this pump and nozzles in the DLG files

**Description** - Checking for all the pumps and for nozzles 1 to 3 it will output weather the pump and nozzles have been opened, if so it will check if they have a difference in counter.
For the nozzles that have a difference in them the automation will check if the nozzle have been opened and closed properly, and if not it will print that the pump and nozzles have not been closed properly
For each pump and nozzle that have been opened and closed properly it will create a new file for all the processes that are in the DLG files that are related to this specific pump and nozzle

<br><br>
---
<br><br>

### find-mis 🧐
**Input** - The automation will ask you for a date in the format of DDMM and shift (A, B, C...)

**Output** - The function doesn't output anything on the command prompt but creates a new RS file

**Description** - This automation is going through the entire RS file and find the missing transactions numbers according the ascending order wiriting the missing transaction to an array.
Afterwards, for each transaction number in the array, it looks for information in the DLG files for those specific transactions. It the the automation finds the transaction information it adds the missing transaction to the RS file in the correct position.
Before entering the information to the RS file it create a backup RS file.

<br><br>
---
<br><br>

### RFC-updater ⬆️📥
**Input** - This automation doesn't ask for input

**Output** - The automation doesn't output anything on the command prompt

**Description** - The RFC updater makes sure all the necessary files are well written in order to update the RFC

