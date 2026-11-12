# Microsoft Marketplace listing — Wapliss WhatsApp for Microsoft 365 Copilot

Ready-to-paste values for Partner Center → **Apps and agents for Microsoft 365 and Copilot** (offer type: Microsoft 365 app / Copilot agent). Prepared on 2026-11-11.

## Offer setup

| Field | Value |
| --- | --- |
| Offer name | Wapliss WhatsApp |
| Offer alias (internal) | wapliss-m365-copilot |
| Publisher | NetDigitalTech LLC |
| App package | `appPackage/build/appPackage.prod.zip` built with `atk provision --env prod` from a NetDigitalTech LLC work account (fills `TEAMS_APP_ID` and `MCP_DA_AUTH_ID_WAPLISS`) |
| Pricing | Free in the Marketplace. Wapliss itself has a free plan; Wapliss Pro (US$ 7/month) is purchased on wapliss.com (SaaS, outside the Marketplace) |
| Products | Microsoft 365 Copilot (declarative agent). Also surfaces in Teams and Outlook through Copilot |

## Properties

| Field | Value |
| --- | --- |
| Categories | Productivity; Communication |
| Industries | Professional services; Retail and consumer goods (optional) |
| Keywords (max 3) | WhatsApp; MCP; messaging |
| Legal | Terms: https://wapliss.com/terms-of-service · Privacy: https://wapliss.com/privacy-policy |
| Support URL | https://wapliss.com/integrations#m365-copilot |
| Help URL | https://github.com/proteuscrypto/wapliss-for-m365-copilot#readme |
| Support email | commerce@netdigitaltech.com |

## Listing (English)

**Name:** Wapliss WhatsApp

**Short description (≤ 100 chars):**
Read, summarize and send your own WhatsApp messages from Microsoft 365 Copilot.

**Description:**

Wapliss brings your own WhatsApp account into Microsoft 365 Copilot, so you can work with your chats without switching apps.

Ask Copilot to:
- Show your latest WhatsApp messages, or the messages of one chat or group
- Summarize what was said today in a group, with who said what
- Find a contact or group by name and see its members
- Send a text, image, document, voice note, location, contact or poll to one recipient you name
- Check your Wapliss plan and daily quota

How it works:
1. Create a free account at wapliss.com and link your phone once by scanning a QR code (WhatsApp → Linked devices).
2. Open the Wapliss WhatsApp agent in Microsoft 365 Copilot and sign in to Wapliss when prompted (OAuth 2.1).
3. Ask in natural language. Copilot always asks before sending, and bulk or unsolicited messaging is blocked.

Privacy and security: Wapliss reads only the chats you ask about, and only from your own account. Sign-in uses OAuth 2.1 with PKCE; you can revoke access at any time from your Wapliss dashboard. Wapliss uses WhatsApp Web multi-device and is not affiliated with Meta or Microsoft.

Plans: the Free plan includes 1 WhatsApp number and up to 100 messages per day to 3 contacts. Wapliss Pro (US$ 7/month or US$ 70/year) adds unlimited chats and up to 2,000 messages per day. Requires a Microsoft 365 Copilot license.

Wapliss is a product of NetDigitalTech LLC (Albuquerque, New Mexico, USA).

## Listing (Spanish, optional)

**Nombre:** Wapliss WhatsApp

**Descripción corta:** Lee, resume y envía tus propios mensajes de WhatsApp desde Microsoft 365 Copilot.

**Descripción:** Wapliss lleva tu propia cuenta de WhatsApp a Microsoft 365 Copilot. Pídele a Copilot tus últimos mensajes, un resumen de lo que se habló en un grupo, quiénes son los miembros, o que envíe un texto, imagen, documento, nota de voz, ubicación, contacto o encuesta a la persona que indiques. Copilot siempre confirma antes de enviar y los envíos masivos están bloqueados. Vincula tu teléfono una vez con un código QR en wapliss.com e inicia sesión con OAuth 2.1. Plan Free: 1 número y hasta 100 mensajes por día a 3 contactos. Wapliss Pro: US$ 7/mes. Wapliss usa WhatsApp Web multidispositivo y no está afiliado a Meta ni a Microsoft. Un producto de NetDigitalTech LLC.

## Media

| Asset | File / spec |
| --- | --- |
| Large logo | `listing/logo-216.png` (216 × 216) or `listing/logo-300.png` |
| App icons (inside the package) | `appPackage/color.png` 192 × 192 · `appPackage/outline.png` 32 × 32 |
| Screenshots (3–5, 1366 × 768 PNG) | **To capture with a demo account** (no real conversations): 1) agent home with conversation starters, 2) "Show my latest WhatsApp messages" answer, 3) group summary, 4) send confirmation, 5) Wapliss dashboard with the phone linked |
| Video (optional) | YouTube link of the 60–90 s demo (marketing plan M-33) |

## Notes for certification (reviewer instructions)

> Wapliss WhatsApp is a declarative agent with a remote MCP server action (https://wapliss.com/mcp/v1, OAuth 2.1 with dynamic client registration and PKCE).
>
> Test account: sign in to Wapliss with **[DEMO EMAIL]** / **[DEMO PASSWORD]** when Copilot shows the sign-in card. This demo account has a test WhatsApp number already linked, with sample chats "Demo Contact" and "Demo Group". No real user data.
>
> Suggested prompts:
> 1. "Check my Wapliss account" → plan, quota and status `active`.
> 2. "Show me my latest WhatsApp messages" → list of recent messages.
> 3. "Summarize the WhatsApp group Demo Group" → summary with authors.
> 4. "Send 'Hello from Copilot' to Demo Contact on WhatsApp" → Copilot asks for confirmation, then reports the message as queued.
> 5. Negative: "Send a promotion to all my WhatsApp contacts" → the agent refuses (bulk messaging is blocked).
>
> Support: commerce@netdigitaltech.com.

## Before submitting

- [ ] Republish of CS-19, CS-12/13, CS-20 and CS-21 on wapliss.com (CS-20 is needed by Microsoft's dynamic client registration).
- [ ] Demo account with a linked test WhatsApp number (also used for the screenshots).
- [ ] Production package built with Agents Toolkit (`atk provision --env prod`) from a NetDigitalTech LLC work account; run `python3 scripts/validate.py --live`.
- [ ] Partner Center: company verification approved and the "Microsoft 365 and Copilot" program active.
