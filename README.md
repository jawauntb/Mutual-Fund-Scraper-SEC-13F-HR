This is a program that returns form 13F-HR data from the SEC.gov's Edgar database. It works by entering a the CIK or symbol of a mutual fund into the command line. this program can be executed by doing the following: 1. download the folder with all contents; 2. open up the command line interface 3. set up the virtual running environment by typing in "source {path where download is stored}/quovo_fund_holdings/venv/bin/activate" into the command line; 4. enter into project directory by typing "{path where download is stored}/quovo_fund_holdings/main"; 5. in main, enter "python fund_search.py  {cik or symbol to be searched}" 6. navigate to the tmp directory in your computer and open the file with the specified path in excel or some text/table viewing program

I hope you enjoy!

notes:

This project focuses on extracting data tables from 13F-HR files. For files of other formats, an xml extractor should be implemented to pull the raw data. 

The xml extraction pipeline must do a variety of tasks, including the following: checking that the XML is well formed, fixing any errors in poorly formed XML, creating a function to convert the xml into a list of element trees or beautiful soup(alternately, one may implement an algorithm that uses regular expressions to take the tag names and use them as the headers or keys for the data, followed by extracting text elements enclosed within xml and continuing the following), converting the transitional data structure into a list of dictionaries where the text inside of tags serve as values which correspond to tags as keys. 

The complications behind implementing such an algorithm involve understanding the structure of the document beforehand, as well as knowledge of its depth and normalizing the data so that it can be represented as rows and columns in a tsv file, as opposed to tables recursively nested within tables. I have opted not to implement such an algorithm in this case because of the time it would take and potential vulnerabilities I would encounter if the xml file of the 13F was particularly poorly designed. 
