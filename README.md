# Changelog

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
- numpy: 1.18.2
