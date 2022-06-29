import os
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

class Controller(object):
    def __init__(self):
        print('starting controller')
        if not os.path.exists('topology.json'):
            print("No 'topology.json' file")
            raise Exception
        
        self.topo = load_topo('topology.json')    
        self.controllers = {}
        self.paths = {
            'p1': {'s1', 's4', 's2'},
            'p2': {'s1', 's3', 's2'},
            'p3': {'s1', 's5', 's6', 's2'}
        }
        self.ips = ['10.0.0.1/32', '10.0.0.2/32']
        self.fwdRules = {
            's1' : {
                '10.0.0.1/32 1': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 1': ['00:00:0a:00:00:02', '4'],
                '10.0.0.1/32 2': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 2': ['00:00:0a:00:00:02', '3'],
                '10.0.0.1/32 3': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 3': ['00:00:0a:00:00:02', '5']
            },
            's2' : {
                '10.0.0.1/32 1': ['00:00:0a:00:00:01', '4'],
                '10.0.0.2/32 1': ['00:00:0a:00:00:02', '2'],
                '10.0.0.1/32 2': ['00:00:0a:00:00:01', '3'],
                '10.0.0.2/32 2': ['00:00:0a:00:00:02', '2'],
                '10.0.0.1/32 3': ['00:00:0a:00:00:01', '6'],
                '10.0.0.2/32 3': ['00:00:0a:00:00:02', '2']
            },
            's3' : {
                '10.0.0.1/32 2': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 2': ['00:00:0a:00:00:02', '2'],
            },
            's4' : {
                '10.0.0.1/32 1': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 1': ['00:00:0a:00:00:02', '2']
            },
            's5' : {
                '10.0.0.1/32 3': ['00:00:0a:00:00:01', '1'],
                '10.0.0.2/32 3': ['00:00:0a:00:00:02', '6']
            },
            's6' : {
                '10.0.0.1/32 3': ['00:00:0a:00:00:01', '5'],
                '10.0.0.2/32 3': ['00:00:0a:00:00:02', '2']
            }
        }
        
        self.connect_switches()
        
    def connect_switches(self):
        for p4switch in self.topo.get_nodes():
            if p4switch[0] == 's':
                thrift_port = self.topo.get_thrift_port(p4switch)
                self.controllers[p4switch] = SimpleSwitchThriftAPI(thrift_port)

    def setFastestPath(self, path):
        print('setting fastest path: ' + str(path))
        for switch, control in self.controllers.items():
            #switch is string, control is SimpleSwitchThriftAPI object
            if switch in self.paths[path]:
                for ip in self.ips:
                    # delete old entries for path 0
                    try:
                        control.table_delete_match('ipv4_lpm', [ip, '0'])
                    except:
                        pass
                    
                    # add new rules for path 0
                    action_params = self.fwdRules[switch][ip+' '+ path[1:2]]
                    control.table_add('ipv4_lpm', 'ipv4_forward', [ip, '0'], action_params)
                
                #control.table_dump('ipv4_lpm')
        print('path 0 is set')
        
    def getFastestPath(self):
        file = open('fstPath.txt', 'r')
        fstPath = file.readline()
        print(fstPath)
        return fstPath
        

if __name__ == "__main__":
    cont = Controller()
    
    while True:
        cmd = input("controller> ")
        if cmd == 'exit':
            break
        elif cmd == "fpath":
            fstPath = cont.getFastestPath()
            cont.setFastestPath(fstPath)
        elif cmd.split()[0] == "set-fpath":
            if len(cmd.split()) < 2:
                print('Provide a path to make fastest')
            else:
                print('Using path ' + cmd.split()[1])
                cont.setFastestPath(cmd.split()[1])
        else:
            print('command not found')


