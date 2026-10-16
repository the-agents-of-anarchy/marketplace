# Direct protocol (spec 3.6) on irpc

Date: 2026-10-16.

Sources read: irpc at /tmp/ra-src/irpc, commit 37ce2e24d0c8aee200fed80c8db79f48f92b5550 (last commit 2026-10-14), Cargo.toml version 0.17.0 (line 3). Files: Cargo.toml; src/rpc.rs (1-70, 105, 396-500, 503-566, 596-626, 931-1040, 1081-1270); src/rpc/iroh_impl.rs (full); src/lib.rs (316-344, 600-660, 790-840); irpc-derive/src/lib.rs (158-182, 380-420, grep only); examples/authorized-request.rs (lines 1-30, 125-150, 250-498). iroh-gossip Cargo.toml read via `gh api` at its default branch on 2026-10-16, not pinned to 0.101.0. Spec: spec/blueprint.md 3.6 (lines 516-600) and the 3.14 table (825-844).

## irpc 0.17.0 (github.com/n0-computer/irpc, 37ce2e2; iroh dependency via feature `iroh`, workspace pin iroh = "1" with default features off)

- **What it is.** A typed streaming RPC over QUIC streams. A service is one enum of requests. Each variant names the type of its response channel. The server reads one request per stream and answers on that stream.

- **Wire format.** Each request is one bidirectional stream: a varint u64 length, then the postcard encoding of the request enum (src/rpc.rs:467-478). The writer rejects a body over 16 MiB (src/rpc.rs:105). The reader checks the same limit before reading the body (src/rpc.rs:1248-1251). The response is a varint length and postcard of that variant's response type, written on the same stream (src/rpc.rs:601-614). The send side closes when the stream is dropped, not by an explicit finish (src/rpc.rs:1182 comment; the `_tx` binding in src/lib.rs `rpc()`, around line 818). I did not verify this in the noq source. Span context is off by default (irpc-derive/src/lib.rs:168 and 419). When on, the body becomes the tuple `(Option<SpanContextCarrier>, msg)` (src/rpc.rs:443-446), which changes the bytes. A new stream opens per call (src/lib.rs:649).

- **Declaration, call, and handling.** Declaration: `#[rpc_requests(message = ...)]` on an enum, one `#[rpc(tx = oneshot::Sender<T>)]` per variant (examples/authorized-request.rs:328-342). Client: `Client::boxed(IrohLazyRemoteConnection::new(endpoint, addr, alpn))`, then `inner.rpc(req).await??` (examples/authorized-request.rs:467-481). Server: a custom `ProtocolHandler` whose `accept` reads `conn.remote_id()` and loops on `read_request::<P>(&conn)` (examples/authorized-request.rs:444-453). Each arm destructures `WithChannels { inner, tx, .. }` and calls `tx.send(res).await` (examples/authorized-request.rs:404-436).

- **Features and what each pulls** (Cargo.toml):
  - Always: serde, tokio (sync, macros), tokio-util, n0-error, n0-future.
  - `rpc`: noq (runtime-tokio), postcard (alloc, use-std), smallvec, tracing, derive_more, tokio io-util. It gates the transport module (src/lib.rs:317-342).
  - `iroh`: `rpc` plus the iroh crate, portable-atomic, and getrandom on wasm. It gates src/rpc/iroh_impl.rs (src/lib.rs:344).
  - `derive`: irpc-derive (syn 3, quote, proc-macro2). `spans`: tracing. `stream`: futures-util. `varint-util`: postcard, smallvec, tokio io-util. `noq_endpoint_setup`: rustls, rcgen, futures-buffered (test helpers).
  - Default: rpc, iroh, spans, stream, derive.
  - iroh-gossip 0.101.0 with its default `net` feature enables irpc with only derive, stream, spans (gossip Cargo.toml, `irpc` entry and `net` feature). So estafette's current irpc has no transport code. Its `rpc` feature enables irpc's `rpc` and `noq_endpoint_setup`.

- **Maturity.** Last commit 2026-10-14. 23 tags. Tests: tests/invalid_request.rs (11 tests, bad requests), tests/mpsc_channel.rs (13), tests/oneshot_channel.rs (5), tests/derive.rs (2), tests/compile_fail/ (trybuild), src/tests.rs (1).

