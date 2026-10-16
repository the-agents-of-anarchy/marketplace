# irpc vs hand-written direct protocol

Date 2026-10-16. Toolchain 1.99.1, macOS (Darwin 24.3, aarch64 allocator behavior). iroh 1.3.0, noq 1.3.0, irpc 0.17.0, irpc-iroh 0.17.0, irpc-derive 0.17.0, postcard 1.1.3, iroh-gossip 0.101.0.

Built and ran two prototypes of the 3.6 exchange in `/tmp/ra-v3/proto` (edition 2024, release build): `src/hand.rs` (iroh bi-streams, postcard, `read_to_end(1_114_112)`) and `src/viairpc.rs` (irpc + irpc-iroh). Shared types, handler logic, counting allocator and scenario harness: `src/lib.rs`, `src/harness.rs`. Two endpoints in one process, loopback, `RelayMode::Disabled`. Raw outputs: `/tmp/ra-v3/hand.out`, `/tmp/ra-v3/viairpc.out`. Tree experiments: `/tmp/ra-v3/tree-base`, `tree-irpc`, `tree-nopc`.

Finding that changes the question: irpc 0.17.0 alone does not speak iroh. Its `rpc` module is typed on `noq::Connection`. iroh's `Connection` hides its inner noq connection. The iroh transport is a separate crate, `irpc-iroh` 0.17.0, absent from the tree today. iroh-gossip enables irpc with `derive, stream, spans` only: in-process channels, no remote transport (iroh-gossip Cargo.toml:161-170; tree shows irpc `[derive,spans,stream]`).

## irpc 0.17.0 facts (file:line)

- **Framing.** Request: postcard varint u64 length, then postcard of the request enum. `irpc-0.17.0/src/lib.rs:2133-2140` (`prepare_write`), `util.rs:292-302` (`write_length_prefixed`). Response per request type: varint length, then postcard (`lib.rs:2174-2190`). There is no response enum on the wire: each request variant has its own response type. 3.6's `Response = A | B | C` becomes three response types; wire bytes differ from the spec text.
- **Streams.** One bi-stream per request. The server loops on `accept_bi` per connection (`irpc-iroh/src/lib.rs:301-306`).
- **Remote node id.** The `Handler` type is `Fn(R, RecvStream, SendStream)` (`irpc-0.17.0/src/lib.rs:2449-2454`). It carries no connection. `IrohProtocol` (`irpc-iroh/src/lib.rs:190-232`) therefore cannot show the handler a node id. Only workaround: write your own `ProtocolHandler` that calls `irpc_iroh::read_request` (`:312`) in your own loop with `conn.remote_id()` in scope. I did that.
- **Max frame.** `pub const MAX_MESSAGE_SIZE: u64 = 16 MiB` (`irpc-0.17.0/src/lib.rs:1927`). Constant. No config field, builder, or feature. The 1,114,112 limit of 3.14 cannot be set. A handler can only check after the full body is read and decoded.
- **Allocation vs decode.** Server: read varint, compare with 16 MiB, then `vec![0; size]` of the declared size, then `read_exact`, then `postcard::from_bytes` (`irpc-iroh/src/lib.rs:411-436`, alloc at `:424`). Allocation happens before any body byte arrives, sized by the peer's claim.
- **Malformed or oversize.** Size > 16 MiB: `connection.close(code 1)` (`:417-421`), killing every stream on that connection. Decode or short-read error: `read_request_inner` returns `Err`. `handle_connection` propagates with `?` (`:301-305`), `IrohProtocol::accept` maps it to `AcceptError`, and the connection is closed.
- **Per-connection serialization.** The request loop reads each full request body before taking the next stream (`:301-305`). A stalled body blocks later streams on that connection.
- **Timeouts.** None. `grep -c timeout` is 0 in both `irpc` and `irpc-iroh` lib.rs.
- **Client.** `irpc_iroh::client::<S>(endpoint, addr, alpn)` is lazy, reconnects (`irpc-iroh/src/lib.rs:31-37`).
- **Macro.** `#[rpc_requests]` emits `::tracing::...` (`irpc-derive/src/lib.rs:224,315`). The user crate needs a direct `tracing` dependency.

