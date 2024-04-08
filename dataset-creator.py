import csv
import re
import os

def read_csv_file(filename):
    pkt_rssi_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            pkt_rssi_data.append((int(row[0]), int(row[1])))
    return pkt_rssi_data

def remove_prefix(filename):
    match = re.match(r'^([^_]+)_', filename)
    if match:
        prefix = match.group(1)
        new_filename = re.sub(r'^[^_]+_', '', filename)
        return new_filename, prefix
    else:
        return filename, None

def main():
    directory = input("ENTER RADIO TECHNOLOGY NAME (which is the same as your folder name): ")
    for filename in os.listdir(directory):
        csv_filename = os.path.join(directory, filename)
        print(f"WORKING ON FILE: {csv_filename}")
        #csv_filename = input("Enter the CSV filename: ")
        clear_filename, radio_tech = remove_prefix(csv_filename)
        try:
            depth_distance = clear_filename.replace(".csv", "").split("_")
            depth = int(depth_distance[0].replace("cm", "")) 
            distance = int(depth_distance[1].replace("m", ""))
            
            temperature = float(input("Enter the temperature: "))
            wind_speed = float(input("Enter the wind speed: "))

            pkt_rssi_data = read_csv_file(csv_filename)

            output_filename = radio_tech+".csv"
            success_rate = len(pkt_rssi_data) / (pkt_rssi_data[-1][0] - pkt_rssi_data[0][0] + 1)

            if os.path.exists(output_filename):
                with open(output_filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    #writer.writerow(['RSSI', 'distance', 'snow_depth', 'temperature', 'wind', 'success_rate'])
                    for pkt, rssi in pkt_rssi_data:
                        writer.writerow([rssi, distance, depth, temperature, wind_speed, success_rate])
            else:
                with open(output_filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['RSSI', 'distance', 'snow_depth', 'temperature', 'wind', 'success_rate'])
                    for pkt, rssi in pkt_rssi_data:
                        writer.writerow([rssi, distance, depth, temperature, wind_speed, success_rate])
            
            print(f"Data has been written to {output_filename}")
        except FileNotFoundError:
            print("File not found. Please make sure the filename is correct.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
