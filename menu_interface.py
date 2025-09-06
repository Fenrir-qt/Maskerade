from network_calculator import NetworkCalculator
from file_exporter import FileExporter

class MenuInterface:
    # Interactive menu for the network calculator
    
    def __init__(self, calculator: NetworkCalculator):
        self.calculator = calculator
        self.exporter = FileExporter(calculator)
    
    def run(self) -> None:
        # Main menu loop
        while True:
            self._display_menu()
            
            try:
                choice = input("Select an option (1-8): ").strip()
                
                if choice == '1':
                    self.calculator.print_summary()
                
                elif choice == '2':
                    self._show_host_list()
                
                elif choice == '3':
                    self._calculate_subnets()
                
                elif choice == '4':
                    self._export_network_info()
                
                elif choice == '5':
                    self._export_host_list()
                
                elif choice == '6':
                    self._export_subnets()
                
                elif choice == '7':
                    self.calculator.get_network_input()
                
                elif choice == '8':
                    print("Thank you for using Maskerade!")
                    break
                
                else:
                    print("Invalid option. Please select 1-8.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def _display_menu(self):
        # Display the main menu options
        print("\n" + "="*40)
        print("MASKERADE - NETWORK ANALYZER")
        print("="*40)
        print("1. Show network summary")
        print("2. Show host list")
        print("3. Calculate subnets")
        print("4. Export network info")
        print("5. Export host list")
        print("6. Export subnets")
        print("7. Load new network")
        print("8. Exit")
        print("="*40)
    
    def _show_host_list(self):
        # Handle host list display
        try:
            limit = input("Number of hosts to show (press Enter for default 1000): ").strip()
            limit = int(limit) if limit else None
            df = self.calculator.get_host_list(limit)
            print(f"\n{df}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def _calculate_subnets(self):
        # Handle subnet calculation
        try:
            new_prefix = int(input(f"Enter new subnet prefix (current: /{self.calculator.network.prefixlen}): "))
            df = self.calculator.get_subnets(new_prefix)
            print(f"\n{df}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def _export_network_info(self):
        # Handle network info export
        try:
            filename = self.exporter.export_network_info()
            print(f"Network info exported to {filename}")
        except Exception as e:
            print(f"Export failed: {e}")
    
    def _export_host_list(self):
        # Handle host list export
        try:
            limit = input("Number of hosts to export (press Enter for default 1000): ").strip()
            limit = int(limit) if limit else None
            filename = self.exporter.export_host_list(limit=limit)
            print(f"Host list exported to {filename}")
        except Exception as e:
            print(f"Export failed: {e}")
    
    def _export_subnets(self):
        # Handle subnet export
        try:
            new_prefix = int(input(f"Enter subnet prefix for export (current: /{self.calculator.network.prefixlen}): "))
            filename = self.exporter.export_subnets(new_prefix)
            print(f"Subnets exported to {filename}")
        except ValueError as e:
            print(f"Export failed: {e}")