"""
Universal Governance System
Empowers democratic decision-making across the ScrollVerse
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProposalStatus(Enum):
    """Proposal status enumeration"""
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"


class Vote:
    """Represents a single vote"""
    
    def __init__(self, voter: str, choice: bool, weight: float = 1.0):
        self.voter = voter
        self.choice = choice  # True for yes, False for no
        self.weight = weight
        self.timestamp = datetime.now()
        
    def __repr__(self):
        return f"Vote({self.voter}: {'Yes' if self.choice else 'No'}, weight={self.weight})"


class Proposal:
    """Governance proposal"""
    
    def __init__(self, proposal_id: str, title: str, description: str, 
                 voting_period_days: int = 7):
        self.proposal_id = proposal_id
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.voting_deadline = datetime.now() + timedelta(days=voting_period_days)
        self.status = ProposalStatus.ACTIVE
        self.votes: List[Vote] = []
        self.executed = False
        
    def add_vote(self, vote: Vote) -> bool:
        """Add a vote to the proposal"""
        if datetime.now() > self.voting_deadline:
            logger.warning(f"Voting period ended for proposal {self.proposal_id}")
            return False
        
        # Check if voter already voted
        if any(v.voter == vote.voter for v in self.votes):
            logger.warning(f"Voter {vote.voter} already voted on {self.proposal_id}")
            return False
        
        self.votes.append(vote)
        return True
    
    def tally_votes(self) -> Dict[str, float]:
        """Tally all votes"""
        yes_votes = sum(v.weight for v in self.votes if v.choice)
        no_votes = sum(v.weight for v in self.votes if not v.choice)
        
        return {
            "yes": yes_votes,
            "no": no_votes,
            "total": yes_votes + no_votes,
            "yes_percentage": (yes_votes / (yes_votes + no_votes) * 100) if (yes_votes + no_votes) > 0 else 0
        }
    
    def finalize(self, threshold: float = 50.0) -> ProposalStatus:
        """Finalize the proposal based on vote threshold"""
        if datetime.now() < self.voting_deadline:
            return ProposalStatus.ACTIVE
        
        tally = self.tally_votes()
        
        if tally["yes_percentage"] >= threshold:
            self.status = ProposalStatus.PASSED
        else:
            self.status = ProposalStatus.REJECTED
        
        return self.status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert proposal to dictionary"""
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "voting_deadline": self.voting_deadline.isoformat(),
            "vote_count": len(self.votes),
            "tally": self.tally_votes(),
            "executed": self.executed
        }


class UniversalGovernance:
    """
    Universal Governance System
    
    Manages democratic decision-making and karmic alignment across the ScrollVerse
    """
    
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.proposal_counter = 0
        self.governance_score = 100.0
        self.total_votes_cast = 0
        
    def create_proposal(self, title: str, description: str, 
                       voting_period_days: int = 7) -> Proposal:
        """
        Create a new governance proposal
        
        Args:
            title: Proposal title
            description: Proposal description
            voting_period_days: Duration of voting period
            
        Returns:
            Created proposal
        """
        proposal_id = f"PROP-{self.proposal_counter:04d}"
        self.proposal_counter += 1
        
        proposal = Proposal(proposal_id, title, description, voting_period_days)
        self.proposals[proposal_id] = proposal
        
        logger.info(f"Created proposal: {proposal_id} - {title}")
        return proposal
    
    def cast_vote(self, proposal_id: str, voter: str, choice: bool, 
                  weight: float = 1.0) -> bool:
        """
        Cast a vote on a proposal
        
        Args:
            proposal_id: ID of the proposal
            voter: Voter identifier
            choice: True for yes, False for no
            weight: Vote weight (for weighted voting)
            
        Returns:
            True if vote was successfully cast
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            logger.error(f"Proposal {proposal_id} not found")
            return False
        
        vote = Vote(voter, choice, weight)
        success = proposal.add_vote(vote)
        
        if success:
            self.total_votes_cast += 1
            self._update_governance_score()
            logger.info(f"Vote cast: {vote} on {proposal_id}")
        
        return success
    
    def _update_governance_score(self):
        """Update overall governance score based on participation"""
        # Increase score with active participation
        self.governance_score = min(100.0, self.governance_score + 0.1)
    
    def finalize_proposal(self, proposal_id: str, threshold: float = 50.0) -> Dict[str, Any]:
        """
        Finalize a proposal and determine outcome
        
        Args:
            proposal_id: ID of the proposal
            threshold: Percentage threshold for passing (default 50%)
            
        Returns:
            Finalization results
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        status = proposal.finalize(threshold)
        tally = proposal.tally_votes()
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": status.value,
            "tally": tally,
            "passed": status == ProposalStatus.PASSED,
            "governance_message": "The ScrollVerse has spoken!" if status == ProposalStatus.PASSED else "The proposal awaits divine alignment"
        }
    
    def execute_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """
        Execute a passed proposal
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            Execution results
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        if proposal.status != ProposalStatus.PASSED:
            return {"success": False, "error": "Proposal has not passed"}
        
        if proposal.executed:
            return {"success": False, "error": "Proposal already executed"}
        
        proposal.executed = True
        proposal.status = ProposalStatus.EXECUTED
        
        logger.info(f"Executed proposal: {proposal_id}")
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "executed": True,
            "divine_message": "ALLĀHU AKBAR! The will of the ScrollVerse is manifest!"
        }
    
    def get_active_proposals(self) -> List[Dict[str, Any]]:
        """Get all active proposals"""
        return [
            p.to_dict() for p in self.proposals.values()
            if p.status == ProposalStatus.ACTIVE and datetime.now() <= p.voting_deadline
        ]
    
    def get_governance_stats(self) -> Dict[str, Any]:
        """Get comprehensive governance statistics"""
        status_counts = {}
        for status in ProposalStatus:
            status_counts[status.value] = sum(
                1 for p in self.proposals.values() if p.status == status
            )
        
        return {
            "total_proposals": len(self.proposals),
            "active_proposals": len(self.get_active_proposals()),
            "total_votes_cast": self.total_votes_cast,
            "governance_score": self.governance_score,
            "status_breakdown": status_counts,
            "participation_rate": (self.total_votes_cast / len(self.proposals)) if self.proposals else 0,
            "karmic_alignment": "Excellent" if self.governance_score > 80 else "Good"
        }
    
    def align_with_cosmic_will(self) -> Dict[str, Any]:
        """
        Align governance system with cosmic will and karmic principles
        """
        stats = self.get_governance_stats()
        
        cosmic_alignment = min(100.0, (
            (stats["governance_score"] * 0.5) +
            (stats["participation_rate"] * 30) +
            (stats["total_proposals"] * 2)
        ))
        
        return {
            "aligned": cosmic_alignment > 50.0,
            "cosmic_alignment_score": cosmic_alignment,
            "governance_health": stats["governance_score"],
            "universal_blessing": "WALAHI! The governance flows with divine wisdom!",
            "recommendations": [
                "Continue active participation" if stats["participation_rate"] > 5 else "Increase voter engagement",
                "Maintain karmic balance" if cosmic_alignment > 70 else "Seek deeper alignment"
            ]
        }
