# Hetzner Cloud: one cheap server, recon without token

2026-10-20. No token. No API calls. Local hcloud v1.70.1. No recommendation.

Tags:
- `[help]`: `hcloud <cmd> --help`, local.
- `[raw]`: hetzner.com product page HTML, curl, tags stripped, grepped. Copies: `/tmp/aoa-hetzner-raw/`.
- `[docs]`: official docs via WebFetch. Model summary; quotes unverified against raw HTML.
- `[log]`: docs.hetzner.cloud/changelog via WebFetch. Summary.
- `[sdk]`: hcloud-go source, GitHub main, via WebFetch. Summary.
- `[3p]`: third party, search snippet. Not authoritative.
- `[inferred]`: my inference. No source.

## Bottom line

- Cheapest x86 shared: CX23. 2 vCPU, 4 GB, 40 GB NVMe, €5.99/mo excl. VAT. `[raw]`
- Cheapest Arm: CAX11. 2 vCPU, 4 GB, 40 GB NVMe, Ampere®, €6.49/mo excl. VAT. `[raw]`
- Both read "This product is currently unavailable." `[raw]`
- Arm costs more than x86 at each matched size. `[raw]`
- No API or CLI route to create a project found. `[docs][help][sdk]`
- Hourly billing, capped at monthly. Stopped servers billed. Deleting a server stops server billing. Unassigned Primary IPs keep billing. `[docs]`
- Firewalls: stateful, free. `[docs]`
- iroh's FAQ names one relay UDP port, 7842. All-UDP opens more. `[docs]`

---

## 1. Command sequence

Placeholders: `aoa-relay`, `aoa-relay-key`, `aoa-relay-fw`, `aoa-relay-01`. Flags checked against `[help]` unless tagged.

```bash
# 0. version, no API
hcloud version                                   # v1.70.1 [help]

# 1. context from token
hcloud context create aoa-relay                  # asks for the token unless --token-from-env is set [help]
# hcloud context create --token-from-env aoa-relay   # reads HCLOUD_TOKEN [help]
hcloud context use aoa-relay                     # [help]
hcloud context active                            # [help]

# 2. upload SSH public key
hcloud ssh-key create --name aoa-relay-key --public-key-from-file ~/.ssh/id_ed25519.pub   # [help]

# 3. server types with prices
hcloud server-type list -o columns=name,architecture,cores,memory,disk,location_available   # [help]
hcloud server-type list -o json | jq -r '.[] | . as $t | $t.prices[] | [$t.name, $t.architecture, $t.cores, $t.memory, $t.disk, .location, .price_monthly.net, .price_hourly.net] | @tsv'
# prices[], price_monthly, price_hourly, net: [sdk]. Table view has no price column [help].
# Other JSON keys and array shape: [inferred]

# 4. locations
hcloud location list -o columns=name,city,country,network_zone   # [help]

# 5. images
hcloud image list -t system -a x86 -o columns=name,os_flavor,os_version,architecture,deprecated,status   # [help]
hcloud image list -t system -a arm -o columns=name,os_flavor,os_version,architecture,deprecated,status   # [help]
hcloud image list -t app -o columns=name,description,architecture,deprecated                             # [help]
# "deprecated" field to be removed; use "deprecation" [log 2026-09-08]

# 6. firewall: TCP 22, 80, 443, UDP all ports
hcloud firewall create --name aoa-relay-fw       # [help]
hcloud firewall add-rule --direction in --source-ips 0.0.0.0/0,::/0 --protocol tcp --port 22 aoa-relay-fw
hcloud firewall add-rule --direction in --source-ips 0.0.0.0/0,::/0 --protocol tcp --port 80 aoa-relay-fw
hcloud firewall add-rule --direction in --source-ips 0.0.0.0/0,::/0 --protocol tcp --port 443 aoa-relay-fw
hcloud firewall add-rule --direction in --source-ips 0.0.0.0/0,::/0 --protocol udp --port 1-65535 aoa-relay-fw
# --port required for tcp/udp; ranges such as 80-85 accepted [help]. 1-65535 = all ports [inferred].

# 7. server: --location (--datacenter removed) [help]
hcloud server create --name aoa-relay-01 --type cx23 --image ubuntu-26.04 --location nbg1 \
  --ssh-key aoa-relay-key --user-data-from-file ./cloud-init.yaml --firewall aoa-relay-fw
# ubuntu-26.04 [log 2026-05-18]. cx23 as lowercase API name [inferred]; page name CX23 [raw].

# 8. apply firewall to an existing server
hcloud firewall apply-to-resource --type server --server aoa-relay-01 aoa-relay-fw   # [help]

# 9. public IPs
hcloud server ip aoa-relay-01                    # IPv4 [help]
hcloud server ip -6 aoa-relay-01                 # "first address of the Server's Primary IPv6 network" [help]
hcloud server describe aoa-relay-01 -o json | jq -r '.public_net.ipv4.ip, .public_net.ipv6.ip'   # keys [sdk]
# -6 output equal to public_net.ipv6.ip: not verified

# 10. delete
hcloud firewall remove-from-resource --type server --server aoa-relay-01 aoa-relay-fw   # [help]
hcloud server delete aoa-relay-01                                                          # [help]
hcloud firewall delete aoa-relay-fw                                                       # [help]
hcloud primary-ip list -o columns=name,ip,assignee,auto_delete                            # leftovers [help]
hcloud primary-ip delete <primary-ip>                                                     # [help]
hcloud image list -t snapshot                                                             # leftover snapshots [help]
hcloud image list -t backup                                                               # leftover backups [help]
# Detach-first order: [inferred]. Firewall delete while attached: not verified.
```

