import sys
from rich.console import Console
from rich.table import Table

console = Console()


def error(message):
    """Print a red error message and stop the program."""
    console.print(f"[bold red]Error:[/bold red] {message}")
    sys.exit(1)


# ── Banner ──────────────────────────────────────────────
console.print("[bold cyan]Subnet Calculator[/bold cyan]")

# ── Input + validation ──────────────────────────────────
entry = input("Enter IP/prefix (ex: 192.168.1.0/24) >> ").strip()

if "/" not in entry:
    error("Include a prefix, like 192.168.1.0/24")

ip_address, prefix_text = entry.split("/", 1)

if not prefix_text.isdigit() or int(prefix_text) > 32:
    error("Prefix must be a number from 0 to 32")

ip_addr = ip_address.split(".")
if len(ip_addr) != 4:
    error("IP address must have 4 octets, like 192.168.1.0")

for octet in ip_addr:
    if not octet.isdigit() or int(octet) > 255:
        error("Each octet must be a number from 0 to 255")

# ── Bits and address counts ─────────────────────────────
cidr = int(prefix_text)
network_bits = cidr
host_bits = 32 - cidr
total_addresses = 2 ** host_bits

# ── Subnet mask: build the bits, split into octets, convert ──
binary_calc = ("1" * cidr) + ("0" * host_bits)
mask_bin_1 = binary_calc[0:8]
mask_bin_2 = binary_calc[8:16]
mask_bin_3 = binary_calc[16:24]
mask_bin_4 = binary_calc[24:32]

mask_1 = int(mask_bin_1, 2)
mask_2 = int(mask_bin_2, 2)
mask_3 = int(mask_bin_3, 2)
mask_4 = int(mask_bin_4, 2)

# ── IP octets ───────────────────────────────────────────
ip_oct_1 = int(ip_addr[0])
ip_oct_2 = int(ip_addr[1])
ip_oct_3 = int(ip_addr[2])
ip_oct_4 = int(ip_addr[3])

# ── Network address: IP AND mask ("which chunk am I in") ──
net_1 = ip_oct_1 & mask_1
net_2 = ip_oct_2 & mask_2
net_3 = ip_oct_3 & mask_3
net_4 = ip_oct_4 & mask_4

# ── Broadcast: network + (255 - mask) ("end of the chunk") ──
bc_1 = net_1 + (255 - mask_1)
bc_2 = net_2 + (255 - mask_2)
bc_3 = net_3 + (255 - mask_3)
bc_4 = net_4 + (255 - mask_4)

network_address = f"{net_1}.{net_2}.{net_3}.{net_4}"
broadcast_address = f"{bc_1}.{bc_2}.{bc_3}.{bc_4}"

# ── Usable hosts (special cases: /31 and /32) ───────────
if cidr == 32:
    # A single host, like a loopback or host route
    usable_addresses = 1
    first_usable = network_address
    last_usable = network_address
elif cidr == 31:
    # Point-to-point link: both addresses are usable (RFC 3021)
    usable_addresses = 2
    first_usable = network_address
    last_usable = broadcast_address
else:
    usable_addresses = total_addresses - 2
    first_usable = f"{net_1}.{net_2}.{net_3}.{net_4 + 1}"
    last_usable = f"{bc_1}.{bc_2}.{bc_3}.{bc_4 - 1}"

# ── Results table ───────────────────────────────────────
table = Table(title="Subnet Calculation Results", header_style="bold magenta")
table.add_column("Field", style="cyan")
table.add_column("Value", style="white")

table.add_row("IP Address", f"{ip_oct_1}.{ip_oct_2}.{ip_oct_3}.{ip_oct_4}")
table.add_row("Subnet Mask", f"{mask_1}.{mask_2}.{mask_3}.{mask_4}")
table.add_row("Binary Mask", f"{mask_bin_1}.{mask_bin_2}.{mask_bin_3}.{mask_bin_4}")
table.add_row("Network Address", f"[green]{network_address}[/green]")
table.add_row("Broadcast Address", f"[red]{broadcast_address}[/red]")
table.add_row("Usable Range", f"[yellow]{first_usable} - {last_usable}[/yellow]")
table.add_row("Network Bits", str(network_bits))
table.add_row("Host Bits", str(host_bits))
table.add_row("Total Addresses", str(total_addresses))
table.add_row("Usable Addresses", str(usable_addresses))

console.print(table)


