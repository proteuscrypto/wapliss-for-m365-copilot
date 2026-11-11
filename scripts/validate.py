#!/usr/bin/env python3
"""Validate the Wapliss declarative agent for Microsoft 365 Copilot.

Usage:
  python3 scripts/validate.py          # offline checks (schemas, limits, icons, placeholders)
  python3 scripts/validate.py --live   # also checks https://wapliss.com (OAuth metadata, MCP 401)
  python3 scripts/validate.py --live --dcr  # also registers a throwaway OAuth client like Microsoft does

Schemas in scripts/schemas/ are copied from the npm package @microsoft/app-manifest
(teams v1.30, declarative-agent v1.9, plugin v2.4).
"""
import json, re, sys, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = ROOT / 'appPackage'
SCHEMAS = ROOT / 'scripts' / 'schemas'
MCP_URL = 'https://wapliss.com/mcp/v1'
MS_REDIRECT = 'https://teams.microsoft.com/api/platform/v1.0/oAuthRedirect'

results = []

def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))

def load(name):
    return json.loads((PKG / name).read_text(encoding='utf-8'))

def resolve_placeholders(obj):
    """Agents Toolkit replaces ${{VAR}} at build time; use sample values for schema checks."""
    text = json.dumps(obj)
    text = text.replace('${{TEAMS_APP_ID}}', '00000000-0000-4000-8000-000000000000')
    text = text.replace('${{APP_NAME_SUFFIX}}', '')
    text = text.replace('${{MCP_DA_AUTH_ID_WAPLISS}}', 'sample-auth-config-id')
    return json.loads(text)

def schema_check(doc, schema_file, label):
    try:
        import jsonschema
    except ImportError:
        check(f'{label}: schema', False, 'pip install jsonschema')
        return
    schema = json.loads((SCHEMAS / schema_file).read_text(encoding='utf-8'))
    cls = jsonschema.validators.validator_for(schema)
    errors = sorted(cls(schema).iter_errors(doc), key=lambda e: list(e.path))
    check(f'{label}: official schema', not errors,
          '; '.join(f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message[:120]}" for e in errors[:5]))

def offline():
    manifest = load('manifest.json')
    agent = load('declarativeAgent.json')
    plugin = load('ai-plugin.json')
    instructions = (PKG / 'instruction.txt').read_text(encoding='utf-8')

    schema_check(resolve_placeholders(manifest), 'manifest-v1.30.json', 'manifest.json')
    schema_check(resolve_placeholders(agent), 'declarative-agent-v1.9.json', 'declarativeAgent.json')
    schema_check(resolve_placeholders(plugin), 'plugin-v2.4.json', 'ai-plugin.json')

    # Manifest limits
    short_name = manifest['name']['short'].replace('${{APP_NAME_SUFFIX}}', ' (dev)')
    check('manifest name.short <= 30', len(short_name) <= 30, short_name)
    check('manifest name.full <= 100', len(manifest['name']['full']) <= 100)
    check('manifest description.short <= 80', len(manifest['description']['short']) <= 80)
    check('manifest description.full <= 4000', len(manifest['description']['full']) <= 4000)
    check('manifest points to declarativeAgent.json',
          manifest['copilotAgents']['declarativeAgents'][0]['file'] == 'declarativeAgent.json')
    check('manifest developer URLs are https://wapliss.com',
          all(v.startswith('https://wapliss.com') for k, v in manifest['developer'].items() if k.endswith('Url')))
    check('manifest validDomains includes wapliss.com', 'wapliss.com' in manifest['validDomains'])

    # Declarative agent limits
    check('agent name <= 100', len(agent['name']) <= 100)
    check('agent description <= 1000', len(agent['description']) <= 1000)
    check('instructions <= 8000 chars', len(instructions) <= 8000, f'{len(instructions)} chars')
    check('instructions loaded from file', agent['instructions'] == "$[file('instruction.txt')]")
    starters = agent.get('conversation_starters', [])
    check('conversation starters 1-12', 1 <= len(starters) <= 12, str(len(starters)))
    check('action file is ai-plugin.json', agent['actions'][0]['file'] == 'ai-plugin.json')

    # Plugin
    rt = plugin['runtimes'][0]
    check('plugin runtime is RemoteMCPServer', rt['type'] == 'RemoteMCPServer')
    check('plugin MCP URL is /mcp/v1', rt['spec']['url'] == MCP_URL)
    check('plugin dynamic tool discovery (run_for_functions *, no pinned functions)',
          rt.get('run_for_functions') == ['*'] and plugin.get('functions') == [])
    check('plugin auth OAuthPluginVault with env reference',
          rt['auth'] == {'type': 'OAuthPluginVault', 'reference_id': '${{MCP_DA_AUTH_ID_WAPLISS}}'})
    check('description_for_human <= 100', len(plugin['description_for_human']) <= 100)
    check('description_for_model <= 2048', len(plugin['description_for_model']) <= 2048)

    # Icons
    try:
        from PIL import Image
        c = Image.open(PKG / 'color.png'); o = Image.open(PKG / 'outline.png')
        check('color.png 192x192', c.size == (192, 192), str(c.size))
        check('outline.png 32x32 with transparency', o.size == (32, 32) and o.mode == 'RGBA', f'{o.size} {o.mode}')
        if o.mode == 'RGBA':
            px = [p for p in (o.get_flattened_data() if hasattr(o, "get_flattened_data") else o.getdata()) if p[3] > 0]
            check('outline.png is white only', all(p[:3] == (255, 255, 255) for p in px), f'{len(px)} opaque px')
    except ImportError:
        check('icons', False, 'pip install pillow')

    # Toolkit project
    yml = (ROOT / 'm365agents.yml').read_text(encoding='utf-8')
    check('m365agents.yml version >= v1.13 (dcr/register)', re.search(r'^version:\s*v1\.(1[3-9]|[2-9]\d)', yml, re.M))
    check('m365agents.yml has dcr/register for /mcp/v1',
          'uses: dcr/register' in yml and f'mcpResourceUrl: {MCP_URL}' in yml)
    check('dcr writes MCP_DA_AUTH_ID_WAPLISS', 'configurationId: MCP_DA_AUTH_ID_WAPLISS' in yml)
    for env in ('dev', 'prod'):
        text = (ROOT / 'env' / f'.env.{env}').read_text(encoding='utf-8')
        check(f'env/.env.{env} declares MCP_DA_AUTH_ID_WAPLISS', 'MCP_DA_AUTH_ID_WAPLISS=' in text)
    # No secrets committed
    blob = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in ROOT.rglob('*')
                     if p.is_file() and p.suffix in ('.json', '.yml', '.txt', '.md') and 'schemas' not in p.parts)
    check('no secrets in the repo', not re.search(r'wp_live_[A-Za-z0-9]{8,}|wpl_sec_[a-f0-9]{8,}|client_secret"\s*:\s*"[^"$]', blob))