### 1b. Firewall facts

- Stateful: "Yes, our Cloud Firewalls are stateful and track individual network connections and their states to and from your server." `[docs]` faq
- Responses to outbound requests pass without an inbound rule. `[docs]` faq
- Private networks not filtered: "Not yet, because we consider the private networks to be 'secure'." `[docs]` faq
- No rules: inbound blocked, outbound permitted. `[docs]` overview
- Limits: 500 (effective) rules per firewall, 5 firewalls per server, 50 across all projects. `[docs]` overview
- Free: "We do not charge for our Cloud Firewalls." `[docs]` overview
- Range syntax `80-85` in CLI flag text `[help]`. API range wording: not verified. API docs page did not render.
- iroh relay ports, official FAQ `[docs]`:
  - TCP 443: "This is the only connection iroh strictly requires, and it's an HTTPS connection that upgrades to a WebSocket."
  - UDP 7842: "used to learn your own public address." QUIC address discovery.
  - Full relay port list sits on an Enterprise page, not read. STUN 3478: not on page.
  - Clients: "Nothing listens for inbound connections, no ports are forwarded."
- Conflict `[3p]`, search summary, not fetched: iroh-relay README dev example puts QUIC on 7824. FAQ says 7842. Unresolved.
- Self-hosting guide `[3p]`: TLS relay on 80, 443, 7842.

---

## 2. Server types, prices, locations

Page text `[raw]`, hetzner.com/cloud/cost-optimized/, 2026-10-20. Prices excl. VAT. Label "Price incl. IPv4". Card Details: "eu-central NBG1 HEL1".

| plan | CPU label | vCPU | RAM | disk | €/mo | €/h |
|---|---|---|---|---|---|---|
| CX23 | Intel®/AMD (x86) | 2 | 4 GB | 40 GB NVMe | 5.99 | 0.0096 |
| CX33 | Intel®/AMD (x86) | 4 | 8 GB | 80 GB NVMe | 8.99 | 0.0144 |
| CX43 | Intel®/AMD (x86) | 8 | 16 GB | 160 GB NVMe | 16.49 | 0.0264 |
| CX53 | Intel®/AMD (x86) | 16 | 32 GB | 320 GB NVMe | 29.99 | 0.0481 |
| CAX11 | Ampere® (Arm) | 2 | 4 GB | 40 GB NVMe | 6.49 | 0.0104 |
| CAX21 | Ampere® (Arm) | 4 | 8 GB | 80 GB NVMe | 10.99 | 0.0176 |
| CAX31 | Ampere® (Arm) | 8 | 16 GB | 160 GB NVMe | 21.49 | 0.0344 |
| CAX41 | Ampere® (Arm) | 16 | 32 GB | 320 GB NVMe | 41.49 | 0.0665 |

