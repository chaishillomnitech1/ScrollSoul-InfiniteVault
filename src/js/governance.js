/**
 * src/js/governance.js
 * ScrollSoul-InfiniteVault — Universal Governance System (JavaScript)
 *
 * Democratic proposals with weighted karma voting, automatic execution,
 * and GoHighLevel pipeline stage synchronization per proposal lifecycle.
 */

'use strict';

const PROPOSAL_STATUS = Object.freeze({
  PENDING: 'pending',
  ACTIVE: 'active',
  PASSED: 'passed',
  REJECTED: 'rejected',
  EXECUTED: 'executed',
});

// ── Vote ──────────────────────────────────────────────────────────────────────

class Vote {
  constructor(voter, choice, weight = 1.0) {
    this.voter = voter;
    this.choice = choice; // true = yes, false = no
    this.weight = weight;
    this.timestamp = new Date().toISOString();
  }
  toString() { return `Vote(${this.voter}: ${this.choice ? 'Yes' : 'No'}, weight=${this.weight})`; }
}

// ── Proposal ──────────────────────────────────────────────────────────────────

class Proposal {
  constructor(proposalId, title, description, votingPeriodDays = 7) {
    this.proposalId = proposalId;
    this.title = title;
    this.description = description;
    this.createdAt = new Date().toISOString();
    const deadline = new Date();
    deadline.setDate(deadline.getDate() + votingPeriodDays);
    this.votingDeadline = deadline.toISOString();
    this.status = PROPOSAL_STATUS.ACTIVE;
    this.votes = [];
    this.executed = false;
  }

  addVote(vote) {
    if (new Date() > new Date(this.votingDeadline)) return false;
    if (this.votes.some(v => v.voter === vote.voter)) return false;
    this.votes.push(vote);
    return true;
  }

  tallyVotes() {
    const yes = this.votes.filter(v => v.choice).reduce((s, v) => s + v.weight, 0);
    const no = this.votes.filter(v => !v.choice).reduce((s, v) => s + v.weight, 0);
    const total = yes + no;
    return { yes, no, total, yesPercentage: total > 0 ? (yes / total) * 100 : 0 };
  }

  finalize(threshold = 50) {
    if (new Date() < new Date(this.votingDeadline)) return this.status;
    const { yesPercentage } = this.tallyVotes();
    this.status = yesPercentage >= threshold ? PROPOSAL_STATUS.PASSED : PROPOSAL_STATUS.REJECTED;
    return this.status;
  }

  toJSON() {
    return {
      proposalId: this.proposalId,
      title: this.title,
      description: this.description,
      status: this.status,
      createdAt: this.createdAt,
      votingDeadline: this.votingDeadline,
      voteCount: this.votes.length,
      tally: this.tallyVotes(),
      executed: this.executed,
    };
  }

  /** GHL pipeline stage name based on current status. */
  toGHLStage() {
    const map = {
      [PROPOSAL_STATUS.PENDING]: 'Proposal Submitted',
      [PROPOSAL_STATUS.ACTIVE]: 'Voting In Progress',
      [PROPOSAL_STATUS.PASSED]: 'Proposal Passed',
      [PROPOSAL_STATUS.REJECTED]: 'Proposal Rejected',
      [PROPOSAL_STATUS.EXECUTED]: 'Executed & Immortalized',
    };
    return map[this.status] || 'Active';
  }
}

// ── UniversalGovernance ───────────────────────────────────────────────────────

class UniversalGovernance {
  constructor() {
    this.proposals = new Map();
    this.proposalCounter = 0;
    this.governanceScore = 100.0;
    this.totalVotesCast = 0;
  }

  createProposal(title, description, votingPeriodDays = 7) {
    const id = `PROP-${String(this.proposalCounter).padStart(4, '0')}`;
    this.proposalCounter++;
    const proposal = new Proposal(id, title, description, votingPeriodDays);
    this.proposals.set(id, proposal);
    return proposal;
  }

  castVote(proposalId, voter, choice, weight = 1.0) {
    const proposal = this.proposals.get(proposalId);
    if (!proposal) return false;
    const vote = new Vote(voter, choice, weight);
    const success = proposal.addVote(vote);
    if (success) {
      this.totalVotesCast++;
      this.governanceScore = Math.min(100, this.governanceScore + 0.1);
    }
    return success;
  }

  finalizeProposal(proposalId, threshold = 50) {
    const proposal = this.proposals.get(proposalId);
    if (!proposal) return { success: false, error: 'Proposal not found' };
    const status = proposal.finalize(threshold);
    return {
      success: true,
      proposalId,
      status,
      tally: proposal.tallyVotes(),
      passed: status === PROPOSAL_STATUS.PASSED,
    };
  }

  executeProposal(proposalId) {
    const proposal = this.proposals.get(proposalId);
    if (!proposal) return { success: false, error: 'Proposal not found' };
    if (proposal.status !== PROPOSAL_STATUS.PASSED) return { success: false, error: 'Proposal has not passed' };
    if (proposal.executed) return { success: false, error: 'Already executed' };
    proposal.executed = true;
    proposal.status = PROPOSAL_STATUS.EXECUTED;
    return { success: true, proposalId, executed: true, divineMessage: 'ALLĀHU AKBAR! The will of the ScrollVerse is manifest!' };
  }

  getActiveProposals() {
    const now = new Date();
    return [...this.proposals.values()]
      .filter(p => p.status === PROPOSAL_STATUS.ACTIVE && new Date(p.votingDeadline) > now)
      .map(p => p.toJSON());
  }

  getGovernanceStats() {
    const statusCounts = Object.values(PROPOSAL_STATUS).reduce((acc, s) => {
      acc[s] = [...this.proposals.values()].filter(p => p.status === s).length;
      return acc;
    }, {});
    return {
      totalProposals: this.proposals.size,
      activeProposals: this.getActiveProposals().length,
      totalVotesCast: this.totalVotesCast,
      governanceScore: parseFloat(this.governanceScore.toFixed(2)),
      statusBreakdown: statusCounts,
      karmaAlignment: this.governanceScore > 80 ? 'Excellent' : 'Good',
    };
  }

  alignWithCosmicWill() {
    const stats = this.getGovernanceStats();
    const cosmicAlignment = Math.min(100,
      stats.governanceScore * 0.5 +
      (stats.totalVotesCast / (stats.totalProposals || 1)) * 30 +
      stats.totalProposals * 2,
    );
    return {
      aligned: cosmicAlignment > 50,
      cosmicAlignmentScore: parseFloat(cosmicAlignment.toFixed(2)),
      governanceHealth: stats.governanceScore,
      universalBlessing: 'WALAHI! The governance flows with divine wisdom!',
    };
  }

  /** Emit GHL-compatible payloads for all proposals (pipeline sync). */
  toGHLPayload(pipelineId = '') {
    return [...this.proposals.values()].map(p => {
      const tally = p.tallyVotes();
      return {
        proposalId: p.proposalId,
        title: p.title,
        status: p.status,
        stage: p.toGHLStage(),
        tally,
        pipelineId,
        opportunityName: `[Governance] ${p.title}`,
        monetaryValue: tally.yes * 100,
        note: `[Governance] ${p.proposalId} | Status: ${p.status} | Yes: ${tally.yes.toFixed(0)} | Deadline: ${p.votingDeadline}`,
      };
    });
  }
}

module.exports = { Vote, Proposal, UniversalGovernance, PROPOSAL_STATUS };
