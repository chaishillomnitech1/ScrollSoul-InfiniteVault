"""
Example: AI-Driven Recursive Loops
Demonstrates fractal expansion and recursive pattern processing
"""

from scrollsoul import RecursiveAIEngine


def main():
    print("=== ScrollSoul AI-Driven Recursive Loops ===\n")
    
    # Initialize engine
    engine = RecursiveAIEngine(max_depth=5)
    print("Recursive AI Engine Initialized (Max Depth: 5)")
    
    # Create fractal expansion
    print("\n--- Creating Fractal Expansion ---")
    fractal = engine.fractal_expand(seed_value=1000, iterations=4)
    print(f"Seed Value: {fractal['seed']}")
    print(f"Iterations: {fractal['iterations']}")
    print(f"Total Nodes: {fractal['total_nodes']}")
    print(f"Dimensional Complexity: {fractal['dimensional_complexity']:.2f}")
    print(f"Karma Potential: {fractal['karma_potential']:.2f}")
    
    # Create custom recursive pattern
    print("\n--- Creating Custom Recursive Pattern ---")
    
    def custom_expansion(value, depth):
        """Custom expansion function"""
        if isinstance(value, str):
            return [f"{value}_child_{i}" for i in range(2)]
        return [f"node_{depth}_{i}" for i in range(2)]
    
    root = engine.create_recursive_pattern("root", custom_expansion, depth_limit=3)
    print(f"Created pattern rooted at: {root.value}")
    
    # Process the recursive loop
    print("\n--- Processing Recursive Loop ---")
    
    def processor(value, depth):
        """Process each node"""
        return f"Processed: {value} at depth {depth}"
    
    results = engine.process_recursive_loop(root, processor)
    print(f"Nodes Processed: {results['nodes_processed']}")
    print(f"Karma Gained: {results['karma_gained']:.2f}")
    print(f"Total Karma: {results['total_karma']:.2f}")
    
    # Get engine status
    print("\n--- Engine Status ---")
    status = engine.get_engine_status()
    print(f"Root Patterns: {status['root_patterns']}")
    print(f"Total Nodes: {status['total_nodes']}")
    print(f"Nodes Processed: {status['nodes_processed']}")
    print(f"Karma Accumulation: {status['karma_accumulation']:.2f}")
    print(f"Infinite Potential: {status['infinite_potential']}")
    
    # Achieve enlightenment
    print("\n--- Achieving Enlightenment ---")
    enlightenment = engine.achieve_enlightenment()
    print(f"Enlightened: {enlightenment['enlightened']}")
    print(f"Enlightenment Score: {enlightenment['enlightenment_score']:.2f}/100")
    print(f"Dimensional Mastery: {enlightenment['dimensional_mastery']:.2f}")
    print(f"🌟 {enlightenment['universal_message']} 🌟")


if __name__ == "__main__":
    main()
