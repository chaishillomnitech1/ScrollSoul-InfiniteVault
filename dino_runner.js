/**
 * dino_runner.js
 * ScrollSoul-InfiniteVault — DinoRunner Resilience & Persistence Engine
 *
 * Inspired by Chrome's T-Rex offline game: the dino KEEPS RUNNING no matter
 * what obstacles appear. This module wraps any async operation with
 * exponential-backoff retry, circuit-breaker protection, keep-alive pinging,
 * and cross-sub-account health monitoring — so ScrollSoul NEVER stops.
 *
 *   "When the network drops, the dino runs.
 *    WALAHI! The ScrollVerse never goes offline."
 *
 * Usage:
 *   const { DinoRunner } = require('./dino_runner');
 *   const runner = new DinoRunner({ maxRetries: 5 });
 *   const result = await runner.run(() => someAsyncGHLCall());
 */

'use strict';

// ── Constants ─────────────────────────────────────────────────────────────────

const DINO_ASCII = `
     ____
    /    \\
   | o  o |   ScrollSoul DinoRunner
    \\  ~ /    WALAHI! Never stops running.
  __/----\\__
 /          \\
`;

const DEFAULT_MAX_RETRIES = 5;
const DEFAULT_BASE_DELAY_MS = 500;
const DEFAULT_MAX_DELAY_MS = 30000;
const DEFAULT_JITTER_MS = 200;
const DEFAULT_CIRCUIT_THRESHOLD = 5;   // failures before circuit opens
const DEFAULT_CIRCUIT_RESET_MS = 60000; // 60 s before half-open attempt

// ── DinoRunner ────────────────────────────────────────────────────────────────

/**
 * Resilience engine with exponential backoff, jitter, and circuit-breaker.
 * Wraps any async function and keeps it running through transient failures.
 */
class DinoRunner {
  /**
   * @param {object}  [opts]
   * @param {number}  [opts.maxRetries=5]         Max retry attempts per run.
   * @param {number}  [opts.baseDelayMs=500]       Initial backoff delay (ms).
   * @param {number}  [opts.maxDelayMs=30000]      Maximum backoff cap (ms).
   * @param {number}  [opts.jitterMs=200]          Random jitter ceiling (ms).
   * @param {number}  [opts.circuitThreshold=5]    Consecutive failures to open circuit.
   * @param {number}  [opts.circuitResetMs=60000]  Time before circuit half-opens (ms).
   * @param {boolean} [opts.verbose=false]         Log each attempt.
   */
  constructor({
    maxRetries = DEFAULT_MAX_RETRIES,
    baseDelayMs = DEFAULT_BASE_DELAY_MS,
    maxDelayMs = DEFAULT_MAX_DELAY_MS,
    jitterMs = DEFAULT_JITTER_MS,
    circuitThreshold = DEFAULT_CIRCUIT_THRESHOLD,
    circuitResetMs = DEFAULT_CIRCUIT_RESET_MS,
    verbose = false,
  } = {}) {
    this.maxRetries = maxRetries;
    this.baseDelayMs = baseDelayMs;
    this.maxDelayMs = maxDelayMs;
    this.jitterMs = jitterMs;
    this.circuitThreshold = circuitThreshold;
    this.circuitResetMs = circuitResetMs;
    this.verbose = verbose;

    // Stats
    this.totalRuns = 0;
    this.totalSuccesses = 0;
    this.totalFailures = 0;
    this.totalRetries = 0;
    this.obstacles = []; // history of failures

    // Circuit-breaker state
    this._circuitOpen = false;
    this._consecutiveFailures = 0;
    this._circuitOpenedAt = null;
  }

  // ── Backoff helpers ───────────────────────────────────────────────────────

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  _backoffMs(attempt) {
    const exponential = Math.min(
      this.maxDelayMs,
      this.baseDelayMs * Math.pow(2, attempt),
    );
    const jitter = Math.floor(Math.random() * this.jitterMs);
    return exponential + jitter;
  }

  // ── Circuit breaker ───────────────────────────────────────────────────────

  _isCircuitOpen() {
    if (!this._circuitOpen) return false;
    const elapsed = Date.now() - this._circuitOpenedAt;
    if (elapsed >= this.circuitResetMs) {
      // Half-open: allow one attempt
      this._circuitOpen = false;
      this._consecutiveFailures = 0;
      if (this.verbose) console.log('[DinoRunner] Circuit half-open — trying again...');
      return false;
    }
    return true;
  }

  _recordSuccess() {
    this._consecutiveFailures = 0;
    this._circuitOpen = false;
  }

  _recordFailure(err) {
    this._consecutiveFailures++;
    this.obstacles.push({ error: err.message, ts: new Date().toISOString() });
    if (this._consecutiveFailures >= this.circuitThreshold) {
      this._circuitOpen = true;
      this._circuitOpenedAt = Date.now();
      console.warn(
        `[DinoRunner] ⚡ Circuit OPEN after ${this._consecutiveFailures} failures. ` +
        `Reset in ${this.circuitResetMs / 1000}s.`
      );
    }
  }

  // ── Core run ──────────────────────────────────────────────────────────────

