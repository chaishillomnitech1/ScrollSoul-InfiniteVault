"""
GoHighLevel Integration — ScrollSoul-InfiniteVault
ALLĀHU AKBAR! Full agency-level sub-account orchestration immortalized.

Provides complete coverage of the GoHighLevel API:
  - Agency sub-account (Location) management
  - Contacts, pipelines, opportunities
  - Campaigns, conversations, messaging
  - Webhooks, calendars, custom fields, tags
  - ScrollSoulGHLBridge — wires every ScrollSoul module into GHL seamlessly

Environment variables:
  GHL_API_KEY        — Location or Agency API key (V1)
  GHL_AGENCY_API_KEY — Agency-level API key for sub-account management
  GHL_LOCATION_ID    — Default sub-account Location ID
  GHL_COMPANY_ID     — Agency/Company ID
"""

import os
import time
import logging
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── API constants ────────────────────────────────────────────────────────────
GHL_V1_BASE = "https://rest.gohighlevel.com/v1"
GHL_V2_BASE = "https://services.leadconnectorhq.com"
GHL_V2_VERSION = "2021-07-28"

_DEFAULT_RETRY_ATTEMPTS = 5
_DEFAULT_BACKOFF_BASE_SECONDS = 1.5  # DinoRunner-style exponential backoff

# Karma scoring weights
_LOCATION_KARMA_CONTACT_WEIGHT = 0.1
_LOCATION_KARMA_PIPELINE_WEIGHT = 5.0
_LOCATION_KARMA_CAMPAIGN_WEIGHT = 3.0
_AGENCY_KARMA_LOCATION_WEIGHT = 10.0
_AGENCY_KARMA_CONTACT_WEIGHT = 0.05


# ─── Base Client ─────────────────────────────────────────────────────────────

def _make_scrollsoul_email(name: str, domain_suffix: str = "scrollsoul") -> str:
    """Generate a consistent internal email address for a named entity."""
    local = name.lower().replace(" ", ".").replace("_", ".")
    return f"{local}@{domain_suffix}"


