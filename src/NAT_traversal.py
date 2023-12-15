import stun
import minimal

class NAT_traversal(minimal.Minimal):
    endPoints = []

def get_ip_info(stun_servers):
    try:
        for stun_address in stun_servers:
            host, port = stun_address.strip().split(":")
            nat_type, external_ip, external_port = stun.get_ip_info(stun_host=host, source_port=int(port))            
            endPoint = (external_ip, external_port)    
            if type(external_ip) == str and type(external_port) == int:
                NAT_traversal.endPoints.append(endPoint)
            print(f"External Port: {external_port}\n", 
                f"External IP: {external_ip}\n", 
                f"End-Point: {external_ip}:{external_port}\n", 
                f"NAT type: {nat_type}\n")  

        NAT_TYPE(stun_servers)
        return nat_type, external_ip, external_port
    except OSError as e:
            print(f"Error connecting to STUN server: {e}")

def NAT_TYPE(stun_servers):
    if all(endPoint == NAT_traversal.endPoints[0] for endPoint in stun_servers):
        print("Full Cone NAT")
    if all(endPoint != NAT_traversal.endPoints[0] for endPoint in stun_servers):
        print("Symmetric NAT")
        print("Cannot establish connection with another device.")

if __name__ == "__main__":
    stun_servers = ["stun.l.google.com:4444", "stun1.l.google.com:19302", "stun.l.google.com:19303"]
    nat_type, external_ip, external_port = get_ip_info(stun_servers)
    minimal.args = minimal.parser.parse_known_args()[0]
    otro = NAT_traversal()
    try:
        otro.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
        otro.print_final_averages()
