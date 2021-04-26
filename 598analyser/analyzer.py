#!/usr/bin/python

import sys
import argparse
import operator
import csv

# FILENAME = "gcp_data.txt"
# PROVIDER = "gcp"

class Instance: 
    def __init__(self, name, cpu, mem, bandwidth, od_price, transient_price):
        self.name = name
        self.cpu = cpu 
        self.mem = mem 
        self.bandwidth = bandwidth
        self.od_price = od_price
        self.transient_price = transient_price
    
    def printStatus(self):
        print("Name: {}, #cpu: {}, mem(GB): {}, bandwidth(Gbps): {}, on-demand price: {}, transient price: {}".format(self.name, self.cpu, self.mem, self.bandwidth, self.od_price, self.transient_price))

class Analyzer:
    def __init__(self, filename, provider):
        self.filename = filename 
        self.provider = provider 
        self.instances = {}

        self.run()

    def run(self):
        if self.provider == "gcp":
            self.parse_instance_data_gcp()
        elif self.provider == "aws":
            self.parse_instance_data_aws()
    
    def find_similar_ins(self, cpu_lbound, mem_lbound):
        if self.provider == "gcp":
            return self.analysis_gcp(cpu_lbound, mem_lbound)
        elif self.provider == "aws":
            return self.analysis_aws(cpu_lbound, mem_lbound)

    def parse_instance_data_gcp(self):
        f = open(self.filename, "r")
        f.readline()
        for line in f: 
            line = line.split()
            instance = Instance(line[0], int(line[1]), float(line[2]), float(line[6]), float(line[7][1:]), float(line[8][1:]))
            self.instances[line[0]] = instance
        f.close()

    def analysis_gcp(self, cpu_lbound, mem_lbound):
        ans = []
        for name in self.instances:
            ins = self.instances[name]
            if self.is_in_bounds(ins, cpu_lbound, mem_lbound):
                #ins.printStatus()
                ans.append(ins)
        return ans  

    def find_cheapest_unique(self, similar_instances):
        group_by_type = dict()
        cheapest_unique = []
        if self.provider == "gcp":
            for instance in similar_instances:
                instance_type = instance.name.split('-')
                instance_type = instance_type[0] + instance_type[1]
                if instance_type not in group_by_type:
                    group_by_type[instance_type] = []
                group_by_type[instance_type].append(instance)
        elif self.provider == "aws":
            for instance in similar_instances:
                instance_type = instance.name.split('.')
                instance_type = instance_type[1]
                if instance_type not in group_by_type:
                    group_by_type[instance_type] = []
                group_by_type[instance_type].append(instance)
        for instance_type in group_by_type:
            lowest_price = float('inf')
            cheapest_instance = None
            for instance in group_by_type[instance_type]:
                if instance.transient_price < lowest_price:
                    lowest_price = instance.transient_price
                    cheapest_instance = instance
            cheapest_unique.append(cheapest_instance)

        return cheapest_unique
    
    def generate_yamls(self, cheapest_unique_k):
        yamls = []
        attr = ['name', 'cpu', 'name']
        for instance in cheapest_unique_k:
            yaml = ''
            i = 0
            with open('{}_template.yaml'.format(self.provider), 'r') as template_f:
                for line in template_f:
                    if '*' in line:
                        line = line.replace('*', str(operator.attrgetter(attr[i])(instance)))
                        i += 1
                    yaml += line
                yamls.append(yaml)
        return yamls


    def parse_instance_data_aws(self):
        fileds = []
        rows = []
        with open("aws_data.csv", 'r') as f:
            csvreader = csv.reader(f)
            fields = next(csvreader)
        
            for row in csvreader:
                rows.append(row)
                try: 
                    name = row[1]
                    cpu = int(row[4].split()[0])
                    mem = float(row[2].split()[0])
                    bandwidth = float(row[21].split()[2])
                    od_price = float(row[35].split()[0][1:])
                    trasient_price = float(row[36].split()[0][1:])
                    instance = Instance(name, cpu, mem, bandwidth, od_price, trasient_price)
                    self.instances[name] = instance
                except: 
                    continue

    def analysis_aws(self, cpu_lbound, mem_lbound):
        ans = []
        for name in self.instances:
            ins = self.instances[name]
            if self.is_in_bounds(ins, cpu_lbound, mem_lbound):
                #ins.printStatus()
                ans.append(ins)
        return ans  

    def is_in_bounds(self, ins, cpu_lbound, mem_lbound):
        return cpu_lbound <= ins.cpu and mem_lbound <= ins.mem

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu-lbound', type=int, help='Lower bound for number of cpus required as an integer, e.g. 2', required=True)
    parser.add_argument('--mem-lbound', type=float, help='Lower bound for amount of memory required as a float, e.g. 7.5', required=True)
    parser.add_argument('--cluster-diversity', type=int, help='How many node types we are interested in as an integer, e.g. 3', required=True)
    parser.add_argument('--provider', type=str, help='The cloud provider we should use as a string, e.g. GCP', required=True)
    parser.add_argument('--generate-yaml', action='store_true')
    args = parser.parse_args()

    cpu_lbound = args.__dict__['cpu_lbound']
    mem_lbound = args.__dict__['mem_lbound']
    diversity_score = args.__dict__['cluster_diversity']
    provider = args.__dict__['provider'].lower()
    generate_yaml = args.__dict__['generate_yaml']
        
    a = Analyzer('{}_data.txt'.format(provider), provider) 
    similar = a.find_similar_ins(cpu_lbound, mem_lbound)

    cheapest_unique = a.find_cheapest_unique(similar)
    cheapest_unique.sort(key=operator.attrgetter('transient_price'))
    cheapest_unique_k = [instance for instance in cheapest_unique][:diversity_score]
    print('Average Price per Hour of Transient Instance Type: {}'.format(sum(instance.transient_price for instance in cheapest_unique_k) / len(cheapest_unique_k)))
    if generate_yaml:
        yamls = a.generate_yamls(cheapest_unique_k)
        for yaml in yamls:
            print(yaml)


    else:
        print('List of Cheapest Transient Instance Types Within Bounds: ' + str([i.name for i in cheapest_unique_k]))