def http(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={'Content-Type': 'application/json', **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode()

def live(dcr):
    st, _, body = http('GET', 'https://wapliss.com/.well-known/oauth-protected-resource/mcp/v1')
    meta = json.loads(body) if st == 200 else {}
    check('live: protected resource metadata (RFC 9728) for /mcp/v1', st == 200 and meta.get('resource') == MCP_URL, f'HTTP {st}')
    st, _, body = http('GET', 'https://wapliss.com/.well-known/oauth-authorization-server')
    asm = json.loads(body) if st == 200 else {}
    check('live: authorization server metadata (RFC 8414) with registration_endpoint',
          st == 200 and asm.get('registration_endpoint'), f'HTTP {st}')
    check('live: PKCE S256 advertised', 'S256' in asm.get('code_challenge_methods_supported', []))
    check('live: client_secret auth methods advertised',
          {'client_secret_post', 'client_secret_basic'} & set(asm.get('token_endpoint_auth_methods_supported', [])))
    st, hdrs, _ = http('POST', MCP_URL, {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}})
    www = hdrs.get('WWW-Authenticate') or hdrs.get('www-authenticate') or ''
    check('live: /mcp/v1 without token -> 401 with resource_metadata', st == 401 and 'resource_metadata' in www, f'HTTP {st}')
    if dcr:
        st, _, body = http('POST', asm.get('registration_endpoint', 'https://wapliss.com/oauth/register'),
                           {'client_name': 'Microsoft 365 Copilot (validate.py)', 'redirect_uris': [MS_REDIRECT],
                            'grant_types': ['authorization_code', 'refresh_token'], 'response_types': ['code'],
                            'token_endpoint_auth_method': 'client_secret_post'})
        reg = json.loads(body) if st in (200, 201) else {}
        check('live: DCR accepts the Microsoft redirect URI', st in (200, 201), f'HTTP {st} {body[:120]}')
        check('live: DCR issues a client_secret (required by Microsoft)', bool(reg.get('client_secret')))

if __name__ == '__main__':
    offline()
    if '--live' in sys.argv:
        live('--dcr' in sys.argv)
    width = max(len(n) for n, _, _ in results)
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}  {n.ljust(width)}  {d}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f'\n{len(results) - failed}/{len(results)} passed')
    sys.exit(1 if failed else 0)
