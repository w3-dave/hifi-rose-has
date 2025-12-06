# Set Volume

Set the volume level of the HiFi Rose Streamer.

## CURL Request

```bash
curl -X POST http://192.168.0.102:9283/volume \
  -H "Content-Type: application/json" \
  -d '{
    "volumeType": "volume_set",
    "volumeValue": 50
  }'
```

## Parameters

- **volumeType**: `"volume_set"` (fixed value)
- **volumeValue**: Integer from `0` to `100`
  - `0` = minimum volume (mute)
  - `100` = maximum volume

## Examples

Set volume to 25%:
```bash
curl -X POST http://192.168.0.102:9283/volume \
  -H "Content-Type: application/json" \
  -d '{"volumeType": "volume_set", "volumeValue": 25}'
```

Set volume to 75%:
```bash
curl -X POST http://192.168.0.102:9283/volume \
  -H "Content-Type: application/json" \
  -d '{"volumeType": "volume_set", "volumeValue": 75}'
```

## Notes

- Replace `192.168.0.102` with your device's IP address
- Volume changes made directly on the device may not be reflected when polling state (API limitation)
