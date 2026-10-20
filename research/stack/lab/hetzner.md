# Hetzner Cloud: one cheap server, recon without token

2026-10-20. No token. No API calls. Local hcloud v1.70.1. No recommendation.

Tags:
- `[help]`: `hcloud <cmd> --help`, local.
- `[raw]`: hetzner.com product page HTML, curl, tags stripped, grepped. Copies: `/tmp/aoa-hetzner-raw/`.
- `[docs]`: official docs via WebFetch. Model summary; quotes unverified against raw HTML.
- `[log]`: docs.hetzner.cloud/changelog via WebFetch. Summary.
- `[sdk]`: hcloud-go source, GitHub main, via WebFetch. Summary.
- `[3p]`: third party, search snippet. Not authoritative.
- `[news]`: docs.hetzner.cloud/whats-new. Raw HTML, text extracted and checked.
- `[price]`: docs.hetzner.com price-adjustment page. Raw HTML, figures checked.
- `[inferred]`: my inference. No source.

## Bottom line

- Cheapest x86 shared: CX23. 2 vCPU, 4 GB, 40 GB NVMe. €5.99/mo excl. VAT with IPv4 (€5.49 without). `[raw][price]`
- Cheapest Arm: CAX11. 2 vCPU, 4 GB, 40 GB NVMe, Ampere®. €6.49/mo excl. VAT with IPv4 (€5.99 without). `[raw][price]`
- Prices rose 2026-06-15. CX23 without IPv4: €3.99 → €5.49. See "Recent changes that matter". `[price]`
- Both read "This product is currently unavailable." `[raw]`
- Arm costs more than x86 at each matched size. The gap widened at three of four sizes on 2026-06-15. `[raw][price]`
- Newest plans: CPX12 (EU, 2026-07-07) and CPX02 (EU and SIN, 2026-10-06). The price page marks both unavailable. `[news][raw]`
- No API or CLI route to create a project found. `[docs][help][sdk]`
- Hourly billing, capped at monthly. Stopped servers billed. Deleting a server stops server billing. Unassigned Primary IPs keep billing. `[docs]`
- Firewalls: stateful, free. `[docs]`
- iroh's FAQ names one relay UDP port, 7842. All-UDP opens more. `[docs]`

---

## Recent changes that matter

Newest first. Quotes verbatim. `[news]` = whats-new page. `[price]` = price-adjustment page. `[press]` = press release, WebFetch summary.

- **2026-10-20. New network stack beta (hcnet).** `[news]`
  - "The new Hetzner Cloud network stack "hcnet" is now available in public beta. You can trigger a switch for each server individually."
  - "Limit increase for connection tracking from 80,000 parallel connections for both IPv4 and IPv6 combined, to 120,000 each."
  - "If a firewall is active, existing connections may be dropped."
  - Switch per server: Networking tab, "Try new network stack". Default for new servers: not on page.

- **2026-10-06. CPX02 added (EU and SIN).** `[news]`
  - "...we have now introduced the "Regular Performance" server CPX02, featuring 1 vCPU, 1 GB RAM and 20 GB storage, at our European locations (FSN1, HEL1 and NBG1) and in Singapore (SIN)."
  - Vendor fit: "particularly suitable for applications with very low resource usage and minimal system requirements, such as static websites, blogs or simple single-service web applications."
  - Card: €6.49/mo excl. VAT with IPv4 `[raw]`. Card reads "currently unavailable" `[raw]`. Unresolved.

- **2026-07-07. CPX12 added (EU).** `[news]`
  - "...the "Regular Performance" cloud server CPX12 with 1 vCPU, 2 GB RAM, and 40 GB disk space is now also available in our European locations (FSN1, HEL1, and NBG1)."
  - Vendor fit: "ideal for single-purpose workloads with low resource requirements, such as small websites and personal blogs, private VPN/proxy services, chat servers, and bots."
  - Card: €11.99/mo excl. VAT with IPv4 `[raw]`. Card reads "currently unavailable" `[raw]`. Unresolved.

