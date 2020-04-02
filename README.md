vna_comms v1.0.2

Changelog:

-Incorporated averaging capabilities into the setup function. Averaging factor is now an new argument for setup()

-Completed calibration function. Wording of calibration prompts may need to be improved.

-Added a dummy output generator sample_output.py. Calling the get_data() functions (no args required) will automatically return a dataset with 3600 data points (10 frequencies, 1 degree increments)

-------------------------------------------------------------------------------------------------------------------------------------
Packages used for testing:


-NI VISA: 19.5 (64-bit) (https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456)

-Python: 3.8.2 (64-bit)

-PyVISA: 1.10.1 (https://pyvisa.readthedocs.io/en/latest/)

-numpy: 1.18.2
