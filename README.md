vna_comms v1.0.1

Changelog:


-Markers have been removed from measurement process. They are not necessary.

-Fixed dropped connections issue in get_S21() and get_S11()

-linear frequency mode is now functional. Set sweep type to 0 for linear frequency.


To-do:

-need to incorporate averaging capabilities into the setup function

-calibration function

-------------------------------------------------------------------------------------------------------------------------------------
Packages used for testing:


-NI VISA: 19.5 (64-bit) (https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456)

-Python: 3.8.2 (64-bit)

-PyVISA: 1.10.1 (https://pyvisa.readthedocs.io/en/latest/)

-numpy: 1.18.2
