import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import seaborn as sns
import numpy as np

# df = pd.read_csv('graph/ble.csv')


# snow_depth = df['snow_depth'].values
# success_rate = df['success_rate'].values
# distance = df['distance'].values

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Scatter plot
# ax.scatter(snow_depth, distance, success_rate, c='r', marker='o')

# # Labels
# ax.set_xlabel('Snow Depth')
# ax.set_ylabel('Distance')
# ax.set_zlabel('Success Rate')

# plt.show()


def rssiVsConditions(filename):

    df = pd.read_csv(filename)

    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")

    # Step 2: Differentiate data into two categories
    snow_depth_zero = df[df['snow_depth'] == 0]
    snow_depth_positive = df[df['snow_depth'] > 0]

    print(len(snow_depth_zero))
    print(len(snow_depth_positive))

    # Step 3: Create box plots
    plt.figure(figsize=(12, 6))
    plt.suptitle('RSSI vs Conditions - ' + radio_tech, fontsize=16)

    plt.subplot(1, 2, 1)
    sns.boxplot(data=snow_depth_zero, y='RSSI', color='skyblue')
    plt.title('Snow Depth = 0')

    plt.subplot(1, 2, 2)
    sns.boxplot(data=snow_depth_positive, y='RSSI', color='lightgreen')
    plt.title('Snow Depth > 0')

    plt.tight_layout()
    plt.show()


def countGraph(filename):
    df = pd.read_csv(filename)
    snow_depth_zero = df[df['snow_depth'] == 0]
    
    snow_depth_positive = df[df['snow_depth'] > 0]

    
    # Step 2: Create a histogram of RSSI values
    plt.figure(figsize=(8, 6))
    plt.hist(snow_depth_positive['RSSI'], bins=20, color='skyblue', edgecolor='black')
    plt.title('RSSI count in Unclear conditions - WiFi')
    plt.xlabel('RSSI')
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()


def successRateVsConditions(filename):

    df = pd.read_csv(filename)

    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")

    # Step 2: Differentiate data into two categories
    snow_depth_zero = df[df['snow_depth'] == 0]
    snow_depth_positive = df[df['snow_depth'] > 0]

    print(len(snow_depth_zero))
    print(len(snow_depth_positive))

    # Step 3: Create box plots
    plt.figure(figsize=(12, 6))
    plt.suptitle('Success Rate vs Conditions - ' + radio_tech, fontsize=16)

    plt.subplot(1, 2, 1)
    sns.boxplot(data=snow_depth_zero, y='success_rate', color='skyblue')
    plt.title('Snow Depth = 0')

    plt.subplot(1, 2, 2)
    sns.boxplot(data=snow_depth_positive, y='success_rate', color='lightgreen')
    plt.title('Snow Depth > 0')

    plt.tight_layout()
    plt.show()


def xyz_graph(filename):   

    df = pd.read_csv(filename)
    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")

    snow_depth = df['snow_depth'].values
    success_rate = df['success_rate'].values
    distance = df['distance'].values

    fig = plt.figure()
    plt.suptitle('Sucess Rate vs Snow Depth & Distance - ' + radio_tech, fontsize=16)
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(snow_depth, distance, success_rate, c='b', marker='o')

    # Labels
    ax.set_xlabel('Snow Depth')
    ax.set_ylabel('Distance')
    ax.set_zlabel('Success Rate')

    plt.show()

def xyz_hue_graph(filename):
    # Step 1: Read the CSV file
    df = pd.read_csv(filename)
    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")
    # Step 2: Create a scatter plot with success rate as a color map

    plt.figure(figsize=(10, 8))

    # Create the main scatter plot
    scatter = plt.scatter(df['snow_depth'], df['distance'], c=df['success_rate'], cmap='RdYlGn', edgecolor='none', s=200)

    # Create a separate scatter plot with invisible markers for color mapping
    plt.scatter([], [], c=[], cmap='RdYlGn', edgecolor='none', s=200, label='Success Rate')

    # Add colorbar
    plt.colorbar(scatter, label='Success Rate')

    plt.title('Success Rate vs Snow Depth and Distance - ' + radio_tech)
    plt.xlabel('Snow Depth')
    plt.ylabel('Distance')
    plt.grid(True)
    plt.legend()
    plt.show()


