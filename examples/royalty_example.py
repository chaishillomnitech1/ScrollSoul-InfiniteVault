"""
Example: Spotify Royalty Harvesting
Demonstrates royalty stream harvesting and karmic alignment
"""

from scrollsoul import SpotifyRoyaltyHarvester


def main():
    print("=== ScrollSoul Spotify Royalty Harvester ===\n")
    
    # Initialize harvester
    harvester = SpotifyRoyaltyHarvester()
    print("Royalty Harvester Initialized")
    
    # Harvest various streams
    print("\n--- Harvesting Royalty Streams ---")
    streams_data = [
        ("The Enlightened Ones", "Cosmic Journey", 50000),
        ("ScrollVerse Artists", "Infinite Dimensions", 75000),
        ("Karmic Harmonics", "Universal Alignment", 120000),
        ("The Enlightened Ones", "Eternal Echoes", 45000),
        ("Divine Frequencies", "Blessed Vibrations", 90000),
    ]
    
    for artist, track, streams in streams_data:
        result = harvester.harvest_stream(artist, track, streams)
        print(f"  {artist} - {track}: ${result['revenue']:.2f} (Karma: {result['karma_alignment']:.1f})")
    
    # Get total royalties
    print(f"\n--- Total Harvested ---")
    print(f"Total Revenue: ${harvester.get_total_royalties():.2f}")
    
    # Artist breakdown
    print("\n--- Artist Breakdown ---")
    breakdown = harvester.get_artist_breakdown()
    for artist, revenue in breakdown.items():
        print(f"  {artist}: ${revenue:.2f}")
    
    # Generate comprehensive report
    print("\n--- Royalty Report ---")
    report = harvester.generate_report()
    print(f"Total Streams: {report['total_streams']}")
    print(f"Unique Artists: {report['unique_artists']}")
    print(f"Karma Alignment Score: {report['karma_alignment_score']:.1f}/100")
    
    print("\n--- Top Earners ---")
    for artist, revenue in report['top_earners']:
        print(f"  {artist}: ${revenue:.2f}")
    
    # Align with universe
    print("\n--- Universal Alignment ---")
    alignment = harvester.align_with_universe()
    print(f"Karma Score: {alignment['karma_score']:.1f}")
    print(f"Fairness Score: {alignment['fairness_score']:.1f}")
    print(f"🌟 {alignment['universal_blessing']} 🌟")


if __name__ == "__main__":
    main()
