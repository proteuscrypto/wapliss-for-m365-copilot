<p align="center">
  <img src="assets/icon.png" alt="Wapliss logo" width="120" />
</p>

<h1 align="center">Wapliss WhatsApp for Microsoft 365 Copilot</h1>

<p align="center">
  <strong>Use your own WhatsApp from Microsoft 365 Copilot with the Wapliss MCP server.</strong><br />
  Read and summarize chats and groups, and send messages, files, locations and polls, always with your confirmation.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-25D366" alt="License: MIT" />
  <img src="https://img.shields.io/badge/Microsoft%20365%20Copilot-declarative%20agent-128C7E" alt="Microsoft 365 Copilot" />
  <img src="https://img.shields.io/badge/plugin%20manifest-v2.4%20RemoteMCPServer-24292f" alt="Plugin manifest v2.4" />
  <img src="https://img.shields.io/badge/version-1.0.0-25D366" alt="Version" />
</p>

<p align="center">
  <a href="https://wapliss.com/">Website</a> ·
  <a href="https://wapliss.com/integrations">Integration guides</a> ·
  <a href="#install">Install</a> ·
  <a href="#example-prompts">Examples</a> ·
  <a href="#faq">FAQ</a>
</p>

---

## What is Wapliss?

[Wapliss](https://wapliss.com/), by [NetDigitalTech LLC](https://netdigitaltech.com/), is a WhatsApp gateway for AI assistants. You link your WhatsApp number once with a QR code, authorize your assistant, and the assistant can read your chats and groups and send WhatsApp messages for you through a standard [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server. A free plan is available, with no credit card required.

This repository is the official **Microsoft 365 Copilot package** of Wapliss: a **declarative agent** with a **remote MCP server** action. It only points Microsoft 365 Copilot to the hosted Wapliss MCP server (`https://wapliss.com/mcp/v1`); it stores no account data, messages or credentials.

## How it works

| Piece | Value |
| --- | --- |
| Agent | Declarative agent (schema v1.9) with instructions and 6 conversation starters |
| Action | Plugin manifest v2.4, runtime `RemoteMCPServer`, URL `https://wapliss.com/mcp/v1` |
| Tools | Discovered at runtime from the server (dynamic tool discovery): 7 read tools and 9 send tools |
| Sign-in | OAuth 2.1 with dynamic client registration (RFC 7591) and PKCE. Microsoft's Enterprise token store registers the client; each user signs in to Wapliss once |
| Confirmation | Send tools are marked destructive, so Copilot asks before sending; bulk or unsolicited messaging is blocked by the server |

## Requirements

- A Microsoft 365 account with a **Microsoft 365 Copilot** license, and *Custom App Upload* and *Copilot Access* enabled for your account (Agents Toolkit shows both).
- [Visual Studio Code](https://code.visualstudio.com/) with **Microsoft 365 Agents Toolkit 6.12.0 or later** (dynamic client registration needs it; the Teams Developer Portal does not support it yet).
- A [Wapliss](https://wapliss.com/) account with your phone linked at [wapliss.com/app/connect](https://wapliss.com/app/connect).

## Install

1. Clone this repository and open the folder in VS Code.
2. Open **Microsoft 365 Agents Toolkit** and sign in with your Microsoft 365 account.
3. Select **Provision** (or run `atk provision --env dev` with the Agents Toolkit CLI). The toolkit:
   - creates the app in the Teams Developer Portal,
   - registers the OAuth client with Wapliss through dynamic client registration (`dcr/register`) and writes `MCP_DA_AUTH_ID_WAPLISS`,
   - builds, validates and uploads the app package, and makes the agent available to you in Microsoft 365 Copilot.
4. Open [Microsoft 365 Copilot](https://m365.cloud.microsoft/chat), pick **Wapliss WhatsApp (dev)** in the agents list and ask "Check my Wapliss account".
5. The first time, Copilot asks you to sign in: sign in to Wapliss and approve access.

To make the agent available to your whole organization, run **Publish** (`atk publish --env prod`); a Microsoft 365 admin approves it in the admin center.

## Example prompts

- "Show me my latest WhatsApp messages"
- "Summarize what was said today in my WhatsApp group Team"
- "Find my WhatsApp chat with Alex and show the last 10 messages"
- "Who is in my WhatsApp group Team?"
- "Send 'I'll join the meeting in 5 minutes' to Alex on WhatsApp" (Copilot confirms before sending)
- "Check my Wapliss account"

## Repository layout

```
appPackage/manifest.json          Microsoft 365 app manifest v1.30 (copilotAgents → declarativeAgent.json)
appPackage/declarativeAgent.json  declarative agent v1.9 (instructions, conversation starters, action)
appPackage/ai-plugin.json         plugin manifest v2.4: RemoteMCPServer https://wapliss.com/mcp/v1, OAuthPluginVault
appPackage/instruction.txt        agent instructions (safe reading and sending rules)
appPackage/color.png, outline.png icons (192 × 192 color, 32 × 32 white outline)
m365agents.yml                    Agents Toolkit lifecycle (v1.13, dcr/register)
env/.env.dev, env/.env.prod       environment values (filled in by provision)
scripts/validate.py               checks against the official schemas (+ --live checks of wapliss.com)
```

## Validate

```bash
pip install jsonschema pillow
python3 scripts/validate.py          # official schemas, limits, icons, toolkit config
python3 scripts/validate.py --live   # OAuth metadata and MCP 401 on wapliss.com
```

## FAQ

**Is this the official WhatsApp Business API?** No. Wapliss uses WhatsApp Web multi-device (your own account) and is not affiliated with Meta or Microsoft. It is meant for personal and small-team use, not for bulk messaging.

**Does Copilot send messages without asking?** No. The send tools are marked as destructive, so Copilot asks for confirmation, and the agent instructions require confirming the recipient and content when there is any doubt.

**Who can read my messages?** Only you, through your own Wapliss account. Content that Copilot reads is processed by Microsoft 365 Copilot under your organization's terms. See the [privacy policy](https://wapliss.com/privacy-policy).

**What does it cost?** Wapliss has a free plan (1 number, up to 100 messages per day to 3 contacts). Wapliss Pro costs US$ 7 per month. A Microsoft 365 Copilot license is billed by Microsoft.

**Provisioning fails at the sign-in step.** Use Agents Toolkit 6.12.0 or later; the Teams Developer Portal does not support dynamic client registration yet.

## Wapliss plugins

| Assistant | Package |
| --- | --- |
| Claude | [wapliss-whatsapp-for-claude](https://github.com/proteuscrypto/wapliss-whatsapp-for-claude) |
| ChatGPT | [wapliss-for-chatgpt](https://github.com/proteuscrypto/wapliss-for-chatgpt) |
| Gemini | [wapliss-for-gemini](https://github.com/proteuscrypto/wapliss-for-gemini) |
| DeepSeek | [wapliss-for-deepseek](https://github.com/proteuscrypto/wapliss-for-deepseek) |
| GitHub Copilot | [wapliss-for-copilot](https://github.com/proteuscrypto/wapliss-for-copilot) |
| Grok | [wapliss-for-grok](https://github.com/proteuscrypto/wapliss-for-grok) |
| Microsoft 365 Copilot | this repository |

## License

MIT © 2026 [NetDigitalTech LLC](https://netdigitaltech.com/), creator and owner of [Wapliss](https://wapliss.com/). Microsoft 365 and Copilot are trademarks of Microsoft. WhatsApp is a trademark of Meta. Wapliss is not affiliated with either.
