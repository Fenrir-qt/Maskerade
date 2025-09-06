import os
import pandas as pd
from typing import Optional
from network_calculator import NetworkCalculator

class FileExporter:
    # Handles all file export operations for network data
    
    def __init__(self, calculator: NetworkCalculator):
        self.calculator = calculator
    
    def export_network_info(self, filename_prefix: str = "network_info") -> str:
        # Export network information to CSV file
        info = self.calculator.get_network_info()
        
        # Convert to table format for export
        df = pd.DataFrame([info])
        
        filename = self._get_unique_filename(filename_prefix, "csv")
        df.to_csv(filename, index=False)
        
        return filename
    
    def export_host_list(self, filename_prefix: str = "host_list", limit: Optional[int] = None) -> str:
        # Export host list to CSV file
        df = self.calculator.get_host_list(limit)
        
        filename = self._get_unique_filename(filename_prefix, "csv")
        df.to_csv(filename, index=True)
        
        return filename
    
    def export_subnets(self, new_prefix: int, filename_prefix: str = "subnets") -> str:
        # Export subnet information to CSV file
        df = self.calculator.get_subnets(new_prefix)
        
        filename = self._get_unique_filename(filename_prefix, "csv")
        df.to_csv(filename, index=True)
        
        return filename
    
    def _get_unique_filename(self, prefix: str, extension: str) -> str:
        # Generate a unique filename by adding a number if file already exists
        i = 1
        filename = f"{prefix}_{i}.{extension}"
        
        while os.path.exists(filename):
            i += 1
            filename = f"{prefix}_{i}.{extension}"
        
        return filename