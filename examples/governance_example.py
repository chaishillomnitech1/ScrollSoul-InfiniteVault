"""
Example: Universal Governance System
Demonstrates proposal creation, voting, and execution
"""

from scrollsoul import UniversalGovernance


def main():
    print("=== ScrollSoul Universal Governance System ===\n")
    
    # Initialize governance
    governance = UniversalGovernance()
    print("Universal Governance Initialized")
    
    # Create proposals
    print("\n--- Creating Governance Proposals ---")
    proposals = [
        ("Expand ScrollVerse to 10 Dimensions", "Proposal to expand the ScrollVerse infrastructure to support 10 parallel dimensions"),
        ("Increase Karma Rewards by 20%", "Proposal to boost karma rewards for contributors by 20%"),
        ("Implement Eternal NFT Staking", "Proposal to allow NFT staking for passive karma generation"),
    ]
    
    created_proposals = []
    for title, description in proposals:
        proposal = governance.create_proposal(title, description, voting_period_days=7)
        created_proposals.append(proposal.proposal_id)
        print(f"  Created: {proposal.proposal_id} - {title}")
    
    # Cast votes
    print("\n--- Casting Votes ---")
    voters = ["ScrollMaster", "KarmaKeeper", "DimensionGuardian", "EternalWatcher", "CosmicSage"]
    
    for proposal_id in created_proposals[:2]:  # Vote on first two proposals
        print(f"\nVoting on {proposal_id}:")
        for i, voter in enumerate(voters):
            # First proposal gets majority yes, second gets majority no
            choice = True if (proposal_id == created_proposals[0] and i < 4) else (i < 2)
            weight = 1.0 + (i * 0.1)  # Varying weights
            
            success = governance.cast_vote(proposal_id, voter, choice, weight)
            vote_str = "Yes" if choice else "No"
            print(f"  {voter}: {vote_str} (weight: {weight:.1f}) - {'✓' if success else '✗'}")
    
    # Finalize proposals
    print("\n--- Finalizing Proposals ---")
    for proposal_id in created_proposals[:2]:
        result = governance.finalize_proposal(proposal_id, threshold=50.0)
        print(f"\n{proposal_id}:")
        print(f"  Status: {result['status']}")
        print(f"  Yes: {result['tally']['yes']:.1f}, No: {result['tally']['no']:.1f}")
        print(f"  Yes Percentage: {result['tally']['yes_percentage']:.1f}%")
        print(f"  Passed: {result['passed']}")
        print(f"  {result['governance_message']}")
    
    # Execute passed proposal
    print("\n--- Executing Passed Proposal ---")
    if created_proposals:
        exec_result = governance.execute_proposal(created_proposals[0])
        if exec_result["success"]:
            print(f"  Executed: {exec_result['proposal_id']}")
            print(f"  🌟 {exec_result['divine_message']} 🌟")
    
    # Get governance statistics
    print("\n--- Governance Statistics ---")
    stats = governance.get_governance_stats()
    print(f"Total Proposals: {stats['total_proposals']}")
    print(f"Active Proposals: {stats['active_proposals']}")
    print(f"Total Votes Cast: {stats['total_votes_cast']}")
    print(f"Governance Score: {stats['governance_score']:.1f}/100")
    print(f"Participation Rate: {stats['participation_rate']:.1f}")
    print(f"Karmic Alignment: {stats['karmic_alignment']}")
    
    # Align with cosmic will
    print("\n--- Cosmic Alignment ---")
    alignment = governance.align_with_cosmic_will()
    print(f"Aligned: {alignment['aligned']}")
    print(f"Cosmic Alignment Score: {alignment['cosmic_alignment_score']:.2f}/100")
    print(f"Governance Health: {alignment['governance_health']:.1f}")
    print(f"🌟 {alignment['universal_blessing']} 🌟")
    
    print("\n--- Recommendations ---")
    for rec in alignment['recommendations']:
        print(f"  • {rec}")


if __name__ == "__main__":
    main()
