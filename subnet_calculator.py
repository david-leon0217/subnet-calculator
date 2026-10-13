print("Subnet-Calculator Enabled")

user_input = input("TypeEx: 192.168.1.0/24 >> ").split("/")
ip_address = user_input[0]
cidr = int(user_input[1])
host_bits = 32 - cidr
network_bits = cidr
total_addresses = 2 ** host_bits
usable_addresses = total_addresses - 2

binary_calc = ("1" * cidr) + ("0" * host_bits)
mask_bin_1 = binary_calc[0:8]
mask_bin_2 = binary_calc[8:16]
mask_bin_3 = binary_calc[16:24]
mask_bin_4 = binary_calc[24:32]

mask_1 = int(mask_bin_1, 2)
mask_2 = int(mask_bin_2, 2)
mask_3 = int(mask_bin_3, 2)
mask_4 = int(mask_bin_4, 2)

ip_addr = ip_address.split(".")
ip_oct_1 = int(ip_addr[0])
ip_oct_2 = int(ip_addr[1])
ip_oct_3 = int(ip_addr[2])
ip_oct_4 = int(ip_addr[3])

net_1 = ip_oct_1 & mask_1
net_2 = ip_oct_2 & mask_2
net_3 = ip_oct_3 & mask_3
net_4 = ip_oct_4 & mask_4

bc_1 = net_1 + (255 - mask_1)
bc_2 = net_2 + (255 - mask_2)
bc_3 = net_3 + (255 - mask_3)
bc_4 = net_4 + (255 - mask_4)

first_usable = f"{net_1}.{net_2}.{net_3}.{net_4 + 1}"
last_usable = f"{bc_1}.{bc_2}.{bc_3}.{bc_4 - 1}"

print(f"Calculation Complete (Listed Below)")
print(f"IP Address: {ip_oct_1}.{ip_oct_2}.{ip_oct_3}.{ip_oct_4}")
print(f"Subnet Mask: {mask_1}.{mask_2}.{mask_3}.{mask_4}")
print(f"Binary Mask: {mask_bin_1}.{mask_bin_2}.{mask_bin_3}.{mask_bin_4}")
print(f"Network Address: {net_1}.{net_2}.{net_3}.{net_4}")
print(f"Broadcast Address: {bc_1}.{bc_2}.{bc_3}.{bc_4}")
print(f"Network Bits: {network_bits}")
print(f"Host Bits: {host_bits}")
print(f"Total Addresses: {total_addresses}")
print(f"Usable Addresses: {usable_addresses}")
print(f"Usable Range: {first_usable} - {last_usable}")