- **Spec fit, decision by decision.**
  - 3.6 one request per bi-stream: fits. The client opens one stream per call (src/lib.rs:649). The server reads one request per stream (src/rpc.rs:1160-1200).
  - 3.6 Request as a union: fits. Each variant carries its own response type (examples/authorized-request.rs:332-338). A Message gets a bare MessageAck with no union tag. The client knows which it sent. A tagged response union on the wire needs one shared response enum as every variant's tx type.
  - 3.6 `v` and mac inside each structure: fits. They are plain fields that irpc never reads.
  - 3.6 "close the stream" on a bad request: conflicts with the default. A bad request resets its own stream (src/rpc.rs:1189-1192). The stock `Handler` then closes the whole connection unless `skip_bad_requests(true)` is set (src/rpc.rs module docs "Bad requests"; src/rpc.rs:1016-1032). A custom loop over `read_request` gets the error and decides (src/rpc.rs module docs).
  - 3.6 "close the stream without a response" on a bad MAC: fits. Dropping the response sender writes nothing, and the client sees the stream end (src/rpc.rs:547-549).
  - 3.6 server learns the remote node id: stock `IrohProtocol` does not. Its handler closure receives only the request and streams (src/rpc.rs:952-958; src/rpc/iroh_impl.rs `accept`). A custom `ProtocolHandler` gets it from `conn.remote_id()` (examples/authorized-request.rs:447).
  - 3.14 "wire structure, any" 1,114,112 bytes: conflicts. irpc fixes the cap at 16 MiB as a public constant (src/rpc.rs:105). No setting exists. The server allocates the full declared size before decoding or checking any MAC (src/rpc.rs:1248-1252). Keeping 1,114,112 means reading the frame by hand, which drops irpc's server read path.
  - 3.6 body 1,048,576 bytes: not checked by irpc. It must be checked in the handler.
  - 3.14 timeouts (connect 5000 ms, ack 10000 ms, probe 3000 ms, observer 3000 ms, departure 1000 ms): irpc has no timeouts (zero matches in src/). Callers must wrap each call. The lazy connection holds its tokio Mutex across `endpoint.connect` (src/rpc/iroh_impl.rs:99-135), so a slow connect blocks every caller to that peer.
  - Concurrency, not stated in 3.6: a connection's requests run one after another in the stock handler (src/rpc.rs:949-951, 1000-1010). The example serves them sequentially too (examples/authorized-request.rs:449-450). A slow Message handler stalls later requests from that peer.

- **What estafette could take.**
  - Crate: irpc with features `iroh` and `derive`, for the request enum and the client's `rpc` call. Postcard, tokio, serde, and tracing are already in the tree.
  - Pattern: the custom `ProtocolHandler` that reads `conn.remote_id()` and calls `read_request` in a loop (examples/authorized-request.rs:444-453).
  - Nothing: the stock `IrohProtocol` (no remote id), the 16 MiB cap (conflicts with 3.14), and the default bad-request close.

- **Line estimate for 3.6 (my estimate from the code read above, not measured).**

| Part | By hand, iroh streams and postcard | With irpc, 3.14 cap kept | With irpc, cap dropped |
|---|---|---|---|
| Framing: length prefix, 1 MiB cap, read and write | 30 | 30 | 0 |
| Server accept loop, per-stream dispatch, remote id | 50 | 50 | 25 |
| Client call and connection cache | 60 | 20 | 20 |
| Request and response enum | 25 | 25 | 25 |
| Structs, validation, MAC, timeouts (same in all) | 250 | 250 | 250 |
| Total | about 415 | about 375 | about 320 |

  With the 3.14 cap kept, irpc saves about 40 lines, roughly 10 percent. Only the client side and the enum gain. The server read path is hand-written either way. Without the cap, the saving is about 95 lines.

## Cross-project observations

- Single crate, no cross-project pattern. Two spec limits are absent from irpc and must be written by hand in either approach: the 3.14 frame cap and the 3.14 timeouts.

## Not read

- noq source: send-stream drop behavior, read limits, and whether noq versions unify with iroh 1.3.0's in estafette's lock.
- iroh 1.3.0 source: the version estafette uses. The clone at /tmp/ra-src/iroh was not checked against that version.
- irpc: derive expansion (only grep of irpc-derive/src/lib.rs), tests bodies, DOCS.md, CHANGELOG.md, irpc-opentelemetry, and examples other than authorized-request.rs.
- docs.rs pages for 0.17.0.
- iroh-gossip source: only its Cargo.toml, at its default branch, not the 0.101.0 tag.
