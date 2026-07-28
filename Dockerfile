# Dockerfile
FROM scratch
COPY target/wasm32-wasip1/release/*.wasm /hornet_edge_ai.wasm
ENTRYPOINT ["/hornet_edge_ai.wasm"]
