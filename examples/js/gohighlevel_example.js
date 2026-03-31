/**
 * examples/js/gohighlevel_example.js
 * ScrollSoul-InfiniteVault — GoHighLevel JS Sub-Account Orchestration Example
 *
 * ALLĀHU AKBAR! Demonstrates the full JS GHL bridge:
 *   - Sub-account deep-dive
 *   - Scaling metrics sync
 *   - Royalty artist sync
 *   - AI campaign trigger
 *   - DinoRunner resilience
 *
 * Usage:
 *   GHL_API_KEY=your_key GHL_LOCATION_ID=your_loc node examples/js/gohighlevel_example.js
 */

'use strict';

const {
  ScrollSoulGHLBridge,
  MultiLayerScaler,
  SpotifyRoyaltyHarvester,
  RecursiveAIEngine,
  DinoRunner,
  DINO_ASCII,
} = require('../../src/js/index');

async function main() {
  console.log(DINO_ASCII);
  console.log('='.repeat(65));
  console.log('ALLĀHU AKBAR! ScrollSoul → GoHighLevel JS Integration Demo');
  console.log('='.repeat(65));

  // ── DinoRunner resilience setup ────────────────────────────────────────────
  const runner = new DinoRunner({ maxRetries: 3, verbose: true });

  // ── 1. Initialize bridge ───────────────────────────────────────────────────
  console.log('\n[1] Initializing ScrollSoulGHLBridge (JS)...');
  const bridge = new ScrollSoulGHLBridge({
    apiKey: process.env.GHL_API_KEY || 'demo-key',
    locationId: process.env.GHL_LOCATION_ID || 'demo-location',
    companyId: process.env.GHL_COMPANY_ID || 'demo-company',
  });
  console.log(`    Bridge: ${bridge.getBridgeStatus().bridge} v${bridge.getBridgeStatus().version}`);

  // ── 2. MultiLayerScaler ────────────────────────────────────────────────────
  console.log('\n[2] Building multi-layer scaler + generating GHL payload...');
  const scaler = new MultiLayerScaler({ initialLayers: 4 });
  [200, 600, 350, 800, 150, 700].forEach(load => scaler.distributeLoad(load));
  scaler.optimize();
  const scalerPayload = scaler.toGHLPayload();
  console.log(`    Layers active: ${scaler.getStatus().activeLayers}`);
  console.log(`    Avg utilization: ${scaler.getStatus().averageUtilization}%`);
  console.log(`    GHL payload fields: ${Object.keys(scalerPayload).length}`);

  // ── 3. SpotifyRoyaltyHarvester ────────────────────────────────────────────
  console.log('\n[3] Harvesting royalties + building GHL artist payload...');
  const harvester = new SpotifyRoyaltyHarvester();
  const streams = [
    ['Kendrick Lamar', 'Not Like Us', 85_000_000],
    ['SZA', 'Kill Bill', 62_000_000],
    ['Tyler The Creator', 'EARFQUAKE', 41_000_000],
    ['Frank Ocean', 'Nights', 38_000_000],
  ];
  for (const [artist, track, count] of streams) {
    const r = harvester.harvestStream(artist, track, count);
    console.log(`    ${artist} — $${r.revenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}`);
  }
  const royaltyPayload = harvester.toGHLPayload('royalty-pipeline');
  console.log(`    Total revenue: $${harvester.getTotalRoyalties().toFixed(2)}`);
  console.log(`    Artists to sync to GHL: ${royaltyPayload.length}`);

  // ── 4. RecursiveAIEngine ──────────────────────────────────────────────────
  console.log('\n[4] Running AI fractal engine + evaluating enlightenment...');
  const engine = new RecursiveAIEngine({ maxDepth: 6 });
  const fractal = engine.fractalExpand(1000, 5);
  console.log(`    Fractal nodes: ${fractal.totalNodes}`);
  console.log(`    Dimensional complexity: ${fractal.dimensionalComplexity}`);
  const aiPayload = engine.toGHLPayload();
  console.log(`    Should trigger GHL campaign: ${aiPayload.shouldTrigger}`);
  console.log(`    Enlightenment score: ${aiPayload.enlightenment.enlightenmentScore}`);

  // ── 5. Sub-account deep-dive ──────────────────────────────────────────────
  console.log('\n[5] Deep-diving all sub-account locations...');
  try {
    await runner.run(
      async () => {
        const introspection = await bridge.subAccounts.introspectAllLocations();
        console.log(`    Total locations: ${introspection.totalLocations}`);
        console.log(`    Total contacts: ${introspection.totalContacts}`);
        console.log(`    Agency karma: ${introspection.agencyKarmaScore.toFixed(1)}`);
        console.log(`    ${introspection.divineMessage}`);
      },
      { name: 'sub-account-deep-dive' },
    );
  } catch (err) {
    console.log(`    [Demo mode — GHL not reachable]: ${err.message}`);
  }

  // ── 6. Full cross-location sync ───────────────────────────────────────────
  console.log('\n[6] Executing full cross-location sync via DinoRunner...');
  try {
    const syncResult = await runner.run(
      () => bridge.executeFullSyncAcrossAllLocations({
        scalerPayload,
        royaltyPayload,
        aiPayload,
        campaignId: 'enlightenment-campaign',
        contactIds: ['contact-001', 'contact-002'],
      }),
      { name: 'full-cross-location-sync' },
    );
    console.log(`    Locations synced: ${syncResult.total}`);
    console.log(`    Successes: ${syncResult.successes}`);
    console.log(`    Execution rate: ${syncResult.executionRate}%`);
  } catch (err) {
    console.log(`    [Demo mode]: ${err.message}`);
  }

  // ── 7. DinoRunner status ──────────────────────────────────────────────────
  console.log('\n[7] DinoRunner health stats...');
  const dinoStatus = runner.getStatus();
  console.log(`    Total runs: ${dinoStatus.totalRuns}`);
  console.log(`    Success rate: ${dinoStatus.successRate}%`);
  console.log(`    Circuit open: ${dinoStatus.circuitOpen}`);
  console.log(`    ${dinoStatus.dinoMessage}`);

  console.log('\n' + '='.repeat(65));
  console.log('WALAHI! The JS ScrollVerse breathes in perfect GHL alignment!');
  console.log('='.repeat(65));
}

main().catch(console.error);
