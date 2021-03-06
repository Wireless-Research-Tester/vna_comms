# Changelog
### v1.2.5

- changed data trasnfer from form 4 (ASCII characters) to form 2 (32 bit float), sped up execution by a bit

### v1.2.4

- added better commenting on code
- renamed some syntax fuctions to better represent the performed actions

### v1.2.3

- Minor fix to vna_comms reset() after testing in meas_ctrl

### v1.2.2

- Fixed an issue where dB conversion will return a math domain error
- Changed certain GP-IB commands to use KHz instead of MHz as the unit to reduce execution times.
  - For some reason, the VNA does not deal well with decimals. E.g. "STAR 10.5 MHZ" takes noticeably longer to process than "STAR 10500 KHZ"
  - Input arguments to the functions are still in MHZ, so nothing has changed on the user's end
- Added a reset averaging (rst_avg) function to be used in timing analysis testing. Once timing data is complete, this function will be merged with get_data()
- Rearranged the execution order certain GP-IB commands to ensure that measurement parameters are actually being used during measurements (correction, sweep mode, sweep frequencies, etc.)
- Performed timing analysis with avg_timing.py. Results can be found in vna_timing_results.csv
  - The combinations tested were determined after discussion with Mike
  - There are two times for each testing combination:
    - averaging_complete_time is the time it takes the current averaging number to reach the averaging factor once an averaging reset is triggered
    - get_data_complete_time is the time it takes to run get_data() once to completion.
  - These numbers are the same whether or not correction is turned on
  - Results contain the longest time observed and rounded up to the nearest millisecond
    - Worth noting that the data type (S21 or S11) does not affect averaging time, and the averaging factor does not affect the get_data() completion time

### v1.2.1

- Added exception messages for returned errors
- Fixed some typos in the code

### v1.2.0 

- All vna_comms functions are now part of the same *session* class. No need to repeatedly open and close pyvisa resources and pass redundant data to the functions.
  - To open a new session, call vna_comms.session(Resource) where **Resource** is the resource name for the vna found in list_resources in pyvisa
- Changed data from recording magnitude (dB) only to magnitude (dB) and phase (degrees)
  - This also changes the **data** class structure
  - New function phase() is used to compute the phase from the rectangular form received from the VNA. 
- Removed the **sweep_type** argument from setup() and get_data(). Now the functions will look at the data type for frequency to determine what kind of sweep is appropriate.
- In get_data(), argument **data_type** will be in a string format (i.e. 'S21' or 'S11') instead of 0 and 1. This improves readability of the code.
- **New file**: testbench.py
  - simple script to test vna_comms

### v1.1.0

- **New file**: syntaxes.py
  - Introduces structure for compatibility with different VNA models (most likely HP, Keysight).
  - **check_model** takes the IDN? output as argument, and returns model type.
  - To make code compatible with other VNAs, add model name to class definition and check_model(), and add the equivalent GPIB commands for each action.
  - Now GPIB commands will be sent be calling find_commands() and passing in the following arguments:
    - Model (see class definition).
    - Action (see class definition for all possible actions).
    - Value used in command (if needed).
- Improved wording of calibrate().
- Added IF bandwidth as additional argument for setup.
- Changed frequency units from Hz to MHz (does not apply to IF bandwidth).

### v1.0.2

- Incorporated averaging capabilities into the setup function. Averaging factor is now an new argument for setup()
- Merged get_S21() and get_S11().
- Completed calibration function. Wording of calibration prompts may need to be improved.
- Added a dummy output generator sample_output.py. Calling the get_data() functions (no args required) will automatically return a dataset with 3600 data points (10 frequencies, 1 degree increments).

### v1.0.1

- Markers have been removed from measurement process. They are not necessary.
- Fixed dropped connections issue in get_S21() and get_S11().
- linear frequency mode is now functional. Set sweep type to 0 for linear frequency.

### v1.0.0

- Setup function:
  - data: when data is passed back to the measurement control, it will be in a list of class objects.
    - data class contains: measurement type, frequency, position(theta & phi), and value
	- lin_freq: when vna_comms receives frequency settings, there are two possible formats:
    - for sweeping from a frequency list (sweep type = 1), the frequency settings will be a list of numerical values (smallest to largest) representing the frequencies in Hz.
    - for performing a linear sweep (sweep type = 0), the frequency settings will be an instance of the lin_freq class, which contains: start frequency, end frequency, and number of data points in between.
- Please ensure that the HP-IB address of the VNA is set to 16 for proper connection.
- Reset function complete

-------------------------------------------------------------------------------------------------------------------------------------
Packages used for testing:

- NI VISA: 19.5 (64-bit) (https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456)
- NI 488.2: 19.5 (64-bit) (https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html#329025)
- Python: 3.8.2 (64-bit)
- PyVISA: 1.10.1 (https://pyvisa.readthedocs.io/en/latest/)
