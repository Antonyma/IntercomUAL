import stun
import numpy as np
import minimal 

class NAT_traversal(minimal.Minimal):
    endPoints = []

def get_ip_info():

    with open("lista_ip.txt") as archivo:
        for linea in archivo:
            host, port = linea.strip().split(":")
            nat_type, external_ip, external_port = stun.get_ip_info(stun_host=host, source_port=(int)(port))            
            endPoint = (external_ip, external_port)    
            if (type(external_ip)==str and type(external_port)==int):
                NAT_traversal.endPoints.append(endPoint)
            print(f"External Port: {external_port}\n",f"External IP: {external_ip}\n", f"End-Point: {external_ip}:{external_port}\n", f"NAT type: {nat_type}\n")  
            if all(endPoint == NAT_traversal.endPoints[0] for endPoint in NAT_traversal.endPoints):
                print("*****Full Cone NAT***** \n")
            else:
                print("*****Symetric NAT*****")
                print("No puede establecer conexion con otro dispositivo.\n")
    return nat_type, external_ip, external_port

if __name__ == "__main__": 
    nat_type, external_ip, external_port = get_ip_info()
    minimal.args = minimal.parser.parse_known_args()[0]
    otro = NAT_traversal()
    otro.run()  