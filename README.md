I apologize for the inconvenience caused by the  characters in the previous messages. These characters were unintended and resulted from formatting issues. To provide you with a clean and accurate README for the GitHub repository, here's the revised version without any extraneous characters:

---

# Telegram Media Downloader

A high-performance Telegram media downloader with pacman-style progress display.

## Features

- **Multi-channel support**: Download media from multiple Telegram channels simultaneously.
- **Concurrent downloads**: Enhance performance by downloading multiple media files concurrently.
- **Progress tracking**: Monitor download progress with a pacman-style display.
- **Automatic retries**: Automatically retry failed downloads to ensure all media is downloaded.
- **Rate limiting**: Manage download rates to comply with Telegram's usage policies.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/De3f4ault/telegram-media-downloader.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd telegram-media-downloader
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:

   - On Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

5. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Obtain Telegram API credentials**:

   - Visit [my.telegram.org](https://my.telegram.org/) and log in with your Telegram account.
   - Navigate to the "API Development Tools" section.
   - Create a new application to obtain your `api_id` and `api_hash`.

2. **Configure the downloader**:

   - Rename the `config_sample.json` file to `config.json`.
   - Edit `config.json` to include your `api_id`, `api_hash`, and the list of channels from which you want to download media.

3. **Run the downloader**:

   ```bash
   python telegram_downloader.py
   ```

   The script will start downloading media from the specified channels, displaying progress in a pacman-style format.

## Configuration

The `config.json` file should be structured as follows:

```json
{
  "api_id": "YOUR_API_ID",
  "api_hash": "YOUR_API_HASH",
  "channels": ["channel_username1", "channel_username2"],
  "download_path": "downloads/",
  "concurrent_downloads": 5,
  "retry_attempts": 3,
  "rate_limit": 1.0
}
```

- `api_id` and `api_hash`: Your Telegram API credentials.
- `channels`: A list of Telegram channel usernames from which to download media.
- `download_path`: The directory where downloaded media will be saved.
- `concurrent_downloads`: The number of media files to download concurrently.
- `retry_attempts`: The number of times to retry a failed download.
- `rate_limit`: The delay (in seconds) between API requests to prevent hitting Telegram's rate limits.

## Dependencies

The required Python packages are listed in the `requirements.txt` file and include:

- `telethon`: A Python Telegram client library.
- `tqdm`: A library for progress bars.
- `aiohttp`: An asynchronous HTTP client/server framework.

These dependencies will be installed when you run `pip install -r requirements.txt`.

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes.
4. Commit your changes: `git commit -m 'Add some feature'`.
5. Push to the branch: `git push origin feature-branch-name`.
6. Open a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [Telethon](https://github.com/LonamiWebs/Telethon) for the Telegram client library.
- [tqdm](https://github.com/tqdm/tqdm) for the progress bar utility.
- [aiohttp](https://github.com/aio-libs/aiohttp) for the asynchronous HTTP client/server framework.

For more information, visit the [GitHub repository](https://github.com/De3f4ault/telegram-media-downloader).

---

If you encounter any further issues or have additional questions, feel free to ask! 
