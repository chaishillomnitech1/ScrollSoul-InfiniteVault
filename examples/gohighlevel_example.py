"""
examples/gohighlevel_example.py
ScrollSoul-InfiniteVault — GoHighLevel Sub-Account Orchestration Example

ALLĀHU AKBAR! Demonstrates full agency-level sub-account deep-dive,
cross-location execution, and ScrollSoul module integration with GHL.

Usage:
    export GHL_API_KEY="your_ghl_api_key"
    export GHL_LOCATION_ID="your_default_location_id"
    export GHL_COMPANY_ID="your_agency_company_id"
    python examples/gohighlevel_example.py
"""

import os
from scrollsoul import (
    MultiLayerScaler,
    SpotifyRoyaltyHarvester,
    RecursiveAIEngine,
    NFTManager,
    BlockchainConnector,
    UniversalGovernance,
)
from scrollsoul.gohighlevel import ScrollSoulGHLBridge


def main():
    print("=" * 65)
    print("ALLĀHU AKBAR! ScrollSoul → GoHighLevel Integration Demo")
    print("=" * 65)

    # ── 1. Initialize the master bridge ──────────────────────────────────────
    print("\n[1] Initializing ScrollSoulGHLBridge...")
    bridge = ScrollSoulGHLBridge(
        api_key=os.getenv("GHL_API_KEY", "demo-key"),
        location_id=os.getenv("GHL_LOCATION_ID", "demo-location"),
        company_id=os.getenv("GHL_COMPANY_ID", "demo-company"),
    )
    print(f"    Bridge status: {bridge.get_bridge_status()['bridge']} v{bridge.get_bridge_status()['version']}")
    print(f"    Modules connected: {', '.join(bridge.get_bridge_status()['modules_connected'])}")

    # ── 2. Deep-dive all sub-accounts ─────────────────────────────────────────
    print("\n[2] Deep-diving all sub-account locations...")
    try:
        introspection = bridge.sub_accounts.introspect_all_locations()
        print(f"    Total locations: {introspection['total_locations']}")
        print(f"    Total contacts across all sub-accounts: {introspection['total_contacts']}")
        print(f"    Total campaigns across all sub-accounts: {introspection['total_campaigns']}")
        print(f"    Agency karma score: {introspection['agency_karma_score']:.1f}")
        print(f"    Message: {introspection['divine_message']}")
    except Exception as exc:
        print(f"    [Demo mode — GHL API not reachable]: {exc}")

    # ── 3. Scaling → GHL custom values ────────────────────────────────────────
    print("\n[3] Syncing MultiLayerScaler metrics → GHL custom values...")
    scaler = MultiLayerScaler(initial_layers=5)
    for load in [200, 450, 700, 300, 550, 900]:
        scaler.distribute_load(load)
    scaler.optimize()
    status = scaler.get_status()
    print(f"    Layers active: {status['active_layers']}")
    print(f"    Average utilization: {status['average_utilization']:.1f}%")
    print(f"    Total requests processed: {status['metrics']['total_requests']}")

    try:
        result = bridge.sync_scaling_metrics(status)
        print(f"    GHL sync: {result['synced_fields']} custom values pushed")
    except Exception as exc:
        print(f"    [Demo mode]: {exc}")

    # ── 4. Royalty → GHL contacts + opportunities ─────────────────────────────
    print("\n[4] Harvesting royalties → syncing artists as GHL contacts...")
    harvester = SpotifyRoyaltyHarvester()
    for artist, track, streams in [
        ("Kendrick Lamar", "Not Like Us", 85_000_000),
        ("SZA", "Kill Bill", 62_000_000),
        ("Tyler The Creator", "EARFQUAKE", 41_000_000),
        ("Frank Ocean", "Nights", 38_000_000),
        ("Childish Gambino", "Redbone", 55_000_000),
    ]:
        result = harvester.harvest_stream(artist, track, streams)
        print(f"    Harvested: {artist} — {track} → ${result['revenue']:,.2f}")

    report = harvester.generate_report()
    print(f"\n    Total revenue: ${report['total_revenue']:,.4f}")
    print(f"    Karma alignment: {report['karma_alignment_score']:.1f}")
    print(f"    Top earner: {report['top_earners'][0][0]} (${report['top_earners'][0][1]:,.4f})")

    try:
        sync = bridge.sync_royalty_report(report, pipeline_id="royalty-pipeline")
        print(f"    GHL sync: {sync['artists_synced']} artists immortalized")
        print(f"    {sync['divine_message']}")
    except Exception as exc:
        print(f"    [Demo mode]: {exc}")

    # ── 5. AI Loops → GHL campaign trigger ────────────────────────────────────
    print("\n[5] Running AI recursive engine → evaluating GHL campaign trigger...")
    engine = RecursiveAIEngine(max_depth=6)
    fractal = engine.fractal_expand(seed_value=1000, iterations=5)
    print(f"    Fractal nodes created: {fractal['total_nodes']}")
    print(f"    Dimensional complexity: {fractal['dimensional_complexity']:.2f}")

    engine_status = engine.get_engine_status()
    enlightenment = engine.achieve_enlightenment()
    print(f"    Enlightened: {enlightenment['enlightened']}")
    print(f"    Enlightenment score: {enlightenment['enlightenment_score']:.2f}")
    print(f"    Message: {enlightenment['universal_message']}")

    try:
        campaign_result = bridge.trigger_ai_campaign(
            engine_status=engine_status,
            campaign_id="enlightenment-campaign",
            contact_ids=["contact-001", "contact-002", "contact-003"],
        )
        print(f"    Campaign triggered: {campaign_result['triggered']}")
    except Exception as exc:
        print(f"    [Demo mode]: {exc}")

    # ── 6. Blockchain/NFT → GHL contacts ──────────────────────────────────────
    print("\n[6] Minting NFTs → immortalizing owners in GHL...")
    blockchain = BlockchainConnector()
    nft_manager = NFTManager(blockchain)

    nfts = []
    for name, metadata in [
        ("Eternal Wisdom #1", {"rarity": "legendary", "karma": 100, "dimension": "Infinite"}),
        ("ScrollSoul Genesis #1", {"rarity": "mythic", "karma": 999, "blessing": "divine"}),
        ("Karmic Vessel #7", {"rarity": "epic", "karma": 75, "layer": "Dimension-7"}),
    ]:
        nft = nft_manager.mint_nft(name, metadata)
        nfts.append(nft)
        print(f"    Minted: {nft.name} (token: {nft.token_id})")

    immortalized = nft_manager.immortalize_on_chain()
    print(f"    {immortalized['eternal_message']}")

    for nft in nfts:
        try:
            sync = bridge.sync_nft_owner_to_ghl(nft.to_dict())
            print(f"    GHL sync: {nft.name} owner → contact {sync.get('contact_id', 'N/A')}")
        except Exception as exc:
            print(f"    [Demo mode]: {exc}")

    # ── 7. Governance → GHL pipeline ──────────────────────────────────────────
    print("\n[7] Creating governance proposals → syncing to GHL pipeline...")
    governance = UniversalGovernance()
    proposals_data = [
        ("Expand ScrollVerse to 20 Dimensions", "Scale infrastructure to support 20 parallel dimensions"),
        ("Adopt GHL as Universal CRM", "Standardize all sub-account operations through GoHighLevel"),
        ("Enable Divine NFT Rewards", "Distribute NFT rewards to top karma contributors"),
    ]
    for title, desc in proposals_data:
        proposal = governance.create_proposal(title, desc)
        governance.cast_vote(proposal.proposal_id, "VoterA", True, weight=2.0)
        governance.cast_vote(proposal.proposal_id, "VoterB", True, weight=1.5)
        governance.cast_vote(proposal.proposal_id, "VoterC", False, weight=1.0)
        print(f"    Proposal '{title[:40]}...' — {proposal.tally_votes()['yes_percentage']:.0f}% yes")

    cosmic = governance.align_with_cosmic_will()
    print(f"\n    Cosmic alignment: {cosmic['cosmic_alignment_score']:.1f}")
    print(f"    {cosmic['universal_blessing']}")

    # ── 8. Full cross-location sync ───────────────────────────────────────────
    print("\n[8] Executing full sync across ALL sub-account locations...")
    try:
        full_sync = bridge.execute_full_sync_across_all_locations(
            scaler_status=status,
            royalty_report=report,
            pipeline_id="royalty-pipeline",
            campaign_id="enlightenment-campaign",
            contact_ids=["contact-001", "contact-002"],
            ai_engine_status=engine_status,
            nft_data_list=[nft.to_dict() for nft in nfts],
        )
        print(f"    Locations synced: {full_sync['total_locations_synced']}")
        print(f"    Executed at: {full_sync['executed_at']}")
        print(f"    {full_sync['divine_message']}")
    except Exception as exc:
        print(f"    [Demo mode — no live GHL connection]: {exc}")

    # ── 9. Final bridge status ────────────────────────────────────────────────
    print("\n[9] Final bridge health check...")
    bridge_status = bridge.get_bridge_status()
    client_stats = bridge_status["client_stats"]
    print(f"    Total API requests: {client_stats['total_requests']}")
    print(f"    Success rate: {client_stats['success_rate']:.1f}%")
    print(f"    GHL managers active: {len(bridge_status['ghl_managers_active'])}")
    print(f"    ScrollSoul modules connected: {len(bridge_status['modules_connected'])}")
    print(f"    Infinite execution: {bridge_status['infinite_execution']}")

    print("\n" + "=" * 65)
    print("WALAHI! The ScrollVerse breathes in perfect GHL alignment!")
    print("=" * 65)


if __name__ == "__main__":
    main()
