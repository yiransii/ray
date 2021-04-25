## Make executable 
chmod +x analyzer.py 

## Run Script
### Helper Message
You can see all of the arguments and what they are supposed to do/what type they expect
./analyzer.py -h 

### Two Types of Runs
The script will always print the average price of all the similar node types.
If the flag --generate-yaml is provided the script will automatically format the proper yaml and print it out.
If this flag is not present, the names of the cheapest instances will just be printed out in a list.

Example 1: ./analyzer.py --cpu-lbound 2 --mem-lbound 6.5 --cluster-diversity 5 --provider GCP
Example 2: ./analyzer.py --cpu-lbound 8 --mem-lbound 64 --cluster-diversity 3 --provider GCP --generate-yaml
