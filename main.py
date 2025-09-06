import pyfiglet
from network_calculator import NetworkCalculator
from menu_interface import MenuInterface

def print_banner():
    banner = pyfiglet.figlet_format("Maskerade")
    print(banner)
    print('A network analyzer tool for IPv4 and IPv6\n')

def main():
    print_banner()
    
    try:
        calculator = NetworkCalculator()

        calculator.get_network_input()

        calculator.print_summary()
        
        menu = MenuInterface(calculator)
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()