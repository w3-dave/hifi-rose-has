# Get Current State

Poll the current state of the HiFi Rose Streamer (power, volume, input source).

## CURL Request

```bash
curl -X POST http://192.168.0.102:9283/get_current_state \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Parameters

- Empty JSON object `{}` required

## Response Format

The API returns a JSON response with the following structure:

```json
{
  "data": {
    "volume": 50,
    "isPlaying": false,
    "isPowerOn": true,
    "tempArr": [
      "funcMode:1",
      "..."
    ]
  }
}
```

## Example Response (while device is off)
```json
{
  "code": "SLEEP",
  "status": {
    "errorCd": "",
    "errorMsg": "",
    "outs": "OK"
  },
  "version": "1.0.9"
}
```

## Example Response while playing

```json
{
  "data": {
    "albumName": "festival anthems [sat]",
    "artistName": "Unknown",
    "buf": 15,
    "buffer": "0",
    "curPosition": "0",
    "duration": "168000",
    "favCnt": 0,
    "isFavorite": false,
    "isFile": false,
    "isHdmiOn": true,
    "isPlaying": true,
    "isServer": false,
    "path": "/storage/ROSEDISK/Various Artists/Unknown/festival anthems [sat]/13 - Unknown Track.WAV",
    "playState": "",
    "playType": "MUSIC",
    "repeatMode": 0,
    "shuffleMode": 0,
    "subAppCurrentData": {
      "isCache": false,
      "isDirect": false,
      "mMusicSongInfo": {
        "album": "festival anthems [sat]",
        "album_art": "81/81d0694df8ba6a4bc1a2340401b2b4e9d4/0",
        "album_id": 0,
        "album_key": "QYHQaU34umpLwaI0BAGytOnU",
        "artist": "Unknown",
        "artist_id": "UR805VPyTtrb1HJh5oNiaCQS",
        "composer": "Unknown",
        "composercnt": 0,
        "data": "/storage/ROSEDISK/Various Artists/Unknown/festival anthems [sat]/13 - Unknown Track.WAV",
        "discIndex": "0001",
        "duration": "00168306",
        "favCnt": 0,
        "gener_song_cnt": 0,
        "generid": "YR805VPyTtrb1HJh5oNiaCQS",
        "genernm": "Unknown",
        "id": "ImYmMkwDMHGyRYyWuhvtncdb",
        "idx": "6591",
        "isSelected": false,
        "modifyTime": "2022-01-14T00:21:20+0000",
        "num_of_song": 0,
        "num_of_tracks": 0,
        "title": "13 - Unknown Track",
        "trackIndex": "0001",
        "track_id": "ImYmMkwDMHGyRYyWuhvtncdb"
      }
    },
    "tempArr": [],
    "thumbnail": [
      "http://192.168.0.102:8000/v1/albumarts/81/81d0694df8ba6a4bc1a2340401b2b4e9d4/0",
      "isScan:false",
      "isShareFile:false",
      "isCloudFile:false",
      "audioId:ImYmMkwDMHGyRYyWuhvtncdb",
      "isDlnaFile:false"
    ],
    "titleName": "13 - Unknown Track",
    "trackInfo": "wav 16bits 44.1kHz 2ch 1411kbps",
    "ui_state": 0,
    "volume": 0
  },
  "code": "G0000",
  "status": {
    "errorCd": "",
    "errorMsg": "",
    "outs": "OK"
  },
  "version": "1.0.9"
}
```

## Response Fields

- **volume**: Integer 0-100 representing current volume level
- **isPlaying**: Boolean indicating if media is currently playing
- **isPowerOn**: Boolean indicating power state
- **tempArr**: Array containing various state information
  - Look for `"funcMode:X"` string to determine input source (1-5)

## Parsing Current Input Source

The current input source is embedded in the `tempArr` array as a string:
- `"funcMode:1"` = LINE IN
- `"funcMode:2"` = OPTICAL IN
- `"funcMode:3"` = eARC IN
- `"funcMode:4"` = USB IN
- `"funcMode:5"` = AES/EBU IN

## Example with Output

```bash
curl -X POST http://192.168.0.102:9283/get_current_state \
  -H "Content-Type: application/json" \
  -d '{}' | jq
```

## Notes

- Replace `192.168.0.102` with your device's IP address
- This endpoint is used for polling to keep state synchronized
- Volume values of 0 or invalid values should be ignored (API quirk)
- Device is considered "ON" if either `isPlaying` or `isPowerOn` is true
