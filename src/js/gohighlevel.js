/**
 * src/js/gohighlevel.js
 * ScrollSoul-InfiniteVault — GoHighLevel JavaScript API Client
 *
 * Full agency + sub-account client for the GoHighLevel REST API.
 * Uses DinoRunner for automatic retry and circuit-breaker protection.
 *
 * Environment variables:
 *   GHL_API_KEY        — Location or Agency API key
 *   GHL_LOCATION_ID    — Default sub-account Location ID
 *   GHL_COMPANY_ID     — Agency/Company ID
 */

'use strict';

const https = require('https');
const http = require('http');
const { URL } = require('url');
const { DinoRunner } = require('../../dino_runner');

const GHL_V1_BASE = 'https://rest.gohighlevel.com/v1';
const GHL_V2_BASE = 'https://services.leadconnectorhq.com';
const GHL_V2_VERSION = '2021-07-28';

// ── Low-level HTTP helper ─────────────────────────────────────────────────────

function httpRequest(method, rawUrl, headers = {}, body = null) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(rawUrl);
    const isHttps = parsed.protocol === 'https:';
    const lib = isHttps ? https : http;

    const options = {
      hostname: parsed.hostname,
      port: parsed.port || (isHttps ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: method.toUpperCase(),
      headers: { 'Content-Type': 'application/json', ...headers },
    };

    let payload = null;
    if (body) {
      payload = JSON.stringify(body);
      options.headers['Content-Length'] = Buffer.byteLength(payload);
    }

    const req = lib.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try { resolve(JSON.parse(data)); } catch (parseErr) {
            console.warn(`[GHL] JSON parse error (status ${res.statusCode}): ${parseErr.message}`);
            resolve({});
          }
        } else {
          const err = new Error(`GHL HTTP ${res.statusCode}: ${data.slice(0, 200)}`);
          err.statusCode = res.statusCode;
          reject(err);
        }
      });
    });

    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

// ── GoHighLevelClient ─────────────────────────────────────────────────────────

class GoHighLevelClient {
  /**
   * @param {object} [opts]
   * @param {string} [opts.apiKey]
   * @param {string} [opts.locationId]
   * @param {string} [opts.companyId]
   * @param {boolean} [opts.useV2=false]
   * @param {number}  [opts.maxRetries=5]
   */
  constructor({
    apiKey,
    locationId,
    companyId,
    useV2 = false,
    maxRetries = 5,
  } = {}) {
    this.apiKey = apiKey || process.env.GHL_API_KEY || '';
    this.locationId = locationId || process.env.GHL_LOCATION_ID || '';
    this.companyId = companyId || process.env.GHL_COMPANY_ID || '';
    this.useV2 = useV2;
    this.baseUrl = useV2 ? GHL_V2_BASE : GHL_V1_BASE;
    this.runner = new DinoRunner({ maxRetries, verbose: false });
  }

  _headers(locationOverride) {
    const headers = { Authorization: `Bearer ${this.apiKey}` };
    if (this.useV2) headers['Version'] = GHL_V2_VERSION;
    const loc = locationOverride || this.locationId;
    if (loc) headers['Location'] = loc;
    return headers;
  }

  _url(endpoint, params = {}) {
    const url = new URL(`${this.baseUrl}${endpoint}`);
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    }
    return url.toString();
  }

  async request(method, endpoint, { locationId, params, body } = {}) {
    const url = this._url(endpoint, params || {});
    const headers = this._headers(locationId);
    return this.runner.run(
      () => httpRequest(method, url, headers, body || null),
      { name: `GHL ${method} ${endpoint}` },
    );
  }

  get(endpoint, opts = {}) { return this.request('GET', endpoint, opts); }
  post(endpoint, opts = {}) { return this.request('POST', endpoint, opts); }
  put(endpoint, opts = {}) { return this.request('PUT', endpoint, opts); }
  delete(endpoint, opts = {}) { return this.request('DELETE', endpoint, opts); }

  getStats() { return this.runner.getStatus(); }
}