- All 8 cards: "This product is currently unavailable. Please check back later." `[raw]`
- Card locations: nbg1, hel1 `[raw]`. fsn1 only in page-level "Available Locations eu-central FSN NBG HEL" `[raw]`.
- Codes ASH1, HIL1, SIN1: absent from the page `[raw]`. Ashburn, Hillsboro, Singapore: general text, not cards `[raw]`.
- API gives `net` and `gross`. `.net` matches the page label `[sdk]`.
- Hourly price times hours, capped at monthly `[docs]` billing FAQ.
- Calculator, Oct 2026 `[3p]`: CX23 €5.49 + €0.50 IPv4 = €5.99. Fits the label. CAX11 split (€5.99 + €0.50) `[inferred]`.
- 2026 price increases, April and mid-June `[3p]`. Not verified on a Hetzner page.

### Regular Performance (x86 shared, AMD)

Raw text confirmed CPX02 and CPX22 only. Other rows: `[docs]` summary, not raw-checked.

| plan | vCPU | RAM | disk | €/mo | €/h | locations |
|---|---|---|---|---|---|---|
| CPX02 `[raw]` | 1 | 1 GB | 20 GB NVMe | 6.49 | 0.0104 | FSN1, NBG1, HEL1; SIN1 7.99 |
| CPX12 | 1 | 2 GB | 40 GB NVMe | 11.99 | 0.0192 | FSN1, NBG1, HEL1; SIN1 15.99 |
| CPX22 `[raw]` | 2 | 4 GB | 80 GB NVMe | 19.99 | 0.0320 | NBG1, HEL1; SIN1 26.99 |
| CPX32 | 4 | 8 GB | 160 GB NVMe | 35.99 | 0.0577 | NBG1, HEL1 |
| CPX42 | 8 | 16 GB | 320 GB NVMe | 69.99 | 0.1122 | NBG1, HEL1 |
| CPX52 | 12 | 24 GB | 480 GB NVMe | 100.99 | 0.1618 | NBG1, HEL1 |
| CPX62 | 16 | 32 GB | 640 GB NVMe | 130.49 | 0.2091 | NBG1, HEL1 |
| CPX11 | 2 | 2 GB | 40 GB NVMe | 17.99 | 0.0288 | HIL1, ASH1 |
| CPX21 | 3 | 4 GB | 80 GB NVMe | 32.49 | 0.0521 | HIL1, ASH1 |
| CPX31 | 4 | 8 GB | 160 GB NVMe | 62.99 | 0.1009 | HIL1, ASH1 |
| CPX41 | 8 | 16 GB | 240 GB NVMe | 120.99 | 0.1939 | HIL1, ASH1 |
| CPX51 | 16 | 32 GB | 360 GB NVMe | 238.49 | 0.3822 | HIL1, ASH1 |

- All 12 cards: "currently unavailable" `[raw]`.
- Search snippet `[3p]`: a 2026 article says CX and CAX are unavailable and CPX22 (€19.99) is the closest orderable plan. Raw page shows CPX22 unavailable. Unresolved.
- Live or static availability text: not verified. Live check: `hcloud server-type list -o columns=name,location_available`.

---

## 3. System images and apps

### System images

- Distributions: "Ubuntu, Fedora, Debian, CentOS, Rocky Linux, and AlmaLinux" `[docs]` servers overview. No versions there.
- Ubuntu 26.04: `ubuntu-26.04`. IDs 387894169 (x86), 387894171 (arm). Added 2026-05-18 `[log]`.
- Ubuntu 22.04, 24.04, 26.04: named for Private Networks auto-configuration via cloud-init, 2026-05-18 `[log]`.
- `ubuntu-22.04` and `ubuntu-24.04` names, arm availability: not verified. `[inferred]` from 26.04 pattern.
- Changelog, newest first `[log]`:
  - 2026-09-08: Field "deprecated" will be removed. For Images, use the `deprecation` field.
  - 2026-08-31: `debian-11` deprecated. No new servers after 2026-11-30.
  - 2026-07-30: `opensuse-15` unavailable for new servers. IDs 204457491 (x86), 204457492 (arm).
  - 2026-06-30: `fedora-42` unavailable for new servers. IDs 232895138 (x86), 232895264 (arm).
  - 2026-05-18: `fedora-44` and `ubuntu-26.04` available.
  - 2026-04-30: `opensuse-15` deprecated. Unavailable after 2026-07-30.
  - 2026-03-30: `fedora-42` deprecated. Unavailable after 2026-06-30.
  - 2026-02-05: `fedora-41` unavailable for new servers. IDs 199030328 (x86), 199030407 (arm).
  - 2025-12-18: `fedora-43` and `opensuse-16` available. `opensuse-16` IDs 342262088 (x86), 342262097 (arm).
