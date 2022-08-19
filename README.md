# suport-list
Script to generate a support map until the end of the year:

## Usage
To run the script, run the following command:

    python3 main.py --names <names> --date DD/MM/YYYY --previous_names <names> 
or 
    python3 main.py --names <names> --date DD/MM/YYYY --previous_names_file <file> 



Where:
* **--names** argument is a list of names that will be generated for the round robin
* **--date** argument is the date to which the round robin list will be generated (by default the end of today's calendar year, where today is day of executrion); this argument must be in the frmat *DD/MM/YYYY*
* **--previous_names** argument is a list of names that should be excluded from the first generation. To use in case you are regenerating the list and don't want people to be on support 3 times in 2 cycles
* **--previous_names_file** argument is the previously generated file for support. Use this for the same reason as above, but makes it easier to follow up.