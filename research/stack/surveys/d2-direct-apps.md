# D2: One request, one response, on raw iroh streams

Date: 2026-10-16.

## Sources read

- imsg, commit d05551b (`/tmp/ra-src/imsg`, crate version 0.1.0, depends on iroh 0.91 per `Cargo.toml:15`): `src/lib.rs` 1-200, 240-260, 290-420; `src/proto.rs` 1-246; `src/varint.rs` 1-40; `Cargo.toml`. The rest of `src/lib.rs` and `src/actor.rs` were grep-only.
- iroh, commit 0072d7d (`/tmp/ra-src/iroh`, version 1.3.0, `iroh/Cargo.toml:3`): `iroh/examples/echo.rs` (all), `iroh/examples/echo-no-router.rs` (all), `iroh/examples/auth-hook.rs` (grep plus 88-110, 130-138, 230-290, 320-355), `iroh/src/protocol.rs` 228-300, `iroh/src/endpoint/connection.rs` 569, 896-925.
- noq 1.3.0 (iroh's QUIC layer, `iroh/Cargo.toml:44`, registry copy at `~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/noq-1.3.0`): `src/recv_stream.rs` 264-290, 580-587; `src/send_stream.rs` 74, 180-215, 255.
- Spec `spec/blueprint.md`: 3.6 (lines 516-591) and the 3.14 limits table (lines 825-844).

## iroh 1.3.0 examples (echo, auth-hook)

### iroh examples (`iroh/examples/`, commit 0072d7d)

- What it does for this scope: `echo.rs` is the smallest ProtocolHandler. It copies one stream back to the sender. `auth-hook.rs` is a second small handler that reads a token from one uni stream and closes the connection with a code.
- How, in code:
  - Accept side: the handler is `impl ProtocolHandler for Echo` (`echo.rs:83`), called on a spawned task (`protocol.rs:262-263`). It takes `connection.remote_id()` (`echo.rs:90`), then `accept_bi()` (`echo.rs:95`), then `tokio::io::copy(&mut recv, &mut send)` (`echo.rs:99`), then `send.finish()` (`echo.rs:104`), then `connection.closed().await` (`echo.rs:108`).
  - Connect side: `open_bi` (`echo.rs:45`), `write_all` (`echo.rs:48`), `finish` (`echo.rs:51`), `read_to_end(1000)` (`echo.rs:54`), `conn.close(0u32.into(), b"bye!")` (`echo.rs:58`), `endpoint.close().await` (`echo.rs:62`).
  - Auth handler: `accept_uni` then `read_to_end(256)` (`auth-hook.rs:340-341`). It compares the token with `==` (`auth-hook.rs:343`). It closes with `CLOSE_ACCEPTED = 1` or `CLOSE_DENIED = 403` (`auth-hook.rs:137-138, 348, 350`). It records `connection.remote_id()` in an allowlist (`auth-hook.rs:342, 347`).
- Crates it uses: iroh 1.3.0, n0-error, tokio. Nothing else in the examples.
- Maturity: the examples are in the iroh repo at commit 0072d7d. Tests covering these examples: not checked.
- What estafette could take: pattern for the accept-read-respond sequence (see below). Pattern for explicit application close codes via `connection.close(code, reason)` (`auth-hook.rs:348`).
- Against the spec: see section "Against the spec".

### noq stream calls used by the examples (noq 1.3.0)

- `read_to_end(size_limit)` returns `Vec<u8>`. It fails with `ReadToEndError::TooLong` above the limit and discards all data read (`recv_stream.rs:264-270`). It is not cancel-safe (`recv_stream.rs:266-268`).
- `finish()` closes the send side. Writes after `finish` are an error. `reset()` remains allowed after `finish` (`send_stream.rs:180-188`).
- `stopped()` waits for the peer to receive all data (`send_stream.rs:255`, doc text above it). No source in scope calls it.
- `stop(code)` discards unread data and asks the peer to stop sending (`recv_stream.rs:276-290`).
- `write_all(&[u8])` (`send_stream.rs:74`).

### The smallest accept-read-respond sequence

Assembled from `echo.rs`, with the spec limit substituted for the echo copy. Error conversions omitted. The server side:

```rust
let remote = connection.remote_id();                       // echo.rs:90
let (mut send, mut recv) = connection.accept_bi().await?;  // echo.rs:95
let request = recv.read_to_end(LIMIT).await?;              // noq recv_stream.rs:270; echo uses copy instead, echo.rs:99
// validate: identity check, mac, parse; write error responses here
send.write_all(&response).await?;                          // noq send_stream.rs:74
send.finish()?;                                            // echo.rs:104
connection.closed().await;                                 // echo.rs:108
```

The client side:

```rust
let (mut send, mut recv) = conn.open_bi().await?;          // echo.rs:45
send.write_all(&request).await?;                           // echo.rs:48
send.finish()?;                                            // echo.rs:51
let response = recv.read_to_end(LIMIT).await?;             // echo.rs:54
conn.close(0u32.into(), b"bye!");                          // echo.rs:58
endpoint.close().await;                                    // echo.rs:62
```

The client's `read_to_end` returns only after the server finishes its send side (`iroh/src/lib.rs:193, 230`, doc comments, not read in full).

### Framing, encoding, ack, timeouts, identity, errors (iroh examples)

- Framing: none. The end of the request is the `finish` from the client. `echo.rs:51` and `echo.rs:54` use this. The client caps its read at 1000 bytes (`echo.rs:54`). The server copies without a cap (`echo.rs:99`).
- Encoding: none. Raw bytes in both examples.
- Ack: the response is the payload itself. Echo has no separate ack message. The ack in the spec's sense is written by `write_all` then `finish` (`send_stream.rs:74`, `send_stream.rs:189`).
- Timeouts: none in `echo.rs`, `echo-no-router.rs`, or `auth-hook.rs`. `connection.closed().await` at `echo.rs:108` waits without a bound.
- Identity: `echo.rs:90-91` reads and prints `remote_id()`. Nothing compares it with a payload. `auth-hook.rs:342-347` uses `remote_id()` as the allowlist key after a token check.
- Errors to responses: none. `protocol.rs:265-267` says returning `Err(AcceptError)` drops the connection and sends no code. The doc recommends `Connection::close` with an explicit code. `auth-hook.rs:348, 350` does this.
- Finish and close order: server `write` then `finish` (`echo.rs:104`) then `closed().await` (`echo.rs:108`). Client `finish` (`echo.rs:51`) then `read_to_end` (`echo.rs:54`) then `conn.close` (`echo.rs:58`) then `endpoint.close` (`echo.rs:62`). The comment at `echo.rs:106-107` says the remote closes the connection after it receives the response.
- The handler must await `closed()`. `protocol.rs:262-265` says the connection is dropped when `accept` returns if no clone remains.

## imsg (n0 messaging crate, commit d05551b, uses iroh 0.91)

### imsg

- What it does for this scope: a wrapper over an iroh connection that sends and receives length-delimited messages over streams. It has a control stream and user streams. Its lib docs say: "If you care about round trips, bytes and high performance then use the underlying QUIC API directly" (`src/lib.rs:4-6`).
- How, in code:
  - Framing: a QUIC varint length prefix, then the payload. Decoder: `src/proto.rs:198-215`. Encoder: `src/proto.rs:220-235`. The decoder reserves `frame_size` before checking it (`src/proto.rs:208-210`). The code has no maximum frame size (`src/proto.rs:206` and `src/proto.rs:224`, both TODO "Enforce a max frame size?").
  - Stream open: `open_bi` then the first frame is a `StreamType` varint (`src/lib.rs:108-117`). Accept side reads that frame and checks it (`src/lib.rs:138-157`).
  - Send: `writer.send(msg)` (`src/lib.rs:296`). A write stopped with `Closed` maps to `StreamError::RemoteClosed` (`src/lib.rs:303-309`). Any other write error maps to `Aborted` (`src/lib.rs:314-315`).
  - Receive: `reader.next()` (`src/lib.rs:342`). A `None` from the reader sets `EndOfStream` (`src/lib.rs:344-345`).
  - Close: `finish()` the send side (`src/lib.rs:370-375`), then `stop(Closed)` the recv side (`src/lib.rs:376-380`). Abort: `reset(Aborted)` and `stop(Aborted)` (`src/lib.rs:249-258`).
  - Error codes on the wire: stream codes `Dropped=0, Closed=1, Aborted=2, ControlStreamNotNeeded=3, ProtocolError=4` (`src/proto.rs:100-116`). Connection codes `Dropped=0, Closed=1, Aborted=2, ProtocolError=3, ImplementationError=4` (`src/proto.rs:141-157`). Codec errors close the connection with `ProtocolError` (`src/actor.rs:207`).
- Crates it uses (`Cargo.toml:13-20`): anyhow 1.0.98, bytes 1.10.1, iroh 0.91, n0-future 0.2, thiserror 2.0.12, tokio 1.46.1, tokio-util 0.7.15 (codec), tracing 0.1.41. No serde, no postcard.
- Maturity: last commit Aug 22 2025 (d05551b). The crate is at 0.1.0. Tests are in `src/lib.rs`, module tests from about line 584 (for example `test_stream_not_closed` at 584). Release count: not checked.
- What estafette could take: pattern. The stream open and close order (finish, then stop) and the write-error mapping (`RemoteClosed` versus `Aborted`) are reusable as described. Crate: nothing. It is pinned to iroh 0.91 and the spec pins 1.3.0.
- Against the spec: see section "Against the spec".

### Answers, imsg

- Framing: QUIC varint length prefix, no maximum (`src/proto.rs:198-215`). The spec's per-request framing needs no length prefix; stream finish delimits (3.6 says one request per stream).
- Encoding: none. The codec takes and returns `Bytes` (`src/proto.rs:183-236`). Serialization is the caller's job.
- Ack: none. imsg is a message stream, not a request-response protocol. A response is another message on the same stream (`src/lib.rs:296`, `src/lib.rs:322`). That pattern is not one request per stream.
- Timeouts: none. The grep for `timeout`, `Duration`, `sleep`, `deadline` in `src/` returns nothing.
- Identity: `src/lib.rs:88` reads `remote_node_id().unwrap()` for a tracing span only. No payload check. `unwrap` panics if the remote id is absent.
- Errors to responses: no responses. Failures become stream or connection codes (`src/proto.rs:100-157`).
- Finish and close order: finish, then stop (`src/lib.rs:370-380`). Close waits for the peer to close the connection (`src/lib.rs:177-182`, doc says "If it does not, this will block indefinitely.").

## Smallest imsg use for a single exchange

imsg adds nothing to the iroh sequence above for one request and one response. Its value to this scope is its framing and its stream-close ordering. The sequence above is smaller and uses fewer types.

## Cross-project observations

- Both sources end the request with stream finish, not a length prefix, in the single-exchange case. imsg adds a length prefix only because it carries many messages per stream.
- Neither source checks a payload identity against `remote_id()`. The closest is `auth-hook.rs:342-347`, which uses the remote id as an allowlist key after a token check.
- No source sends an application-level error response. All error signaling in the sources is a QUIC stream code or a connection close code.
- No source sets a timeout on a stream or connection operation.
- Accept-side reads with a cap: `auth-hook.rs:341` (256 bytes) and `0rtt.rs:151` (8 bytes, grep only). The echo server copies without a cap (`echo.rs:99`).

## Against the spec

- 3.6 validation step 4 (`from.node` equals the remote node id): no source performs this check. The nearest is `echo.rs:90` (remote id printed only) and `auth-hook.rs:342` (remote id as an allowlist key). The spec's step has no precedent in these sources.
- 3.6 steps 1 and 2 close the stream without a response. The natural `?` return in an accept handler sends no code (`iroh/src/protocol.rs:265-267`). Step 2 needs an explicit reset, stop, or connection close with a code. No source shows the reset form with an application code. `auth-hook.rs:348, 350` shows the connection-close form.
- 3.14 "wire structure, any" of 1,114,112 bytes maps onto `read_to_end(size_limit)` directly (`noq recv_stream.rs:270`). The sources do not contradict it. The echo server's uncapped copy (`echo.rs:99`) must not be copied.
- 3.6 "both sides close the stream": the server's receive side is already at end after `read_to_end`, so no stop is needed there. The spec does not say whether the connection closes. Echo closes it from the client side (`echo.rs:58`).
- The handler's `connection.closed().await` (`echo.rs:108`) has no timeout. 3.14 has no limit that covers a handler waiting on a peer. This is a gap the spec leaves open; the sources do not fill it.
- Ack timeout (10000 ms, 3.14): no timeout appears in any source read. Wrapping `read_to_end` or `closed()` in a timeout would be the app's job. No source shows that wrapper.
- Encoding (postcard, 3.6): no source uses postcard or any serializer on the wire.
- Framing of the d1 allocation point (3.14 limit versus declared frame size) is covered in `research/stack/surveys/d1-irpc.md` line 32. Not repeated here.

## Not read

- imsg: `src/actor.rs` (277 lines); the test bodies of `src/lib.rs` (from about line 584); `src/lib.rs` 200-240 and 420-1054 beyond grep.
- iroh examples: `auth-hook.rs` 30-88, 110-130, 150-230, 290-320; `0rtt.rs` (grep only); `connect.rs`, `transfer.rs`, `search.rs`, `listen.rs`, `incoming-filter.rs`, `screening-connection.rs` (grep only).
- iroh source: `iroh/src/lib.rs` 190-235 (grep only); `iroh/src/endpoint/connection.rs` outside the cited ranges.
- noq 1.3.0: only the four methods and two doc blocks named above.
- Release count and CI for both repositories.
