"""
Example: Multi-Layer Scaling Framework Usage
Demonstrates dimensional expansion and load distribution
"""

from scrollsoul import MultiLayerScaler


def main():
    print("=== ScrollSoul Multi-Layer Scaling Framework ===\n")
    
    # Initialize scaler with 3 dimensions
    scaler = MultiLayerScaler(initial_layers=3)
    print("Initialized with 3 base dimensions")
    
    # Distribute various loads
    print("\n--- Distributing Loads Across Dimensions ---")
    for i in range(5):
        load = 100 * (i + 1)
        result = scaler.distribute_load(load)
        print(f"Load {load}: {result}")
    
    # Get current status
    print("\n--- Current Scaling Status ---")
    status = scaler.get_status()
    print(f"Total Layers: {status['total_layers']}")
    print(f"Average Utilization: {status['average_utilization']:.2f}%")
    print(f"Total Requests: {status['metrics']['total_requests']}")
    
    # Display layer details
    print("\n--- Layer Details ---")
    for layer in status['layers']:
        print(f"  {layer['name']}: {layer['utilization']:.1f}% ({layer['load']}/{layer['capacity']})")
    
    # Optimize karmic distribution
    print("\n--- Optimizing Karmic Distribution ---")
    optimization = scaler.optimize()
    print(f"Optimized: {optimization['optimized']}")
    print(f"Adjustments Made: {optimization['adjustments']}")
    print(f"New Average Utilization: {optimization['average_utilization']:.2f}%")
    
    print("\n✨ The ScrollVerse expands across infinite dimensions! ✨")


if __name__ == "__main__":
    main()
