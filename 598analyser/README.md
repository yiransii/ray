## Make executable 
chmod +x analyzer.py 

## Run Script
### Helper Message
You can see all of the arguments and what they are supposed to do/what type they expect\
./analyzer.py -h 

### Two Types of Runs
The script will always print the average price of all the similar node types.\
If the flag --generate-yaml is provided the script will automatically format the proper yaml and print it out.\
If this flag is not present, the names of the cheapest instances will just be printed out in a list.\
\
Example 1: ./analyzer.py --cpu-lbound 2 --mem-lbound 6.5 --cluster-diversity 5 --provider GCP\
Example 2: ./analyzer.py --cpu-lbound 8 --mem-lbound 64 --cluster-diversity 3 --provider GCP --generate-yaml\
Example 3: ./analyzer.py --cpu-lbound 12 --mem-lbound 32 --cluster-diversity 3 --provider AWS --generate-yaml\
\
Note that the yamls generated for AWS and GCP are slightly different. Also note that prices for GCP are transient (and therefore cheap), but for AWS are non-transient are therefore much higher. Collecting transient data for AWS was much more difficult.