def xyz_heatmap(filename):

    # Step 1: Read the CSV file
    df = pd.read_csv(filename)

    # Step 2: Define the range of snow depth and distance
    snow_depth_range = np.linspace(df['snow_depth'].min(), df['snow_depth'].max(), 100)
    distance_range = np.linspace(df['distance'].min(), df['distance'].max(), 100)

    # Step 3: Create a meshgrid
    snow_depth_mesh, distance_mesh = np.meshgrid(snow_depth_range, distance_range)

    # Step 4: Interpolate success rate values on the meshgrid
    success_rate_values = np.zeros_like(snow_depth_mesh)
    for i in range(len(snow_depth_range)):
        for j in range(len(distance_range)):
            snow_depth_val = snow_depth_range[i]
            distance_val = distance_range[j]
            success_rate_val = df[(df['snow_depth'] == snow_depth_val) & (df['distance'] == distance_val)]['success_rate'].mean()
            success_rate_values[j, i] = success_rate_val

    # Step 5: Plot the heatmap
    plt.figure(figsize=(10, 6))
    plt.imshow(success_rate_values, extent=[snow_depth_range.min(), snow_depth_range.max(), distance_range.min(), distance_range.max()], origin='lower', cmap='RdYlGn', aspect='auto')
    plt.colorbar(label='Success Rate')
    plt.xlabel('Snow Depth')
    plt.ylabel('Distance')
    plt.title('Success Rate Heatmap')
    plt.show()


def linegraph_temperature(filename):
    # Step 1: Read the CSV file
    df = pd.read_csv(filename)
    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")

    # Step 2: Calculate average RSSI for each temperature
    average_rssi = df.groupby('temperature')['RSSI'].mean().reset_index()

    # Step 3: Create the line graph
    plt.figure(figsize=(10, 6))

    # Plot Average RSSI vs Temperature
    plt.plot(average_rssi['temperature'], average_rssi['RSSI'], marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.title('Average RSSI vs Temperature - ' + radio_tech)
    plt.xlabel('Temperature')
    plt.ylabel('Average RSSI')
    plt.grid(True)
    for i, txt in enumerate(average_rssi['RSSI']):
        plt.text(average_rssi['temperature'][i], average_rssi['RSSI'][i], f"{txt:.2f}", ha='right', va='bottom')
    plt.show()  

def linegraph_wind(filename):
    # Step 1: Read the CSV file
    df = pd.read_csv(filename)
    radio_tech = input("ENTER THE NAME OF RADIO TECHNOLOGY: ")

    # Step 2: Calculate average RSSI for each temperature
    average_rssi = df.groupby('wind')['RSSI'].mean().reset_index()

    # Step 3: Create the line graph
    plt.figure(figsize=(10, 6))

    # Plot Average RSSI vs Temperature
    plt.plot(average_rssi['wind'], average_rssi['RSSI'], marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.title('Average RSSI vs Wind - ' + radio_tech)
    plt.xlabel('Wind speed')
    plt.ylabel('Average RSSI')
    plt.grid(True)
    for i, txt in enumerate(average_rssi['RSSI']):
        plt.text(average_rssi['wind'][i], average_rssi['RSSI'][i], f"{txt:.2f}", ha='right', va='bottom')
    plt.show()  

filename = 'graph/datasets/LoRa.csv'

#countGraph(filename)
#successRateVsConditions(filename)
#xyz_hue_graph(filename)
#linegraph_temperature(filename)
linegraph_wind(filename)
#xyz_heatmap(filename)