#!/usr/bin/python

import sys

FILENAME = "gcp_data.txt"
PROVIDER = "gcp"
THREDSHOLD = 2
INS_NAME = "e2-standard-2"

class GCPInstance: 
    def __init__(self, name, cpu, mem, bandwidth):
        self.name = name
        self.cpu = cpu 
        self.mem = mem 
        self.bandwidth = bandwidth
    
    def printStatus(self):
        print("Name: {}, #cpu: {}, mem(GB): {}, bandwidth(Gbps): {}".format(self.name, self.cpu, self.mem, self.bandwidth))

class Analyser:
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
        # print("run")
    
    def find_similar_ins(self, ins_name, th):
        if self.provider == "gcp":
            return self.analysis_gcp(ins_name, th)
        elif self.provider == "aws":
            return self.analysis_aws(ins_name, th)
        print("find")

    def parse_instance_data_gcp(self):
        f = open(self.filename, "r")
        first_line = True
        for line in f: 
            if first_line:
                first_line = False 
                continue
            li = line.split()
            instance = GCPInstance(li[0], int(li[1]), float(li[2]), float(li[6]))
            self.instances[li[0]] = instance
        f.close()
        
    def analysis_gcp(self, ins_name, th):
        ans = []
        target = self.instances[ins_name]
        for name in self.instances:
            if name == target.name:
                continue
            ins = self.instances[name]
            if self.is_instance_similar(target, ins, th):
                ins.printStatus()
                ans.append(ins.name)
        return ans  

    def parse_instance_data_aws(self):
        #TODO 
        return ""

    def analysis_aws(self, ins_name, th):
        #TODO 
        return ""

    def is_instance_similar(self, a, b, th):
        return self.is_cpu_similar(a.cpu, b.cpu, th) and self.is_mem_similar(a.mem, b.mem, th) and self.is_bandwidth_similar(a.bandwidth, b.bandwidth, th)

    def is_cpu_similar(self, a, b, th):
        if a >= b and b * th >= a: 
            return True 
        if b >= a and a * th >= b:
            return True
        return False 

    def is_mem_similar(self, a, b, th):
        if a >= b and b * th >= a: 
            return True 
        if b >= a and a * th >= b:
            return True
        # if b <= a * (1+th) and b >= a * (1-th):
        #     return True
        return False 

    def is_bandwidth_similar(self, a, b, th): 
        if a >= b and b * th >= a: 
            return True 
        if b >= a and a * th >= b:
            return True
        # if b <= a * (1+th) and b >= a * (1-th):
        #     return True
        return False

if __name__ == "__main__":
    if "-h" in sys.argv or len(sys.argv) < 3: 
        print("HELP: ./analyser.py [thredshold] [instancename]")
    else :
        ins_name = sys.argv[1]
        thredshold = float(sys.argv[2])
        
        a = Analyser(FILENAME, PROVIDER) 
        a.find_similar_ins(ins_name, thredshold)
