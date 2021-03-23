#!/bin/bash
docker run -ti --mount type=bind,source="$(pwd)"/.,target=/app --network test-net python bash