- **2026-06-15. Price adjustment for new orders and rescales.** `[news][price][press]`
  - `[news]`, dated 2026-05-28: "Starting on 15 June 2026, updated pricing for cloud servers will apply to new orders and rescales." "Existing servers are not affected by the price adjustment, as long as no rescaling is performed."
  - `[price]`: "The price adjustment took effect for new orders and cloud instance rescales starting on the 15 June 2026; 8 AM CEST." "All prices are excluding VAT."
  - `[price]`: "Please note that certain changes to servers with legacy pricing may trigger a switch to the current pricing." "For orders placed before 15 June 2026, but delivered after 15 June 2026, the previous prices will apply."
  - `[press]`: "adjust our prices for certain product lines for new orders effective today, 15 June 2026, 8:00 am (CEST)." Reason: "This is due to the ongoing challenges in the hardware procurement market."
  - Monthly, excl. IPv4, € (old → new) `[price]`:

    | tier | x86 (CX) | Arm (CAX) | Arm minus x86, old → new `[inferred]` |
    |---|---|---|---|
    | 2 vCPU / 4 GB | CX23 3.99 → 5.49 | CAX11 4.49 → 5.99 | 0.50 → 0.50 |
    | 4 vCPU / 8 GB | CX33 6.49 → 8.49 | CAX21 7.99 → 10.49 | 1.50 → 2.00 |
    | 8 vCPU / 16 GB | CX43 11.99 → 15.99 | CAX31 15.99 → 20.99 | 4.00 → 5.00 |
    | 16 vCPU / 32 GB | CX53 22.49 → 29.49 | CAX41 31.49 → 40.99 | 9.00 → 11.50 |

  - Other plans, same table: CPX22 (EU) 7.99 → 19.49. CCX13 (EU) 15.99 → 42.99.
  - IPv4 costs €0.50/mo excl. VAT `[docs]` primary-ips page. Card price = new excl. IPv4 + €0.50 `[raw]`.

- **2025-10-16. New server lines in EU and SIN.** `[news]`
  - "In the locations EU and SIN, server plans are no longer distinguished by hardware type, but by hardware generation."
  - "CAX plans run on an Arm-based platform using Ampere® CPUs."
  - CX Gen3: "They can run on either Intel® or AMD, depending on availability."
  - "Existing servers are not affected by the deprecation of CX Gen2 and CPX Gen1 plans. They will continue to work."
  - Lines: CPX Gen2 (x86 AMD, "Regular Performance"). CX Gen3 (x86, or CAX Arm64, "Cost-Optimized"). CCX (x86, dedicated, "General Purpose").

- **2025-10-07. DNS moved into Hetzner Console.** `[news]` "Integration into the Cloud API: Manage DNS zones via the Hetzner Cloud API." Relevant only if the relay needs a DNS name.

- **2025-06-25. Cloud Console renamed Hetzner Console.** `[news]` "The Cloud Console is now the Hetzner Console , reflecting our goal to unify all Hetzner products under one roof. Now live at: https://console.hetzner.com" Projects live in this Console. See section 5.

- Not relevant to setup: 2026-08-10 experimental platform, "Free during the experimental phase" `[news]`. 2025-08-26 feedback tool `[news]`.
- No image or app entry on the whats-new page after 2023-08-07 `[news]`. Image changes are in the changelog, section 3.

### Older entries still in force

- **2023-08-07. "Deploy to Hetzner Cloud" link.** `[news]` "If you would like to link to one of our Apps, you can do it now using this new URL: https://console.hetzner.cloud/deploy/{app-name}." Opens the create page with the app preselected. Current domain and path: not verified.
- **2023-03-10. Apps.** `[news]` Owncast, PhotoPrism, RustDesk added. "the RustDesk App turns your server into a ready-to-go remote desktop server."
- **2023-04-12. Arm plans introduced.** `[news]` "you can now also create servers with Arm-based architecture (Ampere)." Vendor claim: "the Arm64 architecture makes it possible to get way more compute cores." No benchmark read.
- **2023-09-19. CAX in three locations.** `[news]` "Up until now, server plans with Arm64 architecture were only available in Falkenstein." Nuremberg and Helsinki added. FSN1 status now: see Open.
- **2024-08-06. Singapore.** `[news]` "Singapore is available for all cloud servers with AMD processors, and all cloud features." Singapore: AMD (CPX) only per this entry.
- **2022-06-08. Networking options and Primary IPs.** `[news]` "Because of the new options, servers and IPs are now billed separately." Options: server with IPv4 and IPv6; server with one public IP (IPv4 or IPv6); server without public IP. "To keep your Primary IP even if you delete the server it is assigned to, you can simply disable the "Auto Delete" option." Auto Delete implied on by default `[inferred]`. IPv6-only server: `--without-ipv4` `[help]`. Price effect: not verified.
- **2024-06-06. CX22 to CX52 introduced.** `[news]` Older CX11 to CX51 closed for order via API from 2024-09-06. CX22 is not on the current page `[raw]`.
- **2020-08-11 and 2021-09-17. Firewalls.** `[news]` 2020-08-11: "Our firewalls are "stateful" and thus allow easy configuration." 2021-09-17 general availability: "restricting certain TCP, UDP ICMP, ESP and GRE traffic." Matches section 1b.

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
- hcnet (beta, 2026-10-20) `[raw]` hcnet page: "Cloud Firewalls are stateful and hcnet implements them using eBPF." Connection tracking "may also differ in some details." When the table fills, "traffic that relies on connection tracking will be disrupted." "No fragment tracking is done for IPv6."

