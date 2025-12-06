# Power Off

Turn off the HiFi Rose Streamer.

## CURL Request

```bash
curl -X POST http://192.168.0.102:9283/remote_bar_order \
  -H "Content-Type: application/json" \
  -d '{
    "barControl": "remote_bar_order_sleep_on_off",
    "value": "-1"
  }'
```

## Parameters

- **barControl**: `"remote_bar_order_sleep_on_off"` (fixed value)
- **value**: `"-1"` (power off)

## Notes

- Replace `192.168.0.102` with your device's IP address
- The device must be accessible on port `9283`
- Response may be empty or contain status information