- Summary read 100,000 of 107,248 characters. Oldest entries unread. No row above depends on them.

### Apps (image type `app`)

- `docker-ce` `[docs]`, last change 2024-11-06:
  - Use: `hcloud server create --image docker-ce`.
  - Base: Ubuntu 24.04.
  - Preinstalled: Docker (license "GPLv3 (Apache 2.0)") and Docker Compose plugin.
  - Docker Engine version: not on page.
- `photoprism` `[docs]`, created 2023-03-01, last change 2024-11-06:
  - Base: Ubuntu 24.04.
  - Preinstalled as Docker containers: PhotoPrism, MariaDB, Traefik, Watchtower.
  - Not activated until login `[docs]` summary.
  - Let's Encrypt: in links section, not in package table `[docs]`.
  - Running state at first boot: not verified.
- Full catalog `[raw]`, hetzner.com/cloud, 12 names: Coolify, Docker CE, GitLab CE, Grafana, Jitsi Meet, Nextcloud, Owncast, PhotoPrism, Prometheus, RustDesk, WireGuard, Wordpress.
- Page wording: "every cloud server comes with free, high-quality one-click apps that are ready to go in just a few minutes."
- Apps index `docs.hetzner.com/cloud/apps/list/`: HTTP 404.
- Search snippet `[3p]`: five names, including LAMP Stack. LAMP Stack appears only there.
- Image values and contents for the other ten apps: not verified.

---

## 4. Billing

Source `[docs]` billing FAQ. Page footer: "Last change on 2020-07-07". Current terms: not cross-checked.

- Hourly, capped at monthly: "Your server's bill will never exceed its monthly price cap." Hourly usage rounded up.
- Stopped servers billed: "Yes, you pay for a server that has completed the creation process for as long as it exists," "regardless of whether it is turned on or not."
- Deleting stops server billing: "If you delete your cloud server before the end of the billing month, we will only bill you for the hourly rate."
- Unassigned Primary IPs billed: "including Primary IPs that are not assigned to any cloud server." "If you want to stop paying for a Primary IP, you need to delete it."
- Primary IPv4: €0.50/mo excl. VAT. Primary IPv6: free. `[docs]` primary-ips page and FAQ.
- Snapshots: per GB per month, prorated. Backups: 20% of server price, monthly. Floating IPs: monthly.
- After server deletion, not on page: snapshots, backups, floating IPs, volumes, load balancers.
- Firewalls: free `[docs]`.
- Primary IP `auto_delete`:
  - Flag `hcloud primary-ip create --auto-delete`: "Delete Primary IP if assigned resource is deleted" `[help]`.
  - Default: not on pages read.
  - Changelog 2026-05-01 `[log]`: assigned Primary IP must be unassigned before deletion.
  - Server deletion leaves its Primary IPv4 behind: not verified.
- `server create --without-ipv4` exists `[help]`. Plan-price effect: not on pages read.

---

## 5. Projects

- `[docs]` token page: "To generate an API token on your Hetzner Console, please open your project and do the following:" Steps: Security, API tokens, Generate API token.
- Permissions: Read = GET only. Read & Write = GET, DELETE, PUT, POST. Token shown once.
- `[docs]` not on page: whether a token is tied to one project; how to create a project.
- `[help]`: `hcloud --help` lists no project resource. `hcloud api <path>` is a raw call, GET by default.
- `[sdk]`: hcloud-go Client has 22 service fields. None is Project.
- Search snippet `[3p]`: a token works only inside its project. Not verified on a Hetzner page.
- Result: no documented API or CLI route to create a project. Docs describe projects only in the Console.
- Check after token exists, read-only: `hcloud api /projects`. Result decides. `[inferred]`

---

## Recommendation inputs

Facts only. No recommendation.

- Price pairs, excl. VAT `[raw]`:
  - 2 vCPU / 4 GB: CX23 €5.99, CAX11 €6.49.
  - 4 vCPU / 8 GB: CX33 €8.99, CAX21 €10.99.
  - 8 vCPU / 16 GB: CX43 €16.49, CAX31 €21.49.
  - 16 vCPU / 32 GB: CX53 €29.99, CAX41 €41.49.
