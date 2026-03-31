/**
 * spotify_royalty_harvesting.js
 * ScrollSoul-InfiniteVault — Spotify Royalty Harvesting (JavaScript)
 *
 * WALAHI! Harvest streaming royalties and align with karmic fairness —
 * then push every artist directly into GoHighLevel as a contact + opportunity.
 *
 * Usage:
 *   const { SpotifyRoyaltyHarvester } = require('./spotify_royalty_harvesting');
 *   const harvester = new SpotifyRoyaltyHarvester();
 *   harvester.harvestStream('Artist Name', 'Track Title', 50000);
 */

'use strict';

// ── RoyaltyStream ─────────────────────────────────────────────────────────────

class RoyaltyStream {
  /**
   * @param {string} artist
   * @param {string} track
   * @param {number} streams
   * @param {number} [ratePerStream=0.003]
   */
  constructor(artist, track, streams, ratePerStream = 0.003) {
    this.artist = artist;
    this.track = track;
    this.streams = streams;
    this.ratePerStream = ratePerStream;
    this.timestamp = new Date().toISOString();
  }

  calculateRevenue() {
    return parseFloat((this.streams * this.ratePerStream).toFixed(6));
  }

  toJSON() {
    return {
      artist: this.artist,
      track: this.track,
      streams: this.streams,
      ratePerStream: this.ratePerStream,
      revenue: this.calculateRevenue(),
      timestamp: this.timestamp,
    };
  }

  toString() {
    return `RoyaltyStream(${this.artist} — ${this.track}: $${this.calculateRevenue().toFixed(4)})`;
  }
}

// ── SpotifyRoyaltyHarvester ───────────────────────────────────────────────────

class SpotifyRoyaltyHarvester {
  /**
   * @param {object} [opts]
   * @param {number} [opts.defaultRatePerStream=0.003]
   * @param {number} [opts.karmaBoostThreshold=10]
   * @param {number} [opts.alignmentDecayRate=0.1]
   */
  constructor({
    defaultRatePerStream = 0.003,
    karmaBoostThreshold = 10,
    alignmentDecayRate = 0.1,
  } = {}) {
    this.defaultRatePerStream = defaultRatePerStream;
    this.karmaBoostThreshold = karmaBoostThreshold;
    this.alignmentDecayRate = alignmentDecayRate;
    this.streams = [];
    this.totalHarvested = 0;
    this.karmaAlignmentScore = 100.0;
  }

  /**
   * Harvest a new royalty stream.
   * @param {string} artist
   * @param {string} track
   * @param {number} streams
   * @param {number} [ratePerStream]
   * @returns {object}
   */
  harvestStream(artist, track, streams, ratePerStream) {
    const rate = ratePerStream ?? this.defaultRatePerStream;
    const stream = new RoyaltyStream(artist, track, streams, rate);
    const revenue = stream.calculateRevenue();

    this.streams.push(stream);
    this.totalHarvested = parseFloat((this.totalHarvested + revenue).toFixed(6));
    this._updateKarmaAlignment(revenue);

    return {
      success: true,
      artist,
      track,
      streams,
      revenue,
      karmaAlignment: parseFloat(this.karmaAlignmentScore.toFixed(2)),
      timestamp: stream.timestamp,
    };
  }

  _updateKarmaAlignment(revenue) {
    if (revenue > this.karmaBoostThreshold) {
      this.karmaAlignmentScore = Math.min(100, this.karmaAlignmentScore + 0.5);
    } else {
      this.karmaAlignmentScore = Math.max(0, this.karmaAlignmentScore - this.alignmentDecayRate);
    }
  }

  getTotalRoyalties() {
    return this.totalHarvested;
  }

  getArtistBreakdown() {
    return this.streams.reduce((acc, s) => {
      acc[s.artist] = parseFloat(((acc[s.artist] || 0) + s.calculateRevenue()).toFixed(6));
      return acc;
    }, {});
  }

  /**
   * Generate a comprehensive royalty report.
   * @returns {object}
   */
  generateReport() {
    const breakdown = this.getArtistBreakdown();
    const sorted = Object.entries(breakdown).sort(([, a], [, b]) => b - a);
    return {
      totalStreams: this.streams.length,
      totalRevenue: this.totalHarvested,
      karmaAlignmentScore: parseFloat(this.karmaAlignmentScore.toFixed(2)),
      uniqueArtists: Object.keys(breakdown).length,
      artistBreakdown: breakdown,
      topEarners: sorted.slice(0, 5).map(([artist, revenue]) => ({ artist, revenue })),
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Align royalty distribution with universal governance principles.
   * @returns {object}
   */
  alignWithUniverse() {
    const breakdown = this.getArtistBreakdown();
    const revenues = Object.values(breakdown);
    const maxRevenue = revenues.length ? Math.max(...revenues) : 1;
    const avgRevenue = revenues.length
      ? revenues.reduce((s, v) => s + v, 0) / revenues.length
      : 0;
    const fairnessScore = parseFloat(Math.min(100, (avgRevenue / maxRevenue) * 100).toFixed(2));

    return {
      aligned: true,
      karmaScore: parseFloat(this.karmaAlignmentScore.toFixed(2)),
      fairnessScore,
      totalHarvested: this.totalHarvested,
      universalBlessing: 'WALAHI! The royalties flow with divine alignment!',
    };
  }

  /**
   * Emit a payload shaped for GHL contact/opportunity batch upsert.
   * Each entry represents one artist to sync.
   */
  toGHLPayload(pipelineId = '') {
    const breakdown = this.getArtistBreakdown();
    return Object.entries(breakdown).map(([artist, revenue]) => ({
      artist,
      revenue,
      streams: Math.round(revenue / this.defaultRatePerStream),
      email: `${artist.toLowerCase().replace(/\s+/g, '.')}@scrollsoul.artist`,
      tags: ['scrollsoul-artist', 'royalty-stream'],
      pipelineId,
      opportunityName: `${artist} — Royalty Stream`,
      monetaryValue: revenue,
      note: `[ScrollSoul Royalty] Revenue: $${revenue.toFixed(4)} | Synced: ${new Date().toISOString()}`,
    }));
  }
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = { RoyaltyStream, SpotifyRoyaltyHarvester };
