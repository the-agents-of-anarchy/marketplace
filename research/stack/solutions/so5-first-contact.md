# First contact and reachability: how projects solve it

Ten discovery mechanisms recur across the reports, plus one join gate. Some carry the address inside a ticket or invite. Others look it up through DNS, the Mainline DHT, mDNS, or a relay. Every row names its source line. Cells marked "(inferred)" are not stated in a report.

| Mechanism | Projects (report) | Needs always-on node? | Third-party service? | How the address is learned | Gate | Evidence |
|---|---|---|---|---|---|---|
| 1. Ticket carries the bootstrap address | walkie, alink (a1-walkie-alink); rayfish, mshr (r1-infra); habilis (a3-habilis); n0 chat example (p1-presence-n0) | Yes, the ticketed node must run (inferred) | No, unless the ticket names a relay | Inside the ticket: node id, relay URL, IP addresses | None in the ticket; see row 11 | f1b-iroh-discovery.md:13-15; a1-walkie-alink.md:27; r1-infra.md:47; p1-presence-n0.md:24 |
| 2. Single-use invite token | walkie, alink, rayfish, habilis, buzz (a2b-buzz), mcpmesh (a2-mcpmesh) | Yes, the inviting node must accept | No | Inside the invite: host address, coordinator id, or endpoint | Token compared in constant time; single use; expiry | a1-walkie-alink.md:29, 83; r1-infra.md:47-48; a3-habilis.md:36; a2b-buzz.md:18; a2-mcpmesh.md:70 |
| 3. Id resolved through a pkarr or DNS record | rendezvous and distributed-topic-tracker (p2-presence-trackers, via N0 preset); rayfish seed list (r1-infra); mshr pkarr lane (r1-infra); habilis public meshes (sp1-agent-gossip-architecture) | Publisher must run to publish (inferred) | Yes: n0 DNS and pkarr, or an operator's own server | Signed pkarr or DNS record, resolved from the node id | None | f1b-iroh-discovery.md:9; s2-tests.md:25; r1-infra.md:49, 53, 123; p2-presence-trackers.md:65; sp1-agent-gossip-architecture.md:56 |
| 4. Mainline DHT slot from passphrase or topic name | iroh-gossip-rendezvous, distributed-topic-tracker (p2-presence-trackers); habilis `dht` lookup (a3-habilis, sp1-agent-gossip-architecture) | No | Yes: public Mainline DHT, four default routers | Node ids read from slot records | Decrypting records needs the passphrase or initial secret; vouched ids get no further check | p2-presence-trackers.md:18-30, 41-47, 27; p3a-presence-apps.md:46 |
| 5. mDNS on the LAN | habilis (sp1-agent-gossip-architecture); rayfish, on by default (r1-infra); p2panda (p3b-p2panda); fofoca (s3-breadth) | No (inferred) | No | Multicast announce gives the LAN address | None | f1b-iroh-discovery.md:5-9; e1-api.md:15-16; r1-infra.md:54; p3b-p2panda.md:17 |
| 6. Relay URL in the address | habilis relay ladder (sp1-agent-gossip-architecture, a3-habilis); mshr relays (r1-infra); rayfish relay preset (r1-infra); p2panda, opt in (p3b-p2panda) | Yes, the relay must run | Yes: n0 default relays, or an operator's relay | Relay URL sits in the address; a relay does not resolve ids | None | e1-api.md:9b, 9e, 9f; sp1-agent-gossip-architecture.md:52, 55; r1-infra.md:86, 117; p3b-p2panda.md:85 |
| 7. Pinned seed in config or environment | mshr (r1-infra). Rayfish has no config-file list (r1-infra:84) | Yes, the seed must run | No | Config or env var supplies the address | None | r1-infra.md:97, 115-117, 147, 156 |
| 8. Address book plus PSI topic hashes | p2panda (p3b-p2panda) | No (inferred): any known node serves | No | Discovery peers share transport info; default shares all known nodes | 32-byte topic secret the app supplies; PSI reveals only shared topics | p3b-p2panda.md:34-44, 62-64 |
| 9. Open topic name, no secret | habilis topic meshes (a3-habilis, sp1-agent-gossip-architecture); mcpmesh presence by org id (a2-mcpmesh); tunnet by network UUID (p3a-presence-apps); iroh-rings open ring (i2-admission) | No | No | Name yields the topic; address comes from rows 3 to 6 | Knowing the name is the gate, except where a per-connection gate applies | a3-habilis.md:37; a2-mcpmesh.md:49; p3a-presence-apps.md:64; i2-admission.md:35 |
| 10. Bearer join id carrying a seed | habilis (a3-habilis, sp4-habilis-network-internals) | No | No | Join id decodes to mesh config; lookups from rows 4 to 6 | Possession of the join id; a bearer credential | a3-habilis.md:36; sp4-habilis-network-internals.md:57 |
| 11. Per-connection gate after dial | iroh-auth (i1-auth); chio and iroh-rings (i2-admission); mcpmesh (a2-mcpmesh); walkie (a1-walkie-alink) | n/a | No | n/a: peer is already dialed | SPAKE2 on a shared secret; signed directory membership; operator allowlist by EndpointId; trust gate before gossip ALPN; pinned key after first accept | i1-auth.md:15-18; i2-admission.md:16, 34; a2-mcpmesh.md:47; a1-walkie-alink.md:29 |

