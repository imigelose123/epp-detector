# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Install dependencies
uv sync

# Run the application
uv run python epp_detector.py -i <image.jpg>

# Run with specific LM Studio host/port
uv run python epp_detector.py -i <image.jpg> --host 192.168.1.100 --port 8080

# JSON-only output (for scripting)
uv run python epp_detector.py -i <image.jpg> --json-only
```

### Testing
No automated tests exist. Manual testing requires:
1. LM Studio running with a VLM model loaded
2. A test image file

## Architecture

This is a single-file Python CLI application (`epp_detector.py`) that uses the LM Studio Python SDK to perform vision analysis for industrial safety equipment detection.

### Key Components

- **`lmstudio` SDK**: Used for connecting to LM Studio, loading VLM models, and handling image inputs
- **`Chat` class**: The system prompt is passed to `Chat()` constructor, not via a separate `add_system_message()` method
- **`lms.prepare_image()`**: Converts image paths to handles that VLM models can process
- **Image workflow**: `lms.prepare_image()` → `chat.add_user_message(..., images=[handle])` → `model.respond(chat)`

### Important Notes

1. **VLM Model Required**: LM Studio must be running a Vision-Language Model (e.g., `qwen2-vl-2b-instruct`, `llava-v1.5-7b`, `fuyu-8b`), not a text-only LLM
2. **Sync API Timeout**: Default is 60 seconds, configurable via `--timeout` or `lms.set_sync_api_timeout()`
3. **System Prompt**: Keep concise - long prompts can cause model confusion about image availability
4. **Windows Compatibility**: Avoid emojis in output - use ASCII characters like `[+]`, `[*]`, `[!]` instead

### Dependencies

- `lmstudio>=1.5.0` - Official LM Studio Python SDK
- `pillow>=12.3.0` - Image handling (transitive dependency via lmstudio)

### Project Structure

```
epp-detector/
├── epp_detector.py    # Main CLI script
├── pyproject.toml      # uv project config
├── uv.lock            # Dependency lock file
└── README.md          # User documentation
```