- CPU labels: "Intel®/AMD" (CX), "Ampere®" (CAX), "AMD" (CPX) `[raw]`.
- Locations: nbg1, hel1 for CX and CAX `[raw]`.
- Availability: all 8 CX/CAX and 12 CPX cards read "currently unavailable" `[raw]`. Search-snippet conflict on CPX22 `[3p]`.
- Rust `[docs]` platform support: `x86_64-unknown-linux-gnu` and `aarch64-unknown-linux-gnu` are both "Tier 1 with Host Tools". Both run rustc and cargo natively.
- iroh CI `[docs]`, one file (`.github/workflows/ci.yml`, main):
  - No arm64 Linux runner named.
  - aarch64 appears only as `aarch64-linux-android`, build only.
  - Several jobs take runners dynamically.
  - Other workflows: not read.
- Claude Code `[docs]` setup page:
  - Hardware: "4 GB+ RAM, x64 or ARM64 processor".
  - OS: macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+.
  - Native install: `curl -fsSL https://claude.ai/install.sh | bash` (macOS, Linux, WSL).
  - npm needs Node.js 22+. Platforms include linux-x64, linux-arm64, and musl variants.
- Both 2-vCPU plans have 4 GB RAM, equal to the Claude Code minimum `[raw]` `[docs]`.
- Ubuntu 26.04 has x86 and arm image IDs `[log]`.
- Rust build time and memory benchmarks: none read.

---

## Open and unverified

- Prices and availability: raw text for CX/CAX and CPX02/CPX22; model summary for other CPX rows. Live values need `hcloud server-type list -o json` after token.
- Availability: live or static text not verified. Live order path not verified.
- Price split (€5.49 + €0.50 IPv4) from third party only. Hetzner not checked.
- Lowercase API type names and `ubuntu-22.04`/`ubuntu-24.04` names: `[inferred]`.
- `--port 1-65535` for all UDP: `[inferred]`. Verify with `hcloud firewall describe aoa-relay-fw -o json`.
- Firewall delete while attached: not verified. Detach-first order: `[inferred]`.
- Primary IPv4 after server delete: default not found. Check `auto_delete` first.
- `server ip -6` vs `public_net.ipv6.ip`: not verified.
- Billing FAQ dated 2020-07-07. Current terms: not verified.
- Projects: no creation route found. "Console only" inferred from absence.
- Changelog summary read 100,000 of 107,248 characters.
- One iroh workflow read. Others unread.
- Changelog 2026-09-08 `[log]`: Images field `deprecated` will be removed. CLI column `deprecated` breaks after removal `[inferred]`. Not tested (no token).
- One WebFetch result carried a system-reminder-style block naming a different user email. Ignored. No effect on this work.

## Sources

Local `hcloud` v1.70.1 help: version; context, context create/use/active; ssh-key create; server-type list/describe; location list; image list/describe; server create/ip/describe/delete/poweroff/shutdown/list; firewall create/add-rule/apply-to-resource/remove-from-resource/delete/describe/replace-rules/list; primary-ip list/create/delete; api.

Official docs (WebFetch summary):
- https://docs.hetzner.com/cloud/billing/faq/
- https://docs.hetzner.com/cloud/firewalls/overview/
- https://docs.hetzner.com/cloud/firewalls/faq/
- https://docs.hetzner.com/cloud/servers/primary-ips/overview/
- https://docs.hetzner.com/cloud/servers/overview/
- https://docs.hetzner.com/cloud/apps/list/docker-ce/
- https://docs.hetzner.com/cloud/apps/list/photoprism/
- https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/
- https://docs.hetzner.cloud/changelog
- https://docs.iroh.computer/about/faq
- https://doc.rust-lang.org/rustc/platform-support.html
- https://code.claude.com/docs/en/setup

Raw HTML (curl, 2026-10-20):
- https://www.hetzner.com/cloud/
- https://www.hetzner.com/cloud/cost-optimized/
- https://www.hetzner.com/cloud/regular-performance/

SDK (GitHub main, WebFetch summary):
- https://github.com/hetznercloud/hcloud-go: `hcloud/schema/pricing.go`, `hcloud/schema/server_type.go`, `hcloud/schema/server.go`, `hcloud/schema/firewall.go`, `hcloud/client.go`

CI:
- https://github.com/n0-computer/iroh/blob/main/.github/workflows/ci.yml

Third party, not authoritative `[3p]` (search snippets only):
- https://costgoat.com/pricing/hetzner
- https://stackvaluelab.com/hetzner-cx-cax-unavailable/
