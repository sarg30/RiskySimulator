
# RiscySimulator
A simulator on the lines of QtSpim for RISC-V architecture made in python

    To run the file with GUI, run the testing.py file
<img src="Screenshot 2022-03-06 125656.png" />

## Phase-1
* Instructions Supported
    * add/sub
    * lw/sw
    * la
    * li
    * beq/bne/blt
    * addi
    * sll
    * jal

* Features
    * Executing the code at once
    * Single step execution
    * Supports 4kb of memory
    * Reads an assembly or text file and executes the instructions and at the end displays the contents of the registers and the memory
    * The GUI has been implemented using Tkinter

A sample code for execution has been added, named grouping.txt, which contains assembly code for bubble sort algorithm. To execute this code, run the testing.py file.

## Phase-2
* Extends the simulator made in phase 1 by incorporating pipelining
* Displays the pipeline for both Data Forwarding Enabled and Date Forwarding Disabled
* Displays the number of stalls and the IPC for both data forwarding toggles
* Pipelining has been implemented as follows:
    * Data Forwarding Enabled:
        * For all instructions an array will store for each register the last clock cycle when MEM stage of pipeline was done for the corresponding register.
        * This array helps when there is data dependency while executing the current instruction, we can easily check for data dependencies using this method just by checking for the last clock cycle when the MEM stage was performed for the concerned registers.
    * Data Forwarding Disabled:
        * For all instructions an array will store for each register the last clock cycle when WB stage of pipeline was done for the corresponding register.
        * This array helps when there is data dependency while executing the current instruction, we can easily check for data dependencies using this method just by checking for the last clock cycle when the WB stage was performed for the concerned registers.
    * Branch Predictor:
        * The simulator uses a brach predictor which assumes that the branch will not be taken, so when the branch is not taken, no stalls are produced. When the branch is taken then that causes a STALL in one cycle of the pipeline.
