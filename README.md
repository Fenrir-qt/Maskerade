# Maskerade - Network Analyzer Tool

A comprehensive network analysis tool that supports both IPv4 and IPv6 networks. Calculate network information, generate host lists, perform subnet calculations, and export results to CSV files.

## Features

- **Dual Stack Support**: Works with both IPv4 and IPv6 networks
- **Network Analysis**: Complete network information including class/type, broadcast addresses, and host ranges
- **Host Enumeration**: Generate lists of all usable hosts with hex and binary representations
- **Subnet Calculator**: Divide networks into smaller subnets
- **Data Export**: Export network info, host lists, and subnet data to CSV files
- **Interactive Interface**: User-friendly menu-driven interface
- **ASCII Art Banner**: Stylish application branding

## Supported Network Types

### IPv4
- All standard IPv4 networks (e.g., `192.168.1.0/24`)
- Network classes A, B, C, D (Multicast), E (Reserved)
- Private and public network detection

### IPv6
- Global Unicast addresses (e.g., `2001:db8::/32`)
- Link-local addresses (`fe80::/64`)
- Unique Local addresses (`fc00::/7`, `fd00::/7`)
- Documentation addresses (`2001:db8::/32`)
- Multicast addresses (`ff00::/8`)
- And more IPv6 address types

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**
   ```bash
   git clone https://github.com/Fenrir-qt/Maskerade.git
   cd Maskerade
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   **On Windows:**
   ```bash
   .venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

### Required Dependencies

Create a `requirements.txt` file with:
```
pandas
pyfiglet
ipaddress
```

## Usage

### Running the Application

```bash
python main.py
```

### Interactive Menu Options

1. **Show network summary** - Display complete network information
2. **Show host list** - List all usable host addresses (configurable limit)
3. **Calculate subnets** - Divide network into smaller subnets
4. **Export network info** - Save network summary to CSV
5. **Export host list** - Save host addresses to CSV
6. **Export subnets** - Save subnet information to CSV
7. **Load new network** - Enter a different network address
8. **Exit** - Close the application

### Example Usage

```
Enter network (e.g. 192.168.1.0/24 or 2001:db8::/32): 192.168.1.0/24
IPv4 Network '192.168.1.0/24' loaded successfully

==================================================
NETWORK SUMMARY
==================================================
IP Version          : IPv4
Network Address     : 192.168.1.0
Network CIDR        : 192.168.1.0/24
Subnet Mask         : 255.255.255.0
Wildcard Mask       : 0.0.0.255
Broadcast Address   : 192.168.1.255
Network Class       : C
Is Private          : True
Total Addresses     : 256
Usable Hosts        : 254
First Host          : 192.168.1.1
Last Host           : 192.168.1.254
==================================================
```

## File Structure

```
maskerade/
├── .venv/                # Virtual environment (auto-generated)
├── main.py               # Application entry point
├── network_calculator.py # Core network calculation logic
├── file_exporter.py      # CSV export functionality
├── menu_interface.py     # Interactive user interface
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Module Overview

### `network_calculator.py`
- **NetworkCalculator class**: Core functionality for network analysis
- IPv4/IPv6 network parsing and validation
- Host enumeration with binary/hex conversion
- Subnet calculation algorithms
- Network classification (IPv4 classes, IPv6 types)

### `file_exporter.py`
- **FileExporter class**: Handles all data export operations
- CSV file generation with unique naming
- Network info, host list, and subnet data export
- Automatic file numbering to prevent overwrites

### `menu_interface.py`
- **MenuInterface class**: Interactive command-line interface
- Menu display and user input handling
- Integration between calculator and exporter modules
- Error handling and user feedback

### `main.py`
- Application initialization and startup
- Banner display using ASCII art
- Main execution flow and error handling

## Examples

### IPv4 Network Analysis
```
Input: 10.0.0.0/16
Output: 65,534 usable hosts across 10.0.0.1 - 10.0.255.254
```

### IPv6 Network Analysis
```
Input: 2001:db8::/64
Output: 18,446,744,073,709,551,614 usable hosts
Type: Documentation (IPv6)
```

### Subnet Calculation
```
Input: 192.168.1.0/24 divided into /26 subnets
Output: 4 subnets with 62 hosts each
- 192.168.1.0/26 (192.168.1.1 - 192.168.1.62)
- 192.168.1.64/26 (192.168.1.65 - 192.168.1.126)
- 192.168.1.128/26 (192.168.1.129 - 192.168.1.190)
- 192.168.1.192/26 (192.168.1.193 - 192.168.1.254)
```

## Export Files

All exported files are automatically numbered to prevent overwrites:
- `network_info_1.csv` - Network summary information
- `host_list_1.csv` - Complete host enumeration
- `subnets_1.csv` - Subnet calculation results

## Error Handling

The application includes comprehensive error handling for:
- Invalid network formats
- Unsupported CIDR notations
- File system errors during export
- User input validation
- IPv4/IPv6 compatibility issues

## Development

### Virtual Environment Management

**Activate environment:**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**Deactivate environment:**
```bash
deactivate
```

**Update dependencies:**
```bash
pip freeze > requirements.txt
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r requirements.txt`

2. **"Invalid network format" errors**
   - Include CIDR notation (e.g., `/24`, `/64`)
   - Use proper IPv4/IPv6 formatting

3. **Large network performance**
   - Use host limits for networks with many addresses
   - Consider exporting in smaller batches

### Getting Help

If you encounter issues:
1. Check that your network format is correct
2. Ensure all dependencies are installed
3. Verify Python version compatibility (3.7+)
4. Check file permissions for export operations