// ── SubAccountManager ─────────────────────────────────────────────────────────

class SubAccountManager {
  constructor(client) {
    this.client = client;
    this._cache = {};
  }

  async listLocations() {
    const resp = await this.client.get('/locations/', {
      params: { companyId: this.client.companyId },
    });
    const locations = resp.locations || [];
    for (const loc of locations) this._cache[loc.id] = loc;
    return locations;
  }

  async getLocation(locationId) {
    const resp = await this.client.get(`/locations/${locationId}`);
    const loc = resp.location || resp;
    this._cache[locationId] = loc;
    return loc;
  }

  async createLocation(payload) {
    const resp = await this.client.post('/locations/', {
      body: { companyId: this.client.companyId, ...payload },
    });
    return resp.location || resp;
  }

  async updateLocation(locationId, updates) {
    const resp = await this.client.put(`/locations/${locationId}`, { body: updates });
    return resp.location || resp;
  }

  async deleteLocation(locationId) {
    return this.client.delete(`/locations/${locationId}`);
  }

  async introspectLocation(locationId) {
    const [location, contacts, pipelines, campaigns, conversations, tags, customValues, hooks] =
      await Promise.allSettled([
        this.getLocation(locationId),
        this.client.get('/contacts/', { locationId, params: { limit: 100 } }),
        this.client.get('/pipelines/', { locationId }),
        this.client.get('/campaigns/', { locationId }),
        this.client.get('/conversations/', { locationId, params: { limit: 20 } }),
        this.client.get('/tags/', { locationId }),
        this.client.get('/custom-values/', { locationId }),
        this.client.get('/hooks/', { locationId }),
      ]);

    const loc = location.status === 'fulfilled' ? location.value : {};
    const contactList = contacts.status === 'fulfilled' ? (contacts.value.contacts || []) : [];
    const pipelineList = pipelines.status === 'fulfilled' ? (pipelines.value.pipelines || []) : [];
    const campaignList = campaigns.status === 'fulfilled' ? (campaigns.value.campaigns || []) : [];
    const convList = conversations.status === 'fulfilled' ? (conversations.value.conversations || []) : [];
    const tagList = tags.status === 'fulfilled' ? (tags.value.tags || []) : [];
    const cvList = customValues.status === 'fulfilled' ? (customValues.value.customValues || []) : [];
    const hookList = hooks.status === 'fulfilled' ? (hooks.value.webhooks || hooks.value.hooks || []) : [];

    return {
      locationId,
      locationName: loc.name,
      email: loc.email,
      timezone: loc.timezone,
      contactCount: contactList.length,
      contactsSample: contactList.slice(0, 5),
      pipelineCount: pipelineList.length,
      pipelines: pipelineList,
      campaignCount: campaignList.length,
      campaigns: campaignList.slice(0, 10),
      conversationCount: convList.length,
      tagCount: tagList.length,
      tags: tagList.map(t => t.name),
      customValuesCount: cvList.length,
      webhookCount: hookList.length,
      introspectedAt: new Date().toISOString(),
      karmaScore: Math.min(100, contactList.length * 0.1 + pipelineList.length * 5 + campaignList.length * 3),
    };
  }

  async introspectAllLocations() {
    const locations = await this.listLocations();
    const results = await Promise.allSettled(
      locations.map(loc => this.introspectLocation(loc.id))
    );

    let totalContacts = 0;
    let totalCampaigns = 0;
    const locationResults = results.map((r, i) => {
      if (r.status === 'fulfilled') {
        totalContacts += r.value.contactCount || 0;
        totalCampaigns += r.value.campaignCount || 0;
        return r.value;
      }
      return { locationId: locations[i].id, error: r.reason?.message };
    });

    return {
      totalLocations: locations.length,
      totalContacts,
      totalCampaigns,
      locations: locationResults,
      agencyKarmaScore: Math.min(100, locations.length * 10 + totalContacts * 0.05),
      executedAt: new Date().toISOString(),
      divineMessage: 'WALAHI! Every sub-account deep-dived and immortalized!',
    };
  }
}