class GoHighLevelClient:
    """
    Base GoHighLevel API client.

    Supports both V1 (API-key) and V2 (Bearer/OAuth) endpoints with
    automatic DinoRunner-style exponential-backoff retry so the integration
    *keeps running* through rate-limits and transient errors.

    Args:
        api_key:          Location or Agency API key.
        location_id:      Default Location/sub-account ID.
        company_id:       Agency Company ID (required for agency-level calls).
        use_v2:           Route requests through the V2 base URL when True.
        retry_attempts:   Maximum retry attempts on 429 / 5xx.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        location_id: Optional[str] = None,
        company_id: Optional[str] = None,
        use_v2: bool = False,
        retry_attempts: int = _DEFAULT_RETRY_ATTEMPTS,
    ):
        self.api_key = api_key or os.getenv("GHL_API_KEY", "")
        self.location_id = location_id or os.getenv("GHL_LOCATION_ID", "")
        self.company_id = company_id or os.getenv("GHL_COMPANY_ID", "")
        self.use_v2 = use_v2
        self.retry_attempts = retry_attempts
        self.base_url = GHL_V2_BASE if use_v2 else GHL_V1_BASE
        self._request_count = 0
        self._error_count = 0

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _headers(self, location_override: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.use_v2:
            headers["Version"] = GHL_V2_VERSION
        loc = location_override or self.location_id
        if loc:
            headers["Location"] = loc
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        location_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self._headers(location_id)
        last_error: Exception = Exception("No attempts made")

        for attempt in range(self.retry_attempts):
            try:
                self._request_count += 1
                resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)

                if resp.status_code == 429:
                    wait = _DEFAULT_BACKOFF_BASE_SECONDS ** attempt
                    logger.warning("GHL rate-limited — DinoRunner retry %d in %.1fs", attempt + 1, wait)
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                return resp.json() if resp.content else {}

            except requests.exceptions.HTTPError as exc:
                self._error_count += 1
                if resp.status_code < 500:
                    raise
                last_error = exc
                wait = _DEFAULT_BACKOFF_BASE_SECONDS ** attempt
                logger.warning("GHL HTTP %d — retry %d in %.1fs", resp.status_code, attempt + 1, wait)
                time.sleep(wait)

            except requests.exceptions.RequestException as exc:
                self._error_count += 1
                last_error = exc
                wait = _DEFAULT_BACKOFF_BASE_SECONDS ** attempt
                logger.warning("GHL request error — retry %d in %.1fs: %s", attempt + 1, wait, exc)
                time.sleep(wait)

        raise last_error

    def get(self, endpoint: str, location_id: Optional[str] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, location_id=location_id, params=params or {})

    def post(self, endpoint: str, location_id: Optional[str] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, location_id=location_id, json=data or {})

    def put(self, endpoint: str, location_id: Optional[str] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PUT", endpoint, location_id=location_id, json=data or {})

    def delete(self, endpoint: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self._request("DELETE", endpoint, location_id=location_id)

    def get_client_stats(self) -> Dict[str, Any]:
        return {
            "total_requests": self._request_count,
            "total_errors": self._error_count,
            "success_rate": (
                ((self._request_count - self._error_count) / self._request_count * 100)
                if self._request_count else 100.0
            ),
        }


# ─── Sub-Account (Location) Manager ──────────────────────────────────────────

class SubAccountManager:
    """
    Full agency-level sub-account orchestrator.

    Deep-dives every Location: introspects contacts, pipelines, campaigns,
    conversations, tags, and custom fields — then executes cross-location
    operations seamlessly.
    """

    def __init__(self, client: GoHighLevelClient):
        self.client = client
        self._location_cache: Dict[str, Dict] = {}

    # ── Location CRUD ─────────────────────────────────────────────────────────

    def list_locations(self) -> List[Dict[str, Any]]:
        """List all sub-account locations under the agency."""
        resp = self.client.get("/locations/", params={"companyId": self.client.company_id})
        locations = resp.get("locations", [])
        for loc in locations:
            self._location_cache[loc.get("id", "")] = loc
        logger.info("Found %d sub-account locations", len(locations))
        return locations

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get full details for a single sub-account."""
        resp = self.client.get(f"/locations/{location_id}")
        location = resp.get("location", resp)
        self._location_cache[location_id] = location
        return location

    def create_location(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: str = "US",
        timezone: str = "America/Chicago",
        website: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new sub-account location."""
        payload: Dict[str, Any] = {
            "companyId": self.client.company_id,
            "name": name,
            "email": email,
            "country": country,
            "timezone": timezone,
        }
        if phone:
            payload["phone"] = phone
        if address:
            payload["address"] = address
        if city:
            payload["city"] = city
        if state:
            payload["state"] = state
        if website:
            payload["website"] = website
        payload.update(kwargs)

        resp = self.client.post("/locations/", data=payload)
        location = resp.get("location", resp)
        logger.info("Created sub-account: %s (%s)", name, location.get("id"))
        return location

    def update_location(self, location_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing sub-account."""
        resp = self.client.put(f"/locations/{location_id}", data=updates)
        return resp.get("location", resp)

    def delete_location(self, location_id: str) -> Dict[str, Any]:
        """Delete a sub-account location."""
        return self.client.delete(f"/locations/{location_id}")

    # ── Deep introspection ────────────────────────────────────────────────────

    def introspect_location(self, location_id: str) -> Dict[str, Any]:
        """
        Deep-dive a single sub-account: pull contacts, pipelines, campaigns,
        conversations, custom fields, tags, and snapshot stats.
        """
        logger.info("Deep-diving sub-account: %s", location_id)
        location = self.get_location(location_id)

        # Gather all data concurrently via sequential calls
        contacts_resp = self.client.get("/contacts/", location_id=location_id, params={"limit": 100})
        pipelines_resp = self.client.get("/pipelines/", location_id=location_id)
        campaigns_resp = self.client.get("/campaigns/", location_id=location_id)
        conversations_resp = self.client.get("/conversations/", location_id=location_id, params={"limit": 20})
        tags_resp = self.client.get("/tags/", location_id=location_id)
        custom_values_resp = self.client.get("/custom-values/", location_id=location_id)
        hooks_resp = self.client.get("/hooks/", location_id=location_id)

        contacts = contacts_resp.get("contacts", [])
        pipelines = pipelines_resp.get("pipelines", [])
        campaigns = campaigns_resp.get("campaigns", [])
        conversations = conversations_resp.get("conversations", [])
        tags = tags_resp.get("tags", [])
        custom_values = custom_values_resp.get("customValues", [])
        hooks = hooks_resp.get("webhooks", hooks_resp.get("hooks", []))

        # Opportunity counts per pipeline
        pipeline_stats = []
        for pipeline in pipelines:
            pid = pipeline.get("id")
            opps_resp = self.client.get(
                f"/pipelines/{pid}/opportunities/",
                location_id=location_id,
                params={"limit": 100},
            )
            opps = opps_resp.get("opportunities", [])
            pipeline_stats.append({
                "pipeline_id": pid,
                "name": pipeline.get("name"),
                "stages": pipeline.get("stages", []),
                "opportunity_count": len(opps),
                "opportunities": opps[:10],
            })

        return {
            "location_id": location_id,
            "location_name": location.get("name"),
            "email": location.get("email"),
            "phone": location.get("phone"),
            "timezone": location.get("timezone"),
            "country": location.get("country"),
            "contact_count": len(contacts),
            "contacts_sample": contacts[:5],
            "pipeline_count": len(pipelines),
            "pipelines": pipeline_stats,
            "campaign_count": len(campaigns),
            "campaigns": campaigns[:10],
            "conversation_count": len(conversations),
            "tag_count": len(tags),
            "tags": [t.get("name") for t in tags],
            "custom_values_count": len(custom_values),
            "webhook_count": len(hooks),
            "introspected_at": datetime.now().isoformat(),
            "karma_score": min(100.0,
                               len(contacts) * _LOCATION_KARMA_CONTACT_WEIGHT +
                               len(pipelines) * _LOCATION_KARMA_PIPELINE_WEIGHT +
                               len(campaigns) * _LOCATION_KARMA_CAMPAIGN_WEIGHT),
        }

    def introspect_all_locations(self) -> Dict[str, Any]:
        """
        Deep-dive EVERY sub-account under the agency simultaneously.
        Returns aggregated stats + per-location introspection.
        """
        locations = self.list_locations()
        results = []
        total_contacts = 0
        total_opportunities = 0
        total_campaigns = 0

        for loc in locations:
            loc_id = loc.get("id")
            try:
                data = self.introspect_location(loc_id)
                results.append(data)
                total_contacts += data.get("contact_count", 0)
                total_opportunities += sum(
                    p.get("opportunity_count", 0) for p in data.get("pipelines", [])
                )
                total_campaigns += data.get("campaign_count", 0)
            except Exception as exc:
                logger.error("Failed to introspect location %s: %s", loc_id, exc)
                results.append({"location_id": loc_id, "error": str(exc)})

        return {
            "total_locations": len(locations),
            "total_contacts": total_contacts,
            "total_opportunities": total_opportunities,
            "total_campaigns": total_campaigns,
            "locations": results,
            "agency_karma_score": min(100.0,
                                      len(locations) * _AGENCY_KARMA_LOCATION_WEIGHT +
                                      total_contacts * _AGENCY_KARMA_CONTACT_WEIGHT),
            "executed_at": datetime.now().isoformat(),
            "divine_message": "WALAHI! Every sub-account has been deep-dived and immortalized!",
        }

    def execute_across_all_locations(
        self,
        action: Callable[[str], Dict[str, Any]],
        location_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute any callable across all (or a subset of) sub-accounts.

        Args:
            action:       Function receiving location_id, returning a result dict.
            location_ids: Specific location IDs to target; defaults to all.

        Returns:
            Aggregated results with per-location outcomes.
        """
        if location_ids is None:
            locations = self.list_locations()
            location_ids = [loc.get("id") for loc in locations]

        results = {}
        successes = 0
        failures = 0

        for loc_id in location_ids:
            try:
                results[loc_id] = action(loc_id)
                successes += 1
            except Exception as exc:
                logger.error("Action failed for location %s: %s", loc_id, exc)
                results[loc_id] = {"error": str(exc)}
                failures += 1

        return {
            "executed": len(location_ids),
            "successes": successes,
            "failures": failures,
            "results": results,
            "execution_rate": (successes / len(location_ids) * 100) if location_ids else 0,
            "timestamp": datetime.now().isoformat(),
        }


# ─── Contact Manager ──────────────────────────────────────────────────────────

class ContactManager:
    """CRUD + tagging, notes, and tasks for GHL contacts across sub-accounts."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def create_contact(
        self,
        first_name: str,
        last_name: str = "",
        email: str = "",
        phone: str = "",
        tags: Optional[List[str]] = None,
        custom_fields: Optional[List[Dict]] = None,
        source: str = "ScrollSoul-InfiniteVault",
        location_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "source": source,
        }
        if tags:
            payload["tags"] = tags
        if custom_fields:
            payload["customField"] = custom_fields
        payload.update(kwargs)
        resp = self.client.post("/contacts/", location_id=location_id, data=payload)
        contact = resp.get("contact", resp)
        logger.info("Created contact: %s %s (%s)", first_name, last_name, contact.get("id"))
        return contact

    def get_contact(self, contact_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.get(f"/contacts/{contact_id}", location_id=location_id)

    def search_contacts(
        self,
        query: str,
        location_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        resp = self.client.get(
            "/contacts/",
            location_id=location_id,
            params={"query": query, "limit": limit},
        )
        return resp.get("contacts", [])

    def update_contact(
        self,
        contact_id: str,
        updates: Dict[str, Any],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        resp = self.client.put(f"/contacts/{contact_id}", location_id=location_id, data=updates)
        return resp.get("contact", resp)

    def delete_contact(self, contact_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.delete(f"/contacts/{contact_id}", location_id=location_id)

    def add_tags(
        self,
        contact_id: str,
        tags: List[str],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.client.post(
            f"/contacts/{contact_id}/tags/",
            location_id=location_id,
            data={"tags": tags},
        )

    def remove_tags(
        self,
        contact_id: str,
        tags: List[str],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.client.delete(f"/contacts/{contact_id}/tags/", location_id=location_id)

    def add_note(
        self,
        contact_id: str,
        body: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.client.post(
            f"/contacts/{contact_id}/notes/",
            location_id=location_id,
            data={"body": body},
        )

    def add_task(
        self,
        contact_id: str,
        title: str,
        due_date: Optional[str] = None,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"title": title, "status": "incompleted"}
        if due_date:
            payload["dueDate"] = due_date
        return self.client.post(
            f"/contacts/{contact_id}/tasks/",
            location_id=location_id,
            data=payload,
        )

    def upsert_contact(
        self,
        email: str,
        first_name: str = "",
        last_name: str = "",
        phone: str = "",
        tags: Optional[List[str]] = None,
        location_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Search for existing contact by email, create if not found."""
        existing = self.search_contacts(email, location_id=location_id, limit=1)
        if existing:
            contact_id = existing[0].get("id")
            return self.update_contact(contact_id, {"firstName": first_name, "lastName": last_name, **kwargs}, location_id=location_id)
        return self.create_contact(first_name, last_name, email, phone, tags, location_id=location_id, **kwargs)


# ─── Pipeline Manager ─────────────────────────────────────────────────────────

class PipelineManager:
    """Pipelines, opportunities, and stage transitions across sub-accounts."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_pipelines(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/pipelines/", location_id=location_id)
        return resp.get("pipelines", [])

    def create_opportunity(
        self,
        pipeline_id: str,
        name: str,
        contact_id: str,
        stage_id: str = "",
        monetary_value: float = 0.0,
        status: str = "open",
        location_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "pipelineId": pipeline_id,
            "name": name,
            "contactId": contact_id,
            "status": status,
            "monetaryValue": monetary_value,
        }
        if stage_id:
            payload["pipelineStageId"] = stage_id
        payload.update(kwargs)
        resp = self.client.post("/opportunities/", location_id=location_id, data=payload)
        opp = resp.get("opportunity", resp)
        logger.info("Created opportunity: %s (%s) — $%.2f", name, opp.get("id"), monetary_value)
        return opp

    def update_opportunity(
        self,
        opportunity_id: str,
        updates: Dict[str, Any],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        resp = self.client.put(f"/opportunities/{opportunity_id}", location_id=location_id, data=updates)
        return resp.get("opportunity", resp)

    def move_stage(
        self,
        opportunity_id: str,
        stage_id: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.update_opportunity(opportunity_id, {"pipelineStageId": stage_id}, location_id=location_id)

    def get_opportunities(
        self,
        pipeline_id: str,
        location_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        resp = self.client.get(
            f"/pipelines/{pipeline_id}/opportunities/",
            location_id=location_id,
            params={"limit": limit},
        )
        return resp.get("opportunities", [])

    def delete_opportunity(self, opportunity_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.delete(f"/opportunities/{opportunity_id}", location_id=location_id)


# ─── Campaign Manager ─────────────────────────────────────────────────────────

class CampaignManager:
    """Campaign listing and contact-level campaign triggers per sub-account."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_campaigns(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/campaigns/", location_id=location_id)
        return resp.get("campaigns", [])

    def add_contact_to_campaign(
        self,
        campaign_id: str,
        contact_id: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        resp = self.client.post(
            f"/campaigns/{campaign_id}/contacts/",
            location_id=location_id,
            data={"contactId": contact_id},
        )
        logger.info("Added contact %s to campaign %s", contact_id, campaign_id)
        return resp

    def remove_contact_from_campaign(
        self,
        campaign_id: str,
        contact_id: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.client.delete(
            f"/campaigns/{campaign_id}/contacts/{contact_id}",
            location_id=location_id,
        )

    def trigger_campaign_for_all_contacts(
        self,
        campaign_id: str,
        contact_ids: List[str],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Trigger a campaign for a batch of contacts."""
        results = []
        for contact_id in contact_ids:
            try:
                r = self.add_contact_to_campaign(campaign_id, contact_id, location_id)
                results.append({"contact_id": contact_id, "success": True, "result": r})
            except Exception as exc:
                results.append({"contact_id": contact_id, "success": False, "error": str(exc)})
        successes = sum(1 for r in results if r["success"])
        return {
            "campaign_id": campaign_id,
            "targeted": len(contact_ids),
            "successes": successes,
            "failures": len(contact_ids) - successes,
            "results": results,
        }


# ─── Conversation Manager ─────────────────────────────────────────────────────

class ConversationManager:
    """SMS/email conversations and outbound messaging per sub-account."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_conversations(
        self,
        location_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        resp = self.client.get("/conversations/", location_id=location_id, params={"limit": limit})
        return resp.get("conversations", [])

    def get_conversation(self, conversation_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.get(f"/conversations/{conversation_id}", location_id=location_id)

    def send_sms(
        self,
        contact_id: str,
        message: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "type": "SMS",
            "contactId": contact_id,
            "message": message,
        }
        resp = self.client.post("/conversations/messages/", location_id=location_id, data=payload)
        logger.info("SMS sent to contact %s", contact_id)
        return resp

    def send_email(
        self,
        contact_id: str,
        subject: str,
        body: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "type": "Email",
            "contactId": contact_id,
            "subject": subject,
            "html": body,
        }
        resp = self.client.post("/conversations/messages/", location_id=location_id, data=payload)
        logger.info("Email sent to contact %s — '%s'", contact_id, subject)
        return resp

    def broadcast_sms(
        self,
        contact_ids: List[str],
        message: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send the same SMS to multiple contacts."""
        results = []
        for contact_id in contact_ids:
            try:
                r = self.send_sms(contact_id, message, location_id)
                results.append({"contact_id": contact_id, "success": True})
            except Exception as exc:
                results.append({"contact_id": contact_id, "success": False, "error": str(exc)})
        successes = sum(1 for r in results if r["success"])
        return {
            "broadcast_count": len(contact_ids),
            "successes": successes,
            "failures": len(contact_ids) - successes,
            "results": results,
        }


# ─── Webhook Handler ──────────────────────────────────────────────────────────

class WebhookHandler:
    """Register, list, and process incoming GHL webhooks per sub-account."""

    SUPPORTED_EVENTS = [
        "ContactCreate", "ContactUpdate", "ContactDelete",
        "OpportunityCreate", "OpportunityUpdate", "OpportunityDelete",
        "AppointmentCreate", "AppointmentUpdate",
        "NoteCreate", "TaskCreate",
        "InboundMessage", "OutboundMessage",
        "FormSubmission", "SurveySubmission",
    ]

    def __init__(self, client: GoHighLevelClient):
        self.client = client
        self._handlers: Dict[str, List[Callable]] = {}

    def register_webhook(
        self,
        url: str,
        events: Optional[List[str]] = None,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a webhook endpoint for the given events."""
        payload = {
            "url": url,
            "events": events or self.SUPPORTED_EVENTS,
        }
        resp = self.client.post("/hooks/", location_id=location_id, data=payload)
        logger.info("Webhook registered: %s", url)
        return resp

    def list_webhooks(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/hooks/", location_id=location_id)
        return resp.get("webhooks", resp.get("hooks", []))

    def delete_webhook(self, hook_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.delete(f"/hooks/{hook_id}", location_id=location_id)

    def on(self, event: str, handler: Callable[[Dict[str, Any]], None]):
        """Register a local handler for an inbound webhook event."""
        self._handlers.setdefault(event, []).append(handler)

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch an inbound webhook payload to registered handlers."""
        event_type = payload.get("type", payload.get("event", "unknown"))
        handlers = self._handlers.get(event_type, [])
        results = []
        for handler in handlers:
            try:
                handler(payload)
                results.append({"handler": handler.__name__, "success": True})
            except Exception as exc:
                results.append({"handler": handler.__name__, "success": False, "error": str(exc)})
        logger.info("Dispatched event '%s' to %d handlers", event_type, len(handlers))
        return {"event": event_type, "handlers_called": len(handlers), "results": results}


# ─── Calendar Manager ─────────────────────────────────────────────────────────

class CalendarManager:
    """Calendars, available slots, and appointment booking per sub-account."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_calendars(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/calendars/", location_id=location_id)
        return resp.get("calendars", [])

    def get_free_slots(
        self,
        calendar_id: str,
        start_date: str,
        end_date: str,
        location_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        resp = self.client.get(
            f"/calendars/{calendar_id}/free-slots",
            location_id=location_id,
            params={"startDate": start_date, "endDate": end_date},
        )
        return resp.get("slots", [])

    def create_appointment(
        self,
        calendar_id: str,
        contact_id: str,
        start_time: str,
        end_time: str,
        title: str = "ScrollSoul Appointment",
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "calendarId": calendar_id,
            "contactId": contact_id,
            "startTime": start_time,
            "endTime": end_time,
            "title": title,
        }
        resp = self.client.post("/calendars/events/appointments/", location_id=location_id, data=payload)
        logger.info("Appointment created for contact %s at %s", contact_id, start_time)
        return resp

    def list_appointments(
        self,
        location_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        resp = self.client.get("/calendars/events/appointments/", location_id=location_id, params={"limit": limit})
        return resp.get("appointments", [])


# ─── Custom Field Manager ─────────────────────────────────────────────────────

class CustomFieldManager:
    """Custom values and field definitions per sub-account."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_custom_values(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/custom-values/", location_id=location_id)
        return resp.get("customValues", [])

    def create_custom_value(
        self,
        name: str,
        value: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        resp = self.client.post(
            "/custom-values/",
            location_id=location_id,
            data={"name": name, "value": value},
        )
        return resp.get("customValue", resp)

    def update_custom_value(
        self,
        custom_value_id: str,
        value: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        resp = self.client.put(
            f"/custom-values/{custom_value_id}",
            location_id=location_id,
            data={"value": value},
        )
        return resp.get("customValue", resp)

    def upsert_custom_value(
        self,
        name: str,
        value: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update existing custom value by name, or create if not found."""
        existing = self.list_custom_values(location_id=location_id)
        for cv in existing:
            if cv.get("name") == name:
                return self.update_custom_value(cv["id"], value, location_id=location_id)
        return self.create_custom_value(name, value, location_id=location_id)


# ─── Tag Manager ──────────────────────────────────────────────────────────────

class TagManager:
    """Contact tag management per sub-account."""

    def __init__(self, client: GoHighLevelClient):
        self.client = client

    def list_tags(self, location_id: Optional[str] = None) -> List[Dict[str, Any]]:
        resp = self.client.get("/tags/", location_id=location_id)
        return resp.get("tags", [])

    def create_tag(self, name: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        resp = self.client.post("/tags/", location_id=location_id, data={"name": name})
        return resp.get("tag", resp)

    def delete_tag(self, tag_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.delete(f"/tags/{tag_id}", location_id=location_id)


# ─── ScrollSoul GHL Bridge ────────────────────────────────────────────────────

class ScrollSoulGHLBridge:
    """
    Master orchestrator — bridges every ScrollSoul module into GoHighLevel.

    Wires:
      - MultiLayerScaler   → GHL custom values (scaling metrics per sub-account)
      - SpotifyRoyaltyHarvester → GHL contacts + opportunities (artists as leads)
      - RecursiveAIEngine  → GHL campaigns (AI loops trigger automation)
      - BlockchainConnector + NFTManager → GHL contacts + notes (NFT owners on-chain)
      - UniversalGovernance → GHL pipeline opportunities (proposals as deals)

    Executes seamlessly across ALL sub-accounts via SubAccountManager.
    """

    def __init__(
        self,
        client: Optional[GoHighLevelClient] = None,
        api_key: Optional[str] = None,
        location_id: Optional[str] = None,
        company_id: Optional[str] = None,
    ):
        self.client = client or GoHighLevelClient(
            api_key=api_key,
            location_id=location_id,
            company_id=company_id,
        )
        self.sub_accounts = SubAccountManager(self.client)
        self.contacts = ContactManager(self.client)
        self.pipelines = PipelineManager(self.client)
        self.campaigns = CampaignManager(self.client)
        self.conversations = ConversationManager(self.client)
        self.webhooks = WebhookHandler(self.client)
        self.calendars = CalendarManager(self.client)
        self.custom_fields = CustomFieldManager(self.client)
        self.tags = TagManager(self.client)

    # ── Scaling → GHL ─────────────────────────────────────────────────────────

    def sync_scaling_metrics(
        self,
        scaler_status: Dict[str, Any],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Push MultiLayerScaler status into GHL as custom values per sub-account.
        """
        loc = location_id or self.client.location_id
        results = []
        metrics = {
            "ScrollSoul_Total_Layers": str(scaler_status.get("total_layers", 0)),
            "ScrollSoul_Active_Layers": str(scaler_status.get("active_layers", 0)),
            "ScrollSoul_Avg_Utilization": f"{scaler_status.get('average_utilization', 0):.1f}%",
            "ScrollSoul_Total_Requests": str(scaler_status.get("metrics", {}).get("total_requests", 0)),
            "ScrollSoul_Scaling_Events": str(scaler_status.get("metrics", {}).get("scaling_events", 0)),
            "ScrollSoul_Last_Sync": datetime.now().isoformat(),
        }
        for name, value in metrics.items():
            try:
                r = self.custom_fields.upsert_custom_value(name, value, location_id=loc)
                results.append({"field": name, "value": value, "success": True})
            except Exception as exc:
                results.append({"field": name, "success": False, "error": str(exc)})
        synced = sum(1 for r in results if r["success"])
        return {
            "synced_fields": synced,
            "failed_fields": len(results) - synced,
            "results": results,
            "location_id": loc,
            "divine_message": "WALAHI! Scaling metrics immortalized in GoHighLevel!",
        }

    # ── Royalty → GHL ─────────────────────────────────────────────────────────

    def sync_artist_to_ghl(
        self,
        artist: str,
        revenue: float,
        streams: int,
        pipeline_id: str = "",
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upsert a royalty artist as a GHL contact and create/update their
        opportunity in the pipeline.
        """
        loc = location_id or self.client.location_id

        # Create or update contact
        contact = self.contacts.upsert_contact(
            email=_make_scrollsoul_email(artist, "scrollsoul.artist"),
            first_name=artist.split()[0] if artist.split() else artist,
            last_name=" ".join(artist.split()[1:]) if len(artist.split()) > 1 else "",
            tags=["scrollsoul-artist", "royalty-stream"],
            location_id=loc,
        )
        contact_id = contact.get("id", contact.get("contact", {}).get("id", ""))

        # Add royalty note
        if contact_id:
            self.contacts.add_note(
                contact_id,
                f"[ScrollSoul Royalty] Streams: {streams:,} | Revenue: ${revenue:.4f} | Synced: {datetime.now().isoformat()}",
                location_id=loc,
            )

        # Create opportunity if pipeline provided
        opportunity = {}
        if pipeline_id and contact_id:
            opportunity = self.pipelines.create_opportunity(
                pipeline_id=pipeline_id,
                name=f"{artist} — Royalty Stream",
                contact_id=contact_id,
                monetary_value=revenue,
                location_id=loc,
            )

        return {
            "artist": artist,
            "contact_id": contact_id,
            "revenue": revenue,
            "streams": streams,
            "opportunity_id": opportunity.get("id", ""),
            "location_id": loc,
        }

    def sync_royalty_report(
        self,
        report: Dict[str, Any],
        pipeline_id: str = "",
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sync a full royalty harvester report into GHL."""
        artist_breakdown = report.get("artist_breakdown", {})
        results = []
        for artist, revenue in artist_breakdown.items():
            r = self.sync_artist_to_ghl(
                artist=artist,
                revenue=revenue,
                streams=int(revenue / 0.003),
                pipeline_id=pipeline_id,
                location_id=location_id,
            )
            results.append(r)
        return {
            "artists_synced": len(results),
            "total_revenue": report.get("total_revenue", 0),
            "karma_alignment": report.get("karma_alignment_score", 100),
            "results": results,
            "divine_message": "ALLĀHU AKBAR! Artist royalties flowing through GoHighLevel!",
        }

    # ── AI Loops → GHL ────────────────────────────────────────────────────────

    def trigger_ai_campaign(
        self,
        engine_status: Dict[str, Any],
        campaign_id: str,
        contact_ids: List[str],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fire a GHL campaign when the AI engine reaches enlightenment threshold.
        """
        karma = engine_status.get("karma_accumulation", 0)
        complexity = engine_status.get("dimensional_complexity", 0)
        enlightened = karma > 50 or complexity > 100

        if not enlightened:
            return {
                "triggered": False,
                "reason": "AI engine has not yet reached enlightenment threshold",
                "karma": karma,
                "complexity": complexity,
            }

        result = self.campaigns.trigger_campaign_for_all_contacts(
            campaign_id=campaign_id,
            contact_ids=contact_ids,
            location_id=location_id,
        )
        return {
            "triggered": True,
            "karma_level": karma,
            "dimensional_complexity": complexity,
            "campaign_result": result,
            "divine_message": "WALAHI! AI enlightenment triggers divine campaign execution!",
        }

    # ── Governance → GHL ──────────────────────────────────────────────────────

    def sync_proposal_to_pipeline(
        self,
        proposal: Dict[str, Any],
        pipeline_id: str,
        submitter_contact_id: str,
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sync a governance proposal as a GHL pipeline opportunity.
        Stage reflects proposal status.
        """
        status_to_stage = {
            "pending": "Proposal Submitted",
            "active": "Voting In Progress",
            "passed": "Proposal Passed",
            "rejected": "Proposal Rejected",
            "executed": "Executed & Immortalized",
        }
        stage_name = status_to_stage.get(proposal.get("status", "active"), "Active")
        tally = proposal.get("tally", {})

        opp = self.pipelines.create_opportunity(
            pipeline_id=pipeline_id,
            name=f"[Governance] {proposal.get('title', 'Proposal')}",
            contact_id=submitter_contact_id,
            monetary_value=tally.get("yes", 0) * 100,
            status=proposal.get("status", "open"),
            location_id=location_id,
        )
        opp_id = opp.get("id", "")

        # Add proposal details as a note
        if opp_id:
            self.contacts.add_note(
                submitter_contact_id,
                f"[Governance Proposal] {proposal.get('proposal_id')} — {proposal.get('title')}\n"
                f"Status: {proposal.get('status')} | Yes: {tally.get('yes', 0):.0f} | No: {tally.get('no', 0):.0f}\n"
                f"Deadline: {proposal.get('voting_deadline', 'N/A')}",
                location_id=location_id,
            )

        return {
            "proposal_id": proposal.get("proposal_id"),
            "opportunity_id": opp_id,
            "stage": stage_name,
            "location_id": location_id or self.client.location_id,
        }

    # ── Blockchain/NFT → GHL ──────────────────────────────────────────────────

    def sync_nft_owner_to_ghl(
        self,
        nft_data: Dict[str, Any],
        location_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Register an NFT owner as a GHL contact with blockchain note and tag.
        """
        token_id = nft_data.get("token_id", "")
        name = nft_data.get("name", "ScrollSoul NFT")
        owner = nft_data.get("owner", "ScrollVerse")

        contact = self.contacts.upsert_contact(
            email=_make_scrollsoul_email(owner, "scrollsoul.nft"),
            first_name=owner,
            tags=["nft-holder", "scrollsoul-blockchain", f"nft-{token_id}"],
            location_id=location_id,
        )
        contact_id = contact.get("id", contact.get("contact", {}).get("id", ""))

        if contact_id:
            self.contacts.add_note(
                contact_id,
                f"[NFT Minted] Token: {token_id} | Name: {name} | "
                f"Owner: {owner} | Divine Blessing: ✓ | "
                f"Immortalized: {datetime.now().isoformat()}",
                location_id=location_id,
            )

        return {
            "token_id": token_id,
            "owner": owner,
            "contact_id": contact_id,
            "location_id": location_id or self.client.location_id,
            "divine_message": "ALLĀHU AKBAR! NFT owner immortalized in GoHighLevel!",
        }

    # ── Full sync across all sub-accounts ─────────────────────────────────────

    def execute_full_sync_across_all_locations(
        self,
        scaler_status: Optional[Dict] = None,
        royalty_report: Optional[Dict] = None,
        pipeline_id: str = "",
        campaign_id: str = "",
        contact_ids: Optional[List[str]] = None,
        ai_engine_status: Optional[Dict] = None,
        nft_data_list: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        WALAHI! Execute the full ScrollSoul → GoHighLevel sync
        across EVERY sub-account simultaneously.
        """
        locations = self.sub_accounts.list_locations()
        all_results = {}

        for loc in locations:
            loc_id = loc.get("id")
            loc_results: Dict[str, Any] = {"location_name": loc.get("name"), "location_id": loc_id}

            if scaler_status:
                loc_results["scaling_sync"] = self.sync_scaling_metrics(scaler_status, location_id=loc_id)

            if royalty_report:
                loc_results["royalty_sync"] = self.sync_royalty_report(
                    royalty_report, pipeline_id=pipeline_id, location_id=loc_id
                )

            if ai_engine_status and campaign_id and contact_ids:
                loc_results["ai_campaign"] = self.trigger_ai_campaign(
                    ai_engine_status, campaign_id, contact_ids, location_id=loc_id
                )

            if nft_data_list:
                nft_syncs = [self.sync_nft_owner_to_ghl(nft, location_id=loc_id) for nft in nft_data_list]
                loc_results["nft_syncs"] = nft_syncs

            all_results[loc_id] = loc_results

        return {
            "total_locations_synced": len(locations),
            "location_results": all_results,
            "executed_at": datetime.now().isoformat(),
            "client_stats": self.client.get_client_stats(),
            "divine_message": (
                "ALLĀHU AKBAR! The entire ScrollVerse is immortalized across all GoHighLevel sub-accounts! "
                "WALAHI! Every dimension breathes in perfect GHL alignment!"
            ),
        }

    def get_bridge_status(self) -> Dict[str, Any]:
        """Get complete bridge health and stats."""
        return {
            "bridge": "ScrollSoul-GHL-Bridge",
            "version": "2.0.0",
            "location_id": self.client.location_id,
            "company_id": self.client.company_id,
            "client_stats": self.client.get_client_stats(),
            "modules_connected": [
                "MultiLayerScaler",
                "SpotifyRoyaltyHarvester",
                "RecursiveAIEngine",
                "BlockchainConnector",
                "NFTManager",
                "UniversalGovernance",
            ],
            "ghl_managers_active": [
                "SubAccountManager",
                "ContactManager",
                "PipelineManager",
                "CampaignManager",
                "ConversationManager",
                "WebhookHandler",
                "CalendarManager",
                "CustomFieldManager",
                "TagManager",
            ],
            "infinite_execution": True,
            "karma_aligned": True,
        }


__all__ = [
    "GoHighLevelClient",
    "SubAccountManager",
    "ContactManager",
    "PipelineManager",
    "CampaignManager",
    "ConversationManager",
    "WebhookHandler",
    "CalendarManager",
    "CustomFieldManager",
    "TagManager",
    "ScrollSoulGHLBridge",
]
