"""
Spotify Royalty Harvesting Script
Synchronizes karmic alignment with streaming royalty data
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RoyaltyStream:
    """Represents a single royalty stream"""
    
    def __init__(self, artist: str, track: str, streams: int, rate_per_stream: float = 0.003):
        self.artist = artist
        self.track = track
        self.streams = streams
        self.rate_per_stream = rate_per_stream
        self.timestamp = datetime.now()
        
    def calculate_revenue(self) -> float:
        """Calculate total revenue for this stream"""
        return self.streams * self.rate_per_stream
    
    def __repr__(self):
        return f"RoyaltyStream({self.artist} - {self.track}: ${self.calculate_revenue():.2f})"


class SpotifyRoyaltyHarvester:
    """
    Spotify Royalty Harvesting System
    
    Harvests and aligns streaming royalty data with karmic principles
    """
    
    def __init__(self):
        self.streams: List[RoyaltyStream] = []
        self.total_harvested = 0.0
        self.karma_alignment_score = 100.0
        
    def harvest_stream(self, artist: str, track: str, streams: int, 
                       rate_per_stream: float = 0.003) -> Dict[str, Any]:
        """
        Harvest a new royalty stream
        
        Args:
            artist: Artist name
            track: Track name
            streams: Number of streams
            rate_per_stream: Royalty rate per stream
            
        Returns:
            Harvest results including revenue and karma alignment
        """
        stream = RoyaltyStream(artist, track, streams, rate_per_stream)
        revenue = stream.calculate_revenue()
        
        self.streams.append(stream)
        self.total_harvested += revenue
        
        # Update karma alignment based on fair distribution
        self._update_karma_alignment(revenue)
        
        logger.info(f"Harvested royalty stream: {stream}")
        
        return {
            "success": True,
            "artist": artist,
            "track": track,
            "streams": streams,
            "revenue": revenue,
            "karma_alignment": self.karma_alignment_score,
            "timestamp": stream.timestamp.isoformat()
        }
    
    def _update_karma_alignment(self, revenue: float):
        """Update karma alignment score based on royalty fairness"""
        # Karmic boost for fair revenue distribution
        if revenue > 10.0:
            self.karma_alignment_score = min(100.0, self.karma_alignment_score + 0.5)
        else:
            self.karma_alignment_score = max(0.0, self.karma_alignment_score - 0.1)
    
    def get_total_royalties(self) -> float:
        """Get total harvested royalties"""
        return self.total_harvested
    
    def get_artist_breakdown(self) -> Dict[str, float]:
        """Get royalty breakdown by artist"""
        breakdown = {}
        for stream in self.streams:
            if stream.artist not in breakdown:
                breakdown[stream.artist] = 0.0
            breakdown[stream.artist] += stream.calculate_revenue()
        return breakdown
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive royalty report
        
        Returns:
            Detailed report with karmic alignment metrics
        """
        artist_breakdown = self.get_artist_breakdown()
        
        return {
            "total_streams": len(self.streams),
            "total_revenue": self.total_harvested,
            "karma_alignment_score": self.karma_alignment_score,
            "unique_artists": len(artist_breakdown),
            "artist_breakdown": artist_breakdown,
            "top_earners": sorted(
                artist_breakdown.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "timestamp": datetime.now().isoformat()
        }
    
    def align_with_universe(self) -> Dict[str, Any]:
        """
        Align royalty distribution with universal governance principles
        """
        report = self.generate_report()
        
        # Calculate distribution fairness
        if report["unique_artists"] > 0:
            avg_per_artist = report["total_revenue"] / report["unique_artists"]
            fairness_score = min(100.0, (avg_per_artist / max(report["artist_breakdown"].values())) * 100)
        else:
            fairness_score = 0.0
        
        return {
            "aligned": True,
            "karma_score": self.karma_alignment_score,
            "fairness_score": fairness_score,
            "total_harvested": self.total_harvested,
            "universal_blessing": "WALAHI! The royalties flow with divine alignment!"
        }