  /**
   * Run an async function with retry + circuit-breaker protection.
   *
   * @template T
   * @param {() => Promise<T>} fn          The function to execute.
   * @param {object}           [opts]
   * @param {string}           [opts.name] Label for logging.
   * @returns {Promise<T>}
   */
  async run(fn, { name = 'task' } = {}) {
    this.totalRuns++;

    if (this._isCircuitOpen()) {
      const err = new Error(`[DinoRunner] Circuit is OPEN — "${name}" blocked until circuit resets.`);
      this.totalFailures++;
      throw err;
    }

    let lastError = new Error('No attempts made');

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        if (this.verbose && attempt > 0) {
          console.log(`[DinoRunner] 🦖 Retry ${attempt}/${this.maxRetries} — "${name}"`);
        }
        const result = await fn();
        this._recordSuccess();
        this.totalSuccesses++;
        return result;
      } catch (err) {
        lastError = err;
        this.totalRetries++;

        if (attempt === this.maxRetries) break;

        const wait = this._backoffMs(attempt);
        if (this.verbose) {
          console.warn(
            `[DinoRunner] 🦖 "${name}" failed (attempt ${attempt + 1}): ${err.message}. ` +
            `Jumping in ${wait}ms...`
          );
        }
        await this._delay(wait);
      }
    }

    this._recordFailure(lastError);
    this.totalFailures++;
    throw lastError;
  }

  /**
   * Run a batch of async functions, each individually protected.
   * Never stops — collects all results + errors.
   *
   * @param {Array<{ fn: () => Promise<*>, name?: string }>} tasks
   * @returns {Promise<Array<{ name: string, success: boolean, result?: *, error?: string }>>}
   */
  async runBatch(tasks) {
    const results = [];
    for (const { fn, name = 'batch-task' } of tasks) {
      try {
        const result = await this.run(fn, { name });
        results.push({ name, success: true, result });
      } catch (err) {
        results.push({ name, success: false, error: err.message });
      }
    }
    return results;
  }

  /**
   * Execute a function across every sub-account location ID, never stopping.
   *
   * @param {string[]} locationIds
   * @param {(locationId: string) => Promise<*>} action
   * @returns {Promise<object>}
   */
  async executeAcrossLocations(locationIds, action) {
    const tasks = locationIds.map(locId => ({
      name: `location:${locId}`,
      fn: () => action(locId),
    }));
    const results = await this.runBatch(tasks);
    const successes = results.filter(r => r.success).length;

    return {
      total: locationIds.length,
      successes,
      failures: locationIds.length - successes,
      results: results.reduce((acc, r) => {
        acc[r.name.replace('location:', '')] = r;
        return acc;
      }, {}),
      executionRate: parseFloat(((successes / (locationIds.length || 1)) * 100).toFixed(2)),
      dinoStatus: this.getStatus(),
    };
  }

  // ── Keep-alive ────────────────────────────────────────────────────────────

  /**
   * Start a keep-alive interval that pings a health-check function.
   * Returns a handle; call clearInterval(handle) to stop.
   *
   * @param {() => Promise<*>} healthCheckFn
   * @param {number} [intervalMs=30000]
   * @returns {NodeJS.Timeout}
   */
  keepAlive(healthCheckFn, intervalMs = 30000) {
    console.log(`[DinoRunner] 🦖 Keep-alive started — pinging every ${intervalMs / 1000}s`);
    return setInterval(async () => {
      try {
        await this.run(healthCheckFn, { name: 'keep-alive' });
        if (this.verbose) console.log('[DinoRunner] ✅ Keep-alive OK');
      } catch (err) {
        console.warn('[DinoRunner] ⚠️  Keep-alive failed:', err.message);
      }
    }, intervalMs);
  }

  // ── Status ────────────────────────────────────────────────────────────────

  /** Get full DinoRunner health stats. */
  getStatus() {
    return {
      totalRuns: this.totalRuns,
      totalSuccesses: this.totalSuccesses,
      totalFailures: this.totalFailures,
      totalRetries: this.totalRetries,
      successRate: parseFloat(
        ((this.totalSuccesses / (this.totalRuns || 1)) * 100).toFixed(2)
      ),
      circuitOpen: this._circuitOpen,
      consecutiveFailures: this._consecutiveFailures,
      obstacleCount: this.obstacles.length,
      lastObstacle: this.obstacles[this.obstacles.length - 1] || null,
      karmaAlignment: this.totalFailures === 0 ? 100 : Math.max(
        0,
        100 - (this.totalFailures / (this.totalRuns || 1)) * 100,
      ),
      dinoMessage: this._circuitOpen
        ? '⚡ Circuit open — dino crouching, waiting to jump again...'
        : '🦖 WALAHI! The dino keeps running — nothing stops ScrollSoul!',
    };
  }

  /** Print the ASCII dino and stats to console. */
  announce() {
    console.log(DINO_ASCII);
    console.table(this.getStatus());
  }
}

// ── RetryQueue ────────────────────────────────────────────────────────────────

/**
 * A persistent async retry queue — enqueue tasks and the DinoRunner
 * drains them continuously, retrying failures automatically.
 */
class RetryQueue {
  /**
   * @param {DinoRunner} runner
   * @param {number} [concurrency=3]
   */
  constructor(runner, concurrency = 3) {
    this.runner = runner;
    this.concurrency = concurrency;
    this._queue = [];
    this._running = 0;
    this._processed = 0;
  }

  /**
   * Enqueue a task.
   * @param {() => Promise<*>} fn
   * @param {string} [name]
   */
  enqueue(fn, name = 'queued-task') {
    return new Promise((resolve, reject) => {
      this._queue.push({ fn, name, resolve, reject });
      this._drain();
    });
  }

  _drain() {
    while (this._running < this.concurrency && this._queue.length > 0) {
      const { fn, name, resolve, reject } = this._queue.shift();
      this._running++;
      this.runner
        .run(fn, { name })
        .then(result => { this._processed++; resolve(result); })
        .catch(err => reject(err))
        .finally(() => { this._running--; this._drain(); });
    }
  }

  getQueueStatus() {
    return {
      pending: this._queue.length,
      running: this._running,
      processed: this._processed,
      concurrency: this.concurrency,
    };
  }
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = { DinoRunner, RetryQueue, DINO_ASCII };