// ── ContactManager ────────────────────────────────────────────────────────────

class ContactManager {
  constructor(client) { this.client = client; }

  async createContact(data, locationId) {
    const resp = await this.client.post('/contacts/', { locationId, body: data });
    return resp.contact || resp;
  }

  async searchContacts(query, locationId, limit = 20) {
    const resp = await this.client.get('/contacts/', {
      locationId,
      params: { query, limit },
    });
    return resp.contacts || [];
  }

  async updateContact(contactId, updates, locationId) {
    const resp = await this.client.put(`/contacts/${contactId}`, { locationId, body: updates });
    return resp.contact || resp;
  }

  async deleteContact(contactId, locationId) {
    return this.client.delete(`/contacts/${contactId}`, { locationId });
  }

  async addNote(contactId, body, locationId) {
    return this.client.post(`/contacts/${contactId}/notes/`, { locationId, body: { body } });
  }

  async addTags(contactId, tags, locationId) {
    return this.client.post(`/contacts/${contactId}/tags/`, { locationId, body: { tags } });
  }

  async addTask(contactId, title, dueDate, locationId) {
    const body = { title, status: 'incompleted' };
    if (dueDate) body.dueDate = dueDate;
    return this.client.post(`/contacts/${contactId}/tasks/`, { locationId, body });
  }

  async upsertContact(email, data = {}, locationId) {
    const existing = await this.searchContacts(email, locationId, 1);
    if (existing.length) {
      return this.updateContact(existing[0].id, data, locationId);
    }
    return this.createContact({ email, ...data }, locationId);
  }
}

// ── PipelineManager ───────────────────────────────────────────────────────────

class PipelineManager {
  constructor(client) { this.client = client; }

  async listPipelines(locationId) {
    const resp = await this.client.get('/pipelines/', { locationId });
    return resp.pipelines || [];
  }

  async createOpportunity(data, locationId) {
    const resp = await this.client.post('/opportunities/', { locationId, body: data });
    return resp.opportunity || resp;
  }

  async updateOpportunity(opportunityId, updates, locationId) {
    const resp = await this.client.put(`/opportunities/${opportunityId}`, { locationId, body: updates });
    return resp.opportunity || resp;
  }

  async getOpportunities(pipelineId, locationId, limit = 100) {
    const resp = await this.client.get(`/pipelines/${pipelineId}/opportunities/`, {
      locationId,
      params: { limit },
    });
    return resp.opportunities || [];
  }
}

// ── CampaignManager ───────────────────────────────────────────────────────────

class CampaignManager {
  constructor(client) { this.client = client; }

  async listCampaigns(locationId) {
    const resp = await this.client.get('/campaigns/', { locationId });
    return resp.campaigns || [];
  }

  async addContactToCampaign(campaignId, contactId, locationId) {
    return this.client.post(`/campaigns/${campaignId}/contacts/`, {
      locationId,
      body: { contactId },
    });
  }

  async triggerForContacts(campaignId, contactIds, locationId) {
    const results = await Promise.allSettled(
      contactIds.map(id => this.addContactToCampaign(campaignId, id, locationId))
    );
    const successes = results.filter(r => r.status === 'fulfilled').length;
    return {
      campaignId,
      targeted: contactIds.length,
      successes,
      failures: contactIds.length - successes,
    };
  }
}

// ── ConversationManager ───────────────────────────────────────────────────────

class ConversationManager {
  constructor(client) { this.client = client; }

  async listConversations(locationId, limit = 20) {
    const resp = await this.client.get('/conversations/', { locationId, params: { limit } });
    return resp.conversations || [];
  }