---

## 2. Server types, prices, locations

Page text `[raw]`, hetzner.com/cloud/cost-optimized/, 2026-10-20. Card prices, excl. VAT, include IPv4 (label "Price incl. IPv4"). Card Details: "eu-central NBG1 HEL1".

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
- Excl. IPv4 `[price]`: CX23 €5.49, CAX11 €5.99. IPv4 €0.50/mo excl. VAT `[docs]`. Sums equal the card prices `[raw]`.
- Price adjustment effective 2026-06-15 `[price]`. Old and new table: see "Recent changes that matter".

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
  - Default: implied on. 2022-06-08 entry: "you can simply disable the "Auto Delete" option" to keep the IP `[news][inferred]`.
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
- Supporting `[news]`: "The Cloud Console is now the Hetzner Console" (2025-06-25). "When you open a project, the new dashboard provides an overview of all resources" (2024-09-04).
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
- Arm premium over matched x86, excl. IPv4 `[price]`: €0.50, €1.50, €4.00, €9.00 before 2026-06-15; €0.50, €2.00, €5.00, €11.50 after. `[inferred]` by subtraction.
- CX Gen3 runs on "either Intel® or AMD, depending on availability" `[news]`. CAX: Ampere® CPUs `[news]`.
- CAX first in Falkenstein (2023), then Nuremberg and Helsinki (2023-09-19) `[news]`. Card Details today: NBG1, HEL1 `[raw]`.
- Singapore: AMD (CPX) only `[news 2024-08-06]`.
- Smallest RAM: CPX02, 1 GB, EU and SIN `[news]`. 2-vCPU cost-optimized plans, CX23 and CAX11, both 4 GB `[raw]`. CPX11 (2 vCPU, 2 GB) is US-only in the summary `[docs]`.

---

## Open and unverified

- Prices and availability: raw text for CX/CAX and CPX02/CPX22; model summary for other CPX rows. Live values need `hcloud server-type list -o json` after token.
- Availability: live or static text not verified. Live order path not verified.
- Resolved: €5.49 excl. IPv4 `[price]` + €0.50 IPv4 `[docs]` = €5.99 card price `[raw]`.
- Lowercase API type names and `ubuntu-22.04`/`ubuntu-24.04` names: `[inferred]`.
- `--port 1-65535` for all UDP: `[inferred]`. Verify with `hcloud firewall describe aoa-relay-fw -o json`.
- Firewall delete while attached: not verified. Detach-first order: `[inferred]`.
- Primary IPv4 after server delete: Auto Delete implied on `[inferred]`. Check `auto_delete` first.
- `server ip -6` vs `public_net.ipv6.ip`: not verified.
- Billing FAQ dated 2020-07-07. Current terms: not verified.
- Projects: no creation route found. "Console only" inferred from absence.
- Changelog summary read 100,000 of 107,248 characters.
- One iroh workflow read. Others unread.
- Changelog 2026-09-08 `[log]`: Images field `deprecated` will be removed. CLI column `deprecated` breaks after removal `[inferred]`. Not tested (no token).
- CPX02 (2026-10-06) and CPX12 (2026-07-07) announced as available `[news]`. Price page marks both unavailable `[raw]`. Unresolved.
- CAX11 in FSN1: create link targets fsn1 `[raw]`. Card Details omit fsn1 `[raw]`. 2023 entry says CAX launched in FSN1 `[news]`. Unresolved.
- Default network stack for new servers: not on hcnet page `[raw]`.
- IPv6-only server (`--without-ipv4`): price effect not verified. Card labels say "Price incl. IPv4" `[raw]`.
- Price table: raw page `[price]`. Press release: WebFetch summary `[press]` only.
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

News, prices, hcnet (raw HTML, 2026-10-20):
- https://docs.hetzner.cloud/whats-new
- https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/
- https://docs.hetzner.com/cloud/technical-details/hcnet/

Press release (WebFetch summary):
- https://www.hetzner.com/pressroom/standardization-and-price-adjustment-of-our-server-products/

Third party, not authoritative `[3p]` (search snippets only):
- https://costgoat.com/pricing/hetzner
- https://stackvaluelab.com/hetzner-cx-cax-unavailable/
