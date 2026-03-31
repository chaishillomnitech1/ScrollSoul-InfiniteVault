/**
 * multi_layer_scaling_script.js
 * ScrollSoul-InfiniteVault — Multi-Layer Scaling Framework (JavaScript)
 *
 * ALLĀHU AKBAR! Dimensional expansion across infinite layers,
 * with full GoHighLevel sub-account metric reporting built-in.
 *
 * Usage:
 *   const { MultiLayerScaler } = require('./multi_layer_scaling_script');
 *   const scaler = new MultiLayerScaler({ initialLayers: 3 });
 *   const result = scaler.distributeLoad(500);
 */

'use strict';

// Minimum load delta (units) before a layer is considered imbalanced during optimization
const LOAD_ADJUSTMENT_THRESHOLD = 100;

// ── ScalingLayer ──────────────────────────────────────────────────────────────

class ScalingLayer {
  /**
   * @param {number} layerId
   * @param {string} name
   * @param {number} [capacity=1000]
   */
  constructor(layerId, name, capacity = 1000) {
    this.layerId = layerId;
    this.name = name;
    this.capacity = capacity;
    this.currentLoad = 0;
    this.active = true;
    this.createdAt = new Date().toISOString();
    this.karmaScore = 100.0;
  }

  /** Add load; returns true if accepted, false if over capacity. */
  addLoad(amount) {
    if (this.currentLoad + amount <= this.capacity) {
      this.currentLoad += amount;
      return true;
    }
    return false;
  }

  /** Utilization as a percentage (0–100). */
  getUtilization() {
    return this.capacity > 0 ? (this.currentLoad / this.capacity) * 100 : 0;
  }

  toJSON() {
    return {
      layerId: this.layerId,
      name: this.name,
      capacity: this.capacity,
      currentLoad: this.currentLoad,
      utilization: parseFloat(this.getUtilization().toFixed(2)),
      active: this.active,
      karmaScore: this.karmaScore,
    };
  }

  toString() {
    return `Layer(${this.layerId}: ${this.name}, ${this.getUtilization().toFixed(1)}% utilized)`;
  }
}

// ── MultiLayerScaler ──────────────────────────────────────────────────────────

class MultiLayerScaler {
  /**
   * @param {object} [opts]
   * @param {number} [opts.initialLayers=3]
   * @param {number} [opts.defaultCapacity=1000]
   * @param {boolean} [opts.autoExpand=true]
   * @param {number} [opts.karmaThreshold=80]
   */
  constructor({ initialLayers = 3, defaultCapacity = 1000, autoExpand = true, karmaThreshold = 80 } = {}) {
    this.defaultCapacity = defaultCapacity;
    this.autoExpand = autoExpand;
    this.karmaThreshold = karmaThreshold;
    this.layers = [];
    this.metrics = {
      totalRequests: 0,
      layersCreated: 0,
      scalingEvents: 0,
      karmaAccumulation: 0,
    };

    for (let i = 0; i < initialLayers; i++) {
      this._addLayer(`Dimension-${i + 1}`);
    }
  }

  _addLayer(name) {
    const layer = new ScalingLayer(this.layers.length, name, this.defaultCapacity);
    this.layers.push(layer);
    this.metrics.layersCreated++;
    return layer;
  }

  /**
   * Distribute load across available layers using karmic-balance algorithm.
   * Auto-expands dimensions when all layers are saturated.
   * @param {number} load
   * @returns {object}
   */
  distributeLoad(load) {
    this.metrics.totalRequests++;

    // Find layer with lowest utilization
    const best = this.layers.reduce((min, l) =>
      l.getUtilization() < min.getUtilization() ? l : min
    );

    if (best.addLoad(load)) {
      this.metrics.karmaAccumulation += best.karmaScore * 0.1;
      return {
        success: true,
        layer: best.layerId,
        layerName: best.name,
        utilization: parseFloat(best.getUtilization().toFixed(2)),
        karmaGained: parseFloat((best.karmaScore * 0.1).toFixed(4)),
      };
    }

    if (!this.autoExpand) {
      return { success: false, reason: 'Load exceeds capacity and auto-expand is disabled' };
    }

    // Expand — create new dimension
    const newLayer = this._addLayer(`Dimension-${this.layers.length + 1}`);
    this.metrics.scalingEvents++;
    if (newLayer.addLoad(load)) {
      return {
        success: true,
        layer: newLayer.layerId,
        layerName: newLayer.name,
        utilization: parseFloat(newLayer.getUtilization().toFixed(2)),
        newDimension: true,
        scalingEvent: this.metrics.scalingEvents,
      };
    }

    return { success: false, reason: 'Load exceeds single-layer capacity' };
  }

  /** Get full status of all layers and metrics. */
  getStatus() {
    const avgUtil = this.layers.length
      ? this.layers.reduce((s, l) => s + l.getUtilization(), 0) / this.layers.length
      : 0;
    return {
      totalLayers: this.layers.length,
      activeLayers: this.layers.filter(l => l.active).length,
      averageUtilization: parseFloat(avgUtil.toFixed(2)),
      metrics: { ...this.metrics },
      layers: this.layers.map(l => l.toJSON()),
    };
  }

  /**
   * Optimize load distribution for karmic balance.
   * Rebalances load evenly across all layers.
   */
  optimize() {
    if (!this.layers.length) return { optimized: false, reason: 'No layers available' };

    const totalLoad = this.layers.reduce((s, l) => s + l.currentLoad, 0);
    const target = Math.floor(totalLoad / this.layers.length);
    let adjustments = 0;

    for (const layer of this.layers) {
      if (Math.abs(layer.currentLoad - target) > LOAD_ADJUSTMENT_THRESHOLD) {
        layer.currentLoad = target;
        adjustments++;
      }
    }

    const avgUtil = this.layers.reduce((s, l) => s + l.getUtilization(), 0) / this.layers.length;
    return {
      optimized: true,
      adjustments,
      averageUtilization: parseFloat(avgUtil.toFixed(2)),
      karmaBalance: avgUtil < this.karmaThreshold ? 'Optimal' : 'Needs attention',
    };
  }

  /** Emit status payload suitable for GHL custom-field sync. */
  toGHLPayload() {
    const status = this.getStatus();
    return {
      ScrollSoul_Total_Layers: String(status.totalLayers),
      ScrollSoul_Active_Layers: String(status.activeLayers),
      ScrollSoul_Avg_Utilization: `${status.averageUtilization}%`,
      ScrollSoul_Total_Requests: String(status.metrics.totalRequests),
      ScrollSoul_Scaling_Events: String(status.metrics.scalingEvents),
      ScrollSoul_Karma_Accumulation: String(parseFloat(status.metrics.karmaAccumulation.toFixed(4))),
      ScrollSoul_Last_Sync: new Date().toISOString(),
    };
  }
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = { ScalingLayer, MultiLayerScaler };
