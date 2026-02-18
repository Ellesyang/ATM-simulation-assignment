from collections import defaultdict

filename = "TrafficSWjsf.scn"
output_file = "NL_traffic_analysis.txt"

# Store flight info per callsign
flights = {}

with open(filename, "r") as f:
    for line in f:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue
        
        if ">" not in line:
            continue

        
        time_part, content = line.split(">", 1)
        parts = content.split()
        
        if parts[0] == "CRE":
            callsign = parts[1]
            flights[callsign] = {
                "time": time_part,
                "origin": None,
                "destination": None
            }
        
        elif len(parts) >= 3 and parts[1] == "ORIG":
            callsign = parts[0]
            if callsign in flights:
                flights[callsign]["origin"] = parts[2]
        
        elif len(parts) >= 3 and parts[1] == "DEST":
            callsign = parts[0]
            if callsign in flights:
                flights[callsign]["destination"] = parts[2]


# ===============================
# Organize per Dutch airport (EH*)
# ===============================

airports = defaultdict(lambda: {"departures": [], "arrivals": []})

for callsign, data in flights.items():
    origin = data["origin"]
    destination = data["destination"]
    time = data["time"]
    
    if origin and origin.startswith("EH"):
        airports[origin]["departures"].append(
            (callsign, time, origin, destination)
        )
    
    if destination and destination.startswith("EH"):
        airports[destination]["arrivals"].append(
            (callsign, time, origin, destination)
        )

# Totals NL
total_departures_nl = sum(len(a["departures"]) for a in airports.values())
total_arrivals_nl = sum(len(a["arrivals"]) for a in airports.values())


# ===============================
# Write report
# ===============================

with open(output_file, "w") as f:
    
    # Total NL
    f.write("===== TOTAL NETHERLANDS =====\n")
    f.write(f"Total departures NL: {total_departures_nl}\n")
    f.write(f"Total arrivals NL:   {total_arrivals_nl}\n\n")
    
    #  Totals per airport
    f.write("===== TOTAL PER AIRPORT =====\n")
    for airport in sorted(airports.keys()):
        dep = len(airports[airport]["departures"])
        arr = len(airports[airport]["arrivals"])
        f.write(f"{airport}: Departures = {dep}, Arrivals = {arr}\n")
    
    f.write("\n\n===== DETAILED PER AIRPORT =====\n")
    
    #  Detailed section
    for airport in sorted(airports.keys()):
        f.write(f"\n\n=== {airport} ===\n")
        
        dep = airports[airport]["departures"]
        arr = airports[airport]["arrivals"]
        
        f.write(f"Departures ({len(dep)}):\n")
        for flight in dep:
            callsign, time, origin, destination = flight
            f.write(f"{time} | {callsign} | {origin} -> {destination}\n")
        
        f.write(f"\nArrivals ({len(arr)}):\n")
        for flight in arr:
            callsign, time, origin, destination = flight
            f.write(f"{time} | {callsign} | {origin} -> {destination}\n")

print(f"Analysis exported to: {output_file}")
