# Set Input Source

Switch between input sources on the HiFi Rose Streamer.

## CURL Request

```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{
    "funcMode": 1
  }'
```

## Parameters

- **funcMode**: Integer representing the input source
  - `0` = STREAMER
  - `1` = LINE IN
  - `2` = OPTICAL IN
  - `3` = eARC IN
  - `4` = USB IN
  - `5` = AES/EBU IN

## Examples

### Switch to Streamer
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 0}'
```

### Switch to LINE IN
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 1}'
```

### Switch to OPTICAL IN
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 2}'
```

### Switch to eARC IN
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 3}'
```

### Switch to USB IN
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 4}'
```

### Switch to AES/EBU IN
```bash
curl -X POST http://192.168.0.102:9283/input.mode.set \
  -H "Content-Type: application/json" \
  -d '{"funcMode": 5}'
```

## Notes

- Replace `192.168.0.102` with your device's IP address
- Input source changes sync correctly in both directions (device to API and vice versa)