## Prototype results

| Measure | irpc | by hand |
|---|---|---|
| Lines, protocol file, non-blank | 51 | 41 |
| Lines, excluding `use` and blank | 47 | 39 |
| Server handler incl. node id exposure (non-blank) | 18 lines, custom `ProtocolHandler` + `read_request` loop | 26 lines, custom `ProtocolHandler` |
| Protocol declaration (enum + channel types) | 10 lines | 0 (shared `Request`/`Response` serve) |
| Client (non-blank, incl. `frame` helper) | 17 lines (per-variant mapping to three response types) | 11 lines |
| Three variants round trip, node id seen by handler | pass | pass |
| Direct dependency needs beyond iroh/serde/postcard | `irpc`, `irpc-iroh`, `tracing` | none |
| Variant named `Message` (spec name) | compile error (ambiguous with `Service::Message`, deny lint on 1.99.1); renamed `Deliver` | fine |
| Release binary size | 16,353,824 B | 15,709,216 B |
| 2,000,000-byte body, real client call | accepted, `Ok(response)`, 31 ms | rejected, client `Err(stream reset by peer: error 1)`, 24 ms |
| Same, raw frame | handler ran with the 2 MB body, ack returned | server rejected, client read `Err(stream reset by peer: error 1)` |
| Largest single server allocation, 2 MB request | 2,000,053 B | 40,960 B |
| Request of 100,000 bytes arrived of a declared 2,000,053, not finished | 2,000,053 B allocated up front | 16,384 B max single; live delta 187,668 B |
| 4-byte header declaring 16 MiB, then idle | 16,777,216 B allocated | not applicable (no header; 3,608 B) |
| 20 connections, each 4-byte header declaring 16 MiB | live heap +339,057,891 B; RSS +18,608 KiB (32,544 to 51,152 KiB) | live heap +3,345,202 B; RSS 27,600 to 29,712 KiB |
| Header declaring 20,000,000 | connection closed by server, code 1 | n/a (bytes are junk; stream waits, then reset when connection ends) |
| 64 bytes of 0xFF, finished | connection closed (client sees `connection lost`; close code 0) | stream reset code 1, connection alive, next probe on it answered |
| Truncated valid frame, finished | connection closed | stream reset code 1, connection alive, next probe answered |
| Stalled partial request, then a probe on the same connection | probe times out (3 s): blocked behind the stalled body | probe answered (one task per stream) |

## Oversize behavior (observed)

2,000,000-byte Message, limit 1,114,112:

- **irpc.** The server accepts it. Declared 2,000,053 is below 16 MiB, so it allocates 2,000,053 B zeroed, reads all of it, decodes, and the handler sees a 2 MB body. The limit is unenforceable inside irpc. The client gets a normal response. Connection stays alive.
- **By hand.** `read_to_end(1_114_112)` accumulates chunks and returns `TooLong` once received bytes pass the limit (noq `recv_stream.rs:546-559`). Largest single allocation observed: 40,960 B. The body never became one buffer. My handler then calls `rx.stop(1)` and `tx.reset(1)`. The client's read fails with `stream reset by peer: error 1`. Connection stays alive and the next request on it succeeded. Worst case on the accept path is the received chunks plus one final contiguous buffer, about 2 x limit (`recv_stream.rs:560-571`).
- **Claim-then-stall.** irpc allocates the claimed size before receiving the body: 16 MiB from a 4-byte message. Requested heap grew 339 MB for 20 connections. Physical RSS grew only about 18 MiB because `vec![0; n]` maps zero pages lazily on this OS. I measured requested bytes and RSS, not what a Linux container with strict overcommit would charge. By hand, memory tracks bytes that actually arrived.

## Tree cost