  async sendSMS(contactId, message, locationId) {
    return this.client.post('/conversations/messages/', {
      locationId,
      body: { type: 'SMS', contactId, message },
    });
  }

  async sendEmail(contactId, subject, html, locationId) {
    return this.client.post('/conversations/messages/', {
      locationId,
      body: { type: 'Email', contactId, subject, html },
    });
  }

  async broadcastSMS(contactIds, message, locationId) {
    const results = await Promise.allSettled(
      contactIds.map(id => this.sendSMS(id, message, locationId))
    );
    const successes = results.filter(r => r.status === 'fulfilled').length;
    return { total: contactIds.length, successes, failures: contactIds.length - successes };
  }
}

// ── WebhookHandler ────────────────────────────────────────────────────────────

class WebhookHandler {
  static SUPPORTED_EVENTS = [
    'ContactCreate', 'ContactUpdate', 'ContactDelete',
    'OpportunityCreate', 'OpportunityUpdate', 'OpportunityDelete',
    'AppointmentCreate', 'AppointmentUpdate',
    'InboundMessage', 'OutboundMessage',
    'FormSubmission', 'NoteCreate', 'TaskCreate',
  ];

  constructor(client) {
    this.client = client;
    this._handlers = {};
  }

  async registerWebhook(url, events, locationId) {
    return this.client.post('/hooks/', {
      locationId,
      body: { url, events: events || WebhookHandler.SUPPORTED_EVENTS },
    });
  }

  async listWebhooks(locationId) {
    const resp = await this.client.get('/hooks/', { locationId });
    return resp.webhooks || resp.hooks || [];
  }

  async deleteWebhook(hookId, locationId) {
    return this.client.delete(`/hooks/${hookId}`, { locationId });
  }

  on(event, handler) {
    if (!this._handlers[event]) this._handlers[event] = [];
    this._handlers[event].push(handler);
  }

  dispatch(payload) {
    const event = payload.type || payload.event || 'unknown';
    const handlers = this._handlers[event] || [];
    const results = handlers.map(h => {
      try { h(payload); return { handler: h.name, success: true }; }
      catch (err) { return { handler: h.name, success: false, error: err.message }; }
    });
    return { event, handlersCalled: handlers.length, results };
  }
}

// ── CustomFieldManager ────────────────────────────────────────────────────────

class CustomFieldManager {
  constructor(client) { this.client = client; }

  async listCustomValues(locationId) {
    const resp = await this.client.get('/custom-values/', { locationId });
    return resp.customValues || [];
  }

  async createCustomValue(name, value, locationId) {
    const resp = await this.client.post('/custom-values/', { locationId, body: { name, value } });
    return resp.customValue || resp;
  }

  async updateCustomValue(customValueId, value, locationId) {
    const resp = await this.client.put(`/custom-values/${customValueId}`, {
      locationId,
      body: { value },
    });
    return resp.customValue || resp;
  }

  async upsertCustomValue(name, value, locationId) {
    const existing = await this.listCustomValues(locationId);
    const found = existing.find(cv => cv.name === name);
    if (found) return this.updateCustomValue(found.id, value, locationId);
    return this.createCustomValue(name, value, locationId);
  }
}

// ── ScrollSoulGHLBridge (JS) ──────────────────────────────────────────────────

class ScrollSoulGHLBridge {
  /**
   * Master JS orchestrator — wires all ScrollSoul JS modules into GHL.
   * @param {object} [opts] - Passed to GoHighLevelClient
   */
  constructor(opts = {}) {
    this.client = new GoHighLevelClient(opts);
    this.subAccounts = new SubAccountManager(this.client);
    this.contacts = new ContactManager(this.client);
    this.pipelines = new PipelineManager(this.client);
    this.campaigns = new CampaignManager(this.client);
    this.conversations = new ConversationManager(this.client);
    this.webhooks = new WebhookHandler(this.client);
    this.customFields = new CustomFieldManager(this.client);
    this.runner = new DinoRunner({ maxRetries: 5, verbose: false });
  }

