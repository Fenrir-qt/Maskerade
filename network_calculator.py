import ipaddress
import pandas as pd
import sys
from typing import Optional

class NetworkCalculator:
    # A network analysis tool for calculating network information and host lists
    
    def __init__(self, max_hosts: int = 1000):
        # Initialize the NetworkCalculator with maximum number of hosts to process
        self.max_hosts = max_hosts
        self.network = None
    
    def load_network(self, network_input: str) -> bool:
        # Load a network from string input
        try:
            if not network_input.strip():
                raise ValueError("Please enter a valid network address.")
            
            # Check if user included CIDR notation (the /24 part)
            if '/' not in network_input:
                raise ValueError("Please include CIDR notation (e.g., /24 for IPv4 or /64 for IPv6)")
            
            self.network = ipaddress.ip_network(network_input, strict=False)
            return True
        except ValueError:
            raise
    
    def get_network_input(self) -> None:
        # Get and validate network input from user
        while True:
            try:
                user_input = input('Enter network (e.g. 192.168.1.0/24 or 2001:db8::/32): ').strip()
                
                if self.load_network(user_input):
                    ip_version = "IPv4" if isinstance(self.network, ipaddress.IPv4Network) else "IPv6"
                    print(f"{ip_version} Network '{self.network}' loaded successfully")
                    break
                    
            except ValueError as e:
                print(f"Invalid network format: {e}")
                print("Examples:")
                print("  IPv4: 192.168.1.0/24, 10.0.0.0/16, 172.16.0.0/12")
                print("  IPv6: 2001:db8::/32, fe80::/64, ::1/128")
                
                retry = input("Try again? (y/n): ").lower()
                if retry in ['n', 'no', 'quit', 'exit']:
                    print("Goodbye!")
                    sys.exit(0)
    
    def get_network_info(self) -> dict:
        # Get basic network information
        if not self.network:
            raise ValueError("No network loaded")
        
        total_addresses = self.network.num_addresses
        is_ipv4 = isinstance(self.network, ipaddress.IPv4Network)
        
        # Calculate usable hosts differently for IPv4 vs IPv6
        if is_ipv4:
            # IPv4: subtract 2 for network and broadcast addresses
            total_hosts = total_addresses - 2 if total_addresses > 2 else 0
        else:
            # IPv6: no broadcast address, but still exclude network address
            total_hosts = total_addresses - 1 if total_addresses > 1 else 0
        
        # Safely get first and last host
        try:
            hosts_list = list(self.network.hosts())
            first_host = str(hosts_list[0]) if hosts_list else "N/A"
            last_host = str(hosts_list[-1]) if hosts_list else "N/A"
        except (IndexError, StopIteration):
            first_host = "N/A"
            last_host = "N/A"
        
        info = {
            "IP Version": "IPv4" if is_ipv4 else "IPv6",
            "Network Address": str(self.network.network_address),
            "Network CIDR": str(self.network),
            "Subnet Mask": str(self.network.netmask),
            "Wildcard Mask": str(self.network.hostmask),
            "Broadcast Address": str(self.network.broadcast_address) if is_ipv4 else "N/A (IPv6 doesn't use broadcast)",
            "Network Class": self._get_network_class(),
            "Is Private": self.network.is_private,
            "Total Addresses": total_addresses,
            "Usable Hosts": total_hosts,
            "First Host": first_host,
            "Last Host": last_host
        }
        
        return info
    
    def _get_network_class(self) -> str:
        # Determine the network class for IPv4 or type for IPv6
        if isinstance(self.network, ipaddress.IPv4Network):
            # IPv4 classification based on first octet
            first_octet = int(str(self.network.network_address).split('.')[0])
            
            if 1 <= first_octet <= 126:
                return "A"
            elif 128 <= first_octet <= 191:
                return "B"
            elif 192 <= first_octet <= 223:
                return "C"
            elif 224 <= first_octet <= 239:
                return "D (Multicast)"
            elif 240 <= first_octet <= 255:
                return "E (Reserved)"
            else:
                return "Unknown"
        else:
            # IPv6 classification based on prefix
            network_str = str(self.network.network_address)
            
            if network_str == "::1":
                return "Loopback"
            elif network_str.startswith("::"):
                return "Unspecified/IPv4-mapped"
            elif network_str.startswith("fe80:"):
                return "Link-local"
            elif network_str.startswith("fc") or network_str.startswith("fd"):
                return "Unique Local (Private)"
            elif network_str.startswith("ff"):
                return "Multicast"
            elif network_str.startswith("2001:db8:"):
                return "Documentation"
            elif network_str.startswith("2001:"):
                return "Global Unicast"
            elif network_str.startswith("2002:"):
                return "6to4"
            elif network_str.startswith("3ffe:"):
                return "6bone (Historic)"
            else:
                return "Global Unicast"
    
    def get_host_list(self, limit: Optional[int] = None) -> pd.DataFrame:
        # Get list of host addresses
        if not self.network:
            raise ValueError("No network loaded")
        
        if limit is None:
            limit = self.max_hosts
        
        hosts = list(self.network.hosts())
        total_hosts = len(hosts)
        
        if total_hosts == 0:
            return pd.DataFrame({"Message": ["No usable hosts in this network"]})
        
        # Limit hosts if there are too many
        hosts_to_show = hosts[:limit]
        
        # Different formatting for IPv4 vs IPv6
        is_ipv4 = isinstance(self.network, ipaddress.IPv4Network)
        
        if is_ipv4:
            # 32-bit binary for IPv4
            binary_format = lambda host: format(int(host), '032b')
            binary_display = lambda binary: f"{binary[:8]}.{binary[8:16]}.{binary[16:24]}.{binary[24:32]}"
        else:
            # 128-bit binary for IPv6 (show in groups for readability)
            binary_format = lambda host: format(int(host), '0128b')
            binary_display = lambda binary: ':'.join([binary[i:i+16] for i in range(0, 128, 16)])
        
        host_data = {
            "Host IP": [str(host) for host in hosts_to_show],
            "Hex": [hex(int(host)) for host in hosts_to_show],
            "Binary": [binary_display(binary_format(host)) for host in hosts_to_show]
        }
        
        df = pd.DataFrame(host_data)
        df.index = range(1, len(df) + 1)  # Start numbering from 1
        
        if total_hosts > limit:
            print(f"Showing first {limit} of {total_hosts} hosts")
            print(f"Use get_host_list(limit=N) to show more hosts")
        
        return df
    
    def get_subnets(self, new_prefix: int) -> pd.DataFrame:
        # Calculate subnet information when dividing the network
        if not self.network:
            raise ValueError("No network loaded")
        
        if new_prefix <= self.network.prefixlen:
            raise ValueError(f"New prefix ({new_prefix}) must be larger than current prefix ({self.network.prefixlen})")
        
        try:
            subnets = list(self.network.subnets(new_prefix=new_prefix))
            
            subnet_data = {
                "Subnet": [str(subnet) for subnet in subnets],
                "Usable Hosts": [subnet.num_addresses - 2 if subnet.num_addresses > 2 else 0 for subnet in subnets],
                "Network Address": [str(subnet.network_address) for subnet in subnets],
                "First Host": [str(next(subnet.hosts())) if list(subnet.hosts()) else "N/A" for subnet in subnets],
                "Last Host": [str(list(subnet.hosts())[-1]) if list(subnet.hosts()) else "N/A" for subnet in subnets],
                "Broadcast Address": [str(subnet.broadcast_address) for subnet in subnets],
                "Subnet Mask": [str(subnet.netmask) for subnet in subnets],
                "Subnet Mask (Decimal)": [int(subnet.netmask) for subnet in subnets],
            }
            
            df = pd.DataFrame(subnet_data)
            df.index = range(1, len(df) + 1)
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error calculating subnets: {e}")
    
    def print_summary(self) -> None:
        # Print a formatted summary of the network
        info = self.get_network_info()
        
        print("\n" + "="*50)
        print("NETWORK SUMMARY")
        print("="*50)
        
        for key, value in info.items():
            print(f"{key:<20}: {value}")
        
        print("="*50)