## Each mechanism in two or three sentences

1. **Ticket carries the address.** The ticket holds one endpoint address: id, relay URL, and IP addresses. It carries no name or secret, so an invite needs a container of its own.

2. **Single-use invite token.** The inviting node checks a token once, in constant time, and burns it on join. Walkie pins the joiner's key after the first accept. Alink defaults to a 24-hour invite. Rayfish invites are single use with expiry.

3. **Pkarr or DNS record.** The node id resolves to an address through a signed record. Rayfish also stores its seed list in a record under the network key, so a joiner reads seeds without a config file.

4. **Mainline DHT slot.** Nodes write encrypted, signed peer lists to public DHT slots. A newcomer reads the slots and joins whatever ids it finds. The report says the spec's D14 rejects this option.

5. **mDNS.** LAN peers find each other by multicast. It is not in iroh's core presets and must be added to the builder.

6. **Relay URL in the address.** A relay path lets a dialer connect with only a relay URL, then upgrade to a direct path. The relay does not turn an id into an address.

7. **Pinned seed.** The operator supplies a seed address in config or environment. Rayfish has no such list, which the report records as a counterexample to the spec's form.

8. **Address book and PSI.** A node picks a bootstrap from its address book and walks outward. Two peers learn only their shared topics through hashed exchange.

9. **Open topic name.** A topic is a string or public id. Anyone who knows it can derive the rendezvous identity. The gate is the name itself.

10. **Bearer join id.** Possession of a 32-byte seed in the join id admits a node to the mesh. The report calls this a bearer credential.

11. **Per-connection gate.** After a dial succeeds, the node checks identity, a shared secret, a signed grant, or an allowlist. None of these checks each gossip message.

## What the measurement says (e1-api check 9)

| Check | Setup | Result |
|---|---|---|
| 9a | Id only, relays off, no lookup | FAIL in 148 microseconds: "No addressing information available" |
| 9b | Id only, shared relay, no lookup | FAIL in 135 microseconds: a shared relay does not resolve ids |
| 9c | Id only, shared relay, mDNS | PASS in 0.74 s over the LAN IP |
| 9d | Id only, relays off, mDNS | PASS in 0.74 s over the LAN IP |
| 9e | Id plus relay URL, no direct address, no mDNS | PASS in 4.8 ms via relay; upgraded to LAN IP within 3 s |
| 9f | Same as 9e with IP transports off | PASS in 4.3 ms, relay only |

The address must reach the dialer. An id alone fails without a lookup. An id plus a relay URL works. The report's own conclusion: "Estafette needs a ticket, a lookup, or mDNS for first contact."

The gossip gate report says a node holding the topic id and one bootstrap id joins (v2-gossip-gate.md:7). Check 9 says a bare id does not dial. Those two claims conflict unless the bootstrap address is resolved first.

Caveats the report gives:

- One macOS host, one run per check, debug build, single timing samples.
- Preset `Minimal`, not `N0`. With `N0`, id-only dial could query pkarr and succeed, so 9a and 9b may differ on a networked host.
- The sandbox firewall blocked outbound calls, so the pkarr path was never exercised.
- mDNS used the custom service name `e1spike`, not the default. Default-name behaviour is untested.
- mDNS needs a multicast-capable LAN interface. A host without one may fail 5c, 9c, and 9d.

## Not found in the reports

- No admission hook in iroh-gossip. A search of `src/` for authorization, allowlist, and hook terms found nothing (v2-gossip-gate.md:17).
- No network-wide shared secret or keyed MAC in any surveyed project (a2-mcpmesh.md:150; p2-presence-trackers.md:67).
- No live Mainline DHT or relay run in any report (p2-presence-trackers.md:14, 86).
- No pkarr or N0 run. The e1 pkarr path was never exercised.
- The read-side DHT signature check in the rendezvous project was not traced (p2-presence-trackers.md:24).
- Vouching in the rendezvous project was only partly read (p2-presence-trackers.md:27, 82).
- No invite format carries name and secret inside an EndpointTicket (f1b-iroh-discovery.md:18).
- No iroh-gossip join admission check was verified beyond grep (p3b-p2panda.md:120).
- The d1-irpc and d2-direct-apps reports have zero matches for the search terms.
