# Liverpool FC Ballot Checker 🎫

I have missed almost every local members ballot this season, with the current state of Liverpool's ticketing system I never seem to win any of the members ballots. I find my best chance is with the local members ballots, so I created a bot that can let me know when those ballots are open.

This script can be used to monitor Liverpool FC's ticket ballot availability and receive SMS notifications when local member ballots open.

## Features

- 🔍 Monitors Liverpool FC's ticket page for local member ballot availability
- 📱 Sends SMS notifications via Twilio when ballots open
- 🔄 Includes caching to prevent duplicate notifications
- 🤖 Headless browser automation with Playwright
- ⏰ Can be configured to run as a cron job

## Prerequisites

- Python 3.x
- Make
- A Twilio account for SMS notifications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/A-Georgiou/Liverpool-FC-Ballot-Notifier.git
cd Liverpool-FC-Ballot-Notifier
```

2. Create a `.env` file in the project root with your Twilio credentials:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_MESSAGING_SERVICE_SID=your_messaging_service_sid
NOTIFICATION_RECIPIENTS=+44123456789,+44123456789
```

3. Run the following command to create virtual environment and setup dependencies:
```bash
make setup
```

## Usage

### One-time run
```bash
make run
```

### Setting up automated monitoring

To run the checker periodically, add the following to your crontab:

1. Open your crontab:
```bash
crontab -e
```

2. Add a line to run the checker (e.g., every 6 hours):
```bash
0 */6 * * * cd /path/to/Liverpool-FC-Ballot-Notifier && make cron
```

### Cleaning up

If you wish to remove the virtual environment and cached files, you can run:
```bash
make clean
```

## Logs

When running as a cron job, logs are written to `/var/log/ticket_monitoring.log`. Make sure this path is writable by the user running the cron job.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_MESSAGING_SERVICE_SID` | Your Twilio Messaging Service SID |
| `NOTIFICATION_RECIPIENTS` | Comma-separated list of phone numbers to notify |

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
I am more then happy to extend this to work with other teams, the actual script to scrape the availability is quite crude so feel free to contribute and make changes and extend the logic as needed.