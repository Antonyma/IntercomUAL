import stun
import argparse
import numpy as np
import struct
import minimal 
import logging

def get_ip_info(stun_host='stun.l.google.com', source_port=4444):
    try:
        nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_host, source_port=source_port)
        return nat_type, external_ip, external_port
    except Exception as e:
        print(f"Error al obtener información de red: {e}")
        return None, None, None

class NAT_traversal(minimal.Minimal):
    pass
if __name__ == "__main__": 
    nat_type, external_ip, external_port = get_ip_info()
    if nat_type is not None:
        print(f"Tipo de NAT: {nat_type}")
        print(f"IP externa: {external_ip}")
        print(f"Puerto externo: {external_port}")
    minimal.args = minimal.parser.parse_known_args()[0]
    otro = NAT_traversal()
    otro.run()

