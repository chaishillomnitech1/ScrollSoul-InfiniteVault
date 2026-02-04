"""
Multi-Layer Scaling Framework
Implements dimensional expansion and scalability across the ScrollVerse
"""

from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScalingLayer:
    """Represents a single scaling layer in the multi-dimensional framework"""
    
    def __init__(self, layer_id: int, name: str, capacity: int = 1000):
        self.layer_id = layer_id
        self.name = name
        self.capacity = capacity
        self.current_load = 0
        self.active = True
        
    def add_load(self, amount: int) -> bool:
        """Add load to this layer"""
        if self.current_load + amount <= self.capacity:
            self.current_load += amount
            return True
        return False
    
    def get_utilization(self) -> float:
        """Get current utilization percentage"""
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0
    
    def __repr__(self):
        return f"Layer({self.layer_id}: {self.name}, {self.get_utilization():.1f}% utilized)"


class MultiLayerScaler:
    """
    Multi-Layer Scaling Framework
    
    Manages dimensional expansion and load distribution across infinite layers
    """
    
    def __init__(self, initial_layers: int = 3):
        self.layers: List[ScalingLayer] = []
        self.metrics: Dict[str, Any] = {
            "total_requests": 0,
            "layers_created": 0,
            "scaling_events": 0
        }
        
        # Initialize base layers
        for i in range(initial_layers):
            self._add_layer(f"Dimension-{i+1}")
    
    def _add_layer(self, name: str) -> ScalingLayer:
        """Add a new scaling layer"""
        layer_id = len(self.layers)
        layer = ScalingLayer(layer_id, name)
        self.layers.append(layer)
        self.metrics["layers_created"] += 1
        logger.info(f"Created new scaling layer: {name}")
        return layer
    
    def distribute_load(self, load: int) -> Dict[str, Any]:
        """
        Distribute load across available layers
        Implements karmic balance algorithm
        """
        self.metrics["total_requests"] += 1
        
        # Find layer with lowest utilization
        best_layer = min(self.layers, key=lambda l: l.get_utilization())
        
        if best_layer.add_load(load):
            return {
                "success": True,
                "layer": best_layer.layer_id,
                "utilization": best_layer.get_utilization()
            }
        
        # If no layer can handle, create new dimension
        new_layer = self._add_layer(f"Dimension-{len(self.layers)+1}")
        self.metrics["scaling_events"] += 1
        
        if new_layer.add_load(load):
            return {
                "success": True,
                "layer": new_layer.layer_id,
                "utilization": new_layer.get_utilization(),
                "new_dimension": True
            }
        
        return {"success": False, "reason": "Load exceeds single layer capacity"}
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall scaling framework status"""
        return {
            "total_layers": len(self.layers),
            "active_layers": sum(1 for l in self.layers if l.active),
            "average_utilization": sum(l.get_utilization() for l in self.layers) / len(self.layers) if self.layers else 0,
            "metrics": self.metrics,
            "layers": [
                {
                    "id": l.layer_id,
                    "name": l.name,
                    "utilization": l.get_utilization(),
                    "load": l.current_load,
                    "capacity": l.capacity
                }
                for l in self.layers
            ]
        }
    
    def optimize(self) -> Dict[str, Any]:
        """
        Optimize layer distribution for karmic alignment
        Balances load across dimensions
        """
        if not self.layers:
            return {"optimized": False, "reason": "No layers available"}
        
        total_load = sum(l.current_load for l in self.layers)
        target_per_layer = total_load / len(self.layers)
        
        optimizations = 0
        for layer in self.layers:
            if abs(layer.current_load - target_per_layer) > 100:
                layer.current_load = int(target_per_layer)
                optimizations += 1
        
        return {
            "optimized": True,
            "adjustments": optimizations,
            "average_utilization": sum(l.get_utilization() for l in self.layers) / len(self.layers)
        }