`cargo tree -e normal --prefix none | sort -u`, base = iroh 1.3.0 + iroh-gossip 0.101.0 + postcard + serde + tokio (249 lines). postcard 1.1.3, serde and tokio are in the base tree even with postcard removed from the manifest (246 lines).

| Path | New crates over base | irpc features |
|---|---|---|
| by hand | 0 | irpc stays `[derive,spans,stream]` (gossip's) |
| irpc | 4: `irpc-iroh 0.17.0`, `rcgen 0.14.10`, `pem 4.0.0`, `yasna 0.6.0` | `[default,derive,noq_endpoint_setup,rpc,spans,stream]` |

`irpc-iroh` depends on `irpc` with default features (`irpc-iroh-0.17.0/Cargo.toml:85-86`), so `noq_endpoint_setup` and certificate generation (rcgen, pem, yasna) arrive even though iroh supplies the TLS. They cannot be switched off from a dependent crate while `irpc-iroh` is used. Plus a direct `tracing` dependency for the macro. Release binary +644,608 B (about 4%).

## Verdict

Write it by hand. The decisive evidence is that irpc 0.17.0 cannot enforce the 1,114,112-byte wire limit of 3.14: its frame cap is a fixed 16 MiB constant, so the 2,000,000-byte request in my run was fully allocated, decoded and handled, and a 4-byte header claiming 16 MiB made the server allocate 16 MiB before reading any body (336 MB requested across 20 connections). By hand, `read_to_end(1_114_112)` rejected the same request without ever holding it as one buffer (largest allocation 40,960 B), reset only that stream, and kept the connection. irpc also gives the handler no node id, so the spec's step 4 (`from.node` equals the remote node id) forces a custom accept loop anyway, which leaves the irpc server loop about as large as the hand one (the irpc handler is shorter, 18 vs 26 lines, but the irpc path adds a 10-line protocol declaration and a larger client, 47 vs 39 code lines in total) and left it serializing streams per connection (a stalled body blocked the next probe) and closing the whole connection on any malformed frame. It adds four crates, three irpc features, a direct tracing dependency, a variant-name collision with the spec's `Message`, and a wire format that differs from the 3.6 text (length prefixes, no response enum). What irpc offers (streaming channels, local/remote duality, 0-RTT) is unused by 3.6, which is one request and one response per stream.

## What could make this wrong

- **Single run, loopback, one OS.** No repeats, no timing statistics. Timings (24 ms, 31 ms) are not benchmarks. Allocator behavior and the lazy zero-page effect are macOS specific as measured; Linux may differ in either direction.
- **Same-process noise.** `peak_live_delta` includes the client's send buffers (4,047,675 B for irpc, 2,202,658 B by hand on the 2 MB case). I relied on `max_single` and the 20-connection S9 heap delta for server-side claims. S9 live heap also includes client-side QUIC state, equal in both runs.
- **My handler choices.** The hand server resets with code 1 and spawns a task per stream. The irpc server returns `Err` on any read error, mirroring the library's own `handle_connection`. A variant that `continue`s on `InvalidData` kept the connection alive for the 0xFF case (client read `Ok(0 bytes)`), but the truncated-frame case (`UnexpectedEof`) still closed it. I did not find a way to avoid the per-connection serial body read through the public irpc API.
- **Cap workaround not tried.** One could wrap or fork `read_request_inner` to add a limit. That is the hand-written path with irpc's macro on top, and it forfeits the dependency's stability.
- **Both paths lack a server-side read timeout.** A stalled stream holds a task (hand) or blocks the connection (irpc) until the connection closes. 3.14 lists no such timeout. This is a spec gap on either path, not a differentiator.
- **Not tested.** irpc streaming channels, `rpc_0rtt`, `Router` with many ALPNs, behavior under packet loss, relay paths, behavior of irpc versions after 0.17.0 (a configurable cap could appear), and the stock `IrohProtocol` (which cannot expose the node id, so I did not run it).
- **Line counts** are for my prototypes with minimal error handling. A production hand-written path would add the 3.6 validation order in both cases; that code is the same either way.
