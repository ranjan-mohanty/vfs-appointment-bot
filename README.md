# VFS Appointment Bot

[![GitHub License](https://img.shields.io/github/license/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/blob/main/LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/ranjan-mohanty/vfs-appointment-bot?logo=GitHub)](https://github.com/ranjan-mohanty/vfs-appointment-bot/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/vfs-appointment-bot?logo=pypi)](https://pypi.org/project/vfs-appointment-bot)
[![Downloads](https://static.pepy.tech/badge/vfs-appointment-bot)](https://pepy.tech/project/vfs-appointment-bot)
[![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2Franjan-mohanty%2Fvfs-appointment-bot.json&style=flat&logo=GitHub&label=views)](https://github.com/ranjan-mohanty/vfs-appointment-bot)
[![GitHub forks](https://img.shields.io/github/forks/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/forks)
[![GitHub Repo stars](https://img.shields.io/github/stars/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/stargazers)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ranjan-mohanty/vfs-appointment-bot/build.yml)](https://github.com/ranjan-mohanty/vfs-appointment-bot/actions/workflows/build.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/21f1ecd428ec4342980020a6ef383439)](https://app.codacy.com/gh/ranjan-mohanty/vfs-appointment-bot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ranjan-mohanty/vfs-appointment-bot/badge)](https://securityscorecards.dev/viewer/?uri=github.com/ranjan-mohanty/vfs-appointment-bot)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/issues)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/ranjan-mohanty/vfs-appointment-bot)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Franjan-mohanty%2Fvfs-appointment-bot)](https://twitter.com/intent/tweet?text=Check%20this%20out%20&url=https%3A%2F%2Fgithub.com%2Franjan-mohanty%2Fvfs-appointment-bot)

This Python script(**vfs-appointment-bot**) automates checking for appointments at VFS Global portal in a specified country.

## Installation

The `vfs-appointment-bot` script can be installed using two methods:

### 1. Using pip

It is the preferred method for installing `vfs-appointment-bot`. Here's how to do it:

1. **Create a virtual environment (Recommended):**

   ```bash
   python3 -m venv venv
   ```

   This creates a virtual environment named `venv` to isolate project dependencies from your system-wide Python installation (**recommended**).

2. **Activate the virtual environment:**

   **Linux/macOS:**

   ```bash
   source venv/bin/activate
   ```

   **Windows:**

   ```bash
   venv\Scripts\activate
   ```

3. **Install using pip:**

   ```bash
   pip install vfs-appointment-bot
   ```

   This will download and install the `vfs-appointment-bot` package and its dependencies into your Python environment.

### 2. Manual Installation

For an alternative installation method, clone the source code from the project repository and install it manually.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ranjan-mohanty/vfs-appointment-bot
   ```

2. **Navigate to the project directory:**

   ```bash
   cd vfs-appointment-bot
   ```

3. **Create a virtual environment (Recommended):**

   ```bash
   python3 -m venv venv
   ```

   This creates a virtual environment named `venv` to isolate project dependencies from your system-wide Python installation (**recommended**).

4. **Activate the virtual environment:**

   **Linux/macOS:**

   ```bash
   source venv/bin/activate
   ```

   **Windows:**

   ```bash
   venv\Scripts\activate
   ```

5. **Install dependencies:**

   ```bash
   pip install poetry
   poetry install
   ```

6. **Install playwright dependencies:**

   ```bash
   playwright install
   ```

## Configuration

1. Download the [`config/config.ini`](https://raw.githubusercontent.com/ranjan-mohanty/vfs-appointment-bot/main/config/config.ini) template.

   ```bash
   curl -L https://raw.githubusercontent.com/ranjan-mohanty/vfs-appointment-bot/main/config/config.ini -o config.ini
   ```

2. Update the vfs credentials and notification channel preferences. See the [Notification Channels](#notification-channels) section for details on configuring email, Twilio, and Telegram notifications.
3. Export the path of the config file to the environment variable `VFS_BOT_CONFIG_PATH`

   ```bash
   export VFS_BOT_CONFIG_PATH=<your-config-path>/config.ini
   ```

**If you installed the script by cloning the repository (manual installation)**, you can directly edit the values in `config/config.ini`.

## Usage

1. **Command-Line Argument:**

   The script requires the source and destination country code ([as per ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)) to be provided as a command-line argument using the `-sc` or `--source-country-code` and `-dc` or `--destination-country-code` option.

2. **Running the Script:**

   There are two ways to provide required appointment details:

   - **Responding to User Prompts (recommended):**

     ```bash
     vfs-appointment-bot -sc IN -dc DE
     ```

     The script will prompt you to enter the required apponitment parameters for the specified country.

   - **Using `-ap` or `--appointment-params`:**

     Specify appointment details in a comma-separated (**not space-separated**) key-value format:

     ```bash
     vfs-appointment-bot -sc IN -dc DE -ap visa_center=X,visa_category=Y,visa_sub_category=Z
     ```

   The script will then connect to the VFS Global website for the specified country, search for available appointments using the provided or entered parameters, and potentially send notifications (depending on your configuration).

## Notification Channels

It currently supports three notification channels to keep you informed about appointment availability:

- **Email:** Sends notifications via a Gmail account.
- **Twilio (SMS & Voice Call):** Enables alerts through text messages and phone calls using Twilio's services.
- **Telegram:** Sends notifications directly to your Telegram account through a bot.

**Configuring Notifications:**

**Email:**

1. **Email Account:** You'll need a **Gmail account** for sending notifications.
2. **App Password:** Generate an app password for your Gmail account instead of your regular password. Refer to Google's guide for generating app passwords: [https://support.google.com/accounts/answer/185833?hl=en](https://support.google.com/accounts/answer/185833?hl=en).
3. **Configuration File:** Update your application's configuration file (`config.ini`) with the following details:

   - **`email` (Required):** Your Gmail address.
   - **`password` (Required):** Your generated Gmail app password.

**Twilio:**

1. **Create a Twilio Account (if needed):** Sign up for a free Twilio account at [https://www.twilio.com/en-us](https://www.twilio.com/en-us) to obtain account credentials and phone numbers.
2. **Retrieve Credentials:** Locate your account SID, auth token, and phone numbers within your Twilio account dashboard.
3. **Configuration File:** Update your application's configuration file (`config.ini`) with:

   - `auth_token` (Required): Your Twilio auth token
   - `account_sid` (Required): Your Twilio account SID
   - `sms_enabled` (Optional): Enables SMS notifications (default: True)
   - `call_enabled` (Optional): Enables voice call notifications (default: False)
   - `url` (Optional): Twilio API URL (Only needed if call is enabled)
   - `to_num` (Required): Recipient phone number for notifications
   - `from_num` (Required): Twilio phone number you'll use for sending messages

**Telegram:**

1. **Create a Telegram Bot:** Visit [https://telegram.me/BotFather](https://telegram.me/BotFather) to create a Telegram bot. Follow the on-screen instructions to obtain your bot's token.
2. **Configuration File:** Update your application's configuration file (`config.ini`) with:

   - **`bot_token` (Required):** Your Telegram bot token obtained from BotFather.
   - **`chat_id` (Optional):** The specific Telegram chat ID where you want to receive notifications. If omitted, the bot will send notifications to the chat where it was messaged from. To find your chat ID, you can create a group chat with just yourself and then use the `/my_id` command within the bot.

## Supported Countries and Appointment Parameters

The following table lists currently supported countries and their corresponding appointment parameters:

| Country                    | Appointment Parameters                                      |
| -------------------------- | ----------------------------------------------------------- |
| India(IN) - Germany(DE)    | visa_category, visa_sub_category, visa_center               |
| Iraq(IQ) - Germany(DE)     | visa_category, visa_sub_category, visa_center               |
| Morocco(MA) - Italy(IT)    | visa_category, visa_sub_category, visa_center, payment_mode |
| Azerbaijan(AZ) - Italy(IT) | visa_category, visa_sub_category, visa_center               |

**Notes:**

- Appointment parameters might vary depending on the specific country and visa type. Always consult VFS Global's website for the latest information.

## Known Issues

**1. Login Failures After Frequent Requests:**  
If the bot makes login requests to the VFS website too frequently, the VFS system might temporarily block your access due to suspected automation. This can lead to login failures.

- **Workaround:**
  - **Reduce request frequency:** Consider increasing the delay between bot runs to avoid triggering VFS's blocking mechanisms. You can adjust the interval in the configuration or code.
  - **Retry after 2 hours:** If you encounter a login failure, wait for at least 2 hours before retrying. The VFS block should expire within this timeframe.

**2. Occasional Captcha Verification:**  
The VFS website requires a CAPTCHA verification step during login. Currently, the bot does not have a built-in CAPTCHA solver.

- **Workaround:**
  - **Wait and Retry:** Sometimes, CAPTCHAs appear due to temporary website issues. Wait for a while and try again later.
  - **Retry in another browser:** CAPTCHAs are often solved automatically in the Firefox browser. If it still fails, retry the login process in another browser by setting `browser_type` to `"chromium" or "webkit"` in your `config.ini` file.

**Note:** We are constantly working to improve the bot's functionality. Future updates might include integrated CAPTCHA solving capabilities.

## Extending Country Support

This script is currently designed to work with the VFS Global website for Germany. It might be possible to extend support for other countries by modifying the script to handle potential variations in website structure and parameter requirements across different VFS Global country pages.

## Contributing

We welcome contributions from the community to improve this project! Here's how you can get involved:

- **Report issues:** If you encounter any bugs or problems with the script, please create an issue on the project's repository.
- **Suggest improvements:** Do you have ideas for making the script more user-friendly or feature-rich? Feel free to create an issue or pull request on the repository.
- **Submit pull requests:** If you've made code changes that you think would benefit the project, create a pull request on the repository. Please follow any contribution guidelines outlined in a CONTRIBUTING.md file.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ranjan-mohanty/vfs-appointment-bot&type=Date)](https://star-history.com/#ranjan-mohanty/vfs-appointment-bot&Date)

## Disclaimer

This script is provided as-is and is not affiliated with VFS Global. It's your responsibility to ensure you're complying with VFS Global's terms and conditions when using this script. Be aware that website structures and appointment availability mechanisms might change over time.