  /** Sync scaler GHL payload (from MultiLayerScaler.toGHLPayload()) to a location. */
  async syncScalingMetrics(ghlPayload, locationId) {
    const loc = locationId || this.client.locationId;
    const results = await Promise.allSettled(
      Object.entries(ghlPayload).map(([name, value]) =>
        this.customFields.upsertCustomValue(name, String(value), loc)
      )
    );
    return {
      synced: results.filter(r => r.status === 'fulfilled').length,
      failed: results.filter(r => r.status === 'rejected').length,
      locationId: loc,
    };
  }

  /** Sync royalty GHL payload (from SpotifyRoyaltyHarvester.toGHLPayload()) to a location. */
  async syncRoyaltyArtists(ghlPayload, locationId) {
    const loc = locationId || this.client.locationId;
    const results = await Promise.allSettled(
      ghlPayload.map(async artist => {
        const contact = await this.contacts.upsertContact(
          artist.email,
          {
            firstName: artist.artist.split(' ')[0],
            lastName: artist.artist.split(' ').slice(1).join(' '),
            tags: artist.tags,
            source: 'ScrollSoul-Royalty',
          },
          loc,
        );
        const contactId = contact.id || contact.contact?.id;
        if (contactId) {
          await this.contacts.addNote(contactId, artist.note, loc);
        }
        return { artist: artist.artist, contactId };
      })
    );
    return {
      synced: results.filter(r => r.status === 'fulfilled').length,
      failed: results.filter(r => r.status === 'rejected').length,
      locationId: loc,
    };
  }

  /** Trigger GHL campaign if AI engine has reached enlightenment. */
  async triggerAICampaign(ghlPayload, campaignId, contactIds, locationId) {
    if (!ghlPayload.shouldTrigger) {
      return { triggered: false, reason: 'AI engine has not reached enlightenment', ...ghlPayload };
    }
    const result = await this.campaigns.triggerForContacts(
      campaignId,
      contactIds,
      locationId || this.client.locationId,
    );
    return { triggered: true, campaign: result, enlightenment: ghlPayload.enlightenment };
  }

  /** Execute full sync across ALL sub-account locations via DinoRunner. */
  async executeFullSyncAcrossAllLocations({ scalerPayload, royaltyPayload, aiPayload, campaignId, contactIds } = {}) {
    const locations = await this.subAccounts.listLocations();
    const locationIds = locations.map(l => l.id);

    return this.runner.executeAcrossLocations(locationIds, async locId => {
      const result = { locationId: locId };
      if (scalerPayload) result.scaling = await this.syncScalingMetrics(scalerPayload, locId);
      if (royaltyPayload) result.royalty = await this.syncRoyaltyArtists(royaltyPayload, locId);
      if (aiPayload && campaignId && contactIds) {
        result.aiCampaign = await this.triggerAICampaign(aiPayload, campaignId, contactIds, locId);
      }
      return result;
    });
  }

  getBridgeStatus() {
    return {
      bridge: 'ScrollSoul-GHL-Bridge-JS',
      version: '2.0.0',
      locationId: this.client.locationId,
      companyId: this.client.companyId,
      clientStats: this.client.getStats(),
      modulesConnected: ['MultiLayerScaler', 'SpotifyRoyaltyHarvester', 'RecursiveAIEngine'],
      infiniteExecution: true,
      karmaAligned: true,
      divineMessage: 'ALLĀHU AKBAR! JS bridge fully immortalized in GoHighLevel!',
    };
  }
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = {
  GoHighLevelClient,
  SubAccountManager,
  ContactManager,
  PipelineManager,
  CampaignManager,
  ConversationManager,
  WebhookHandler,
  CustomFieldManager,
  ScrollSoulGHLBridge,
};
