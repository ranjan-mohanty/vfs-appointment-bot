# VFS Appointment Bot

[![GitHub license](https://img.shields.io/github/license/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/blob/main/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/network)
[![GitHub stars](https://img.shields.io/github/stars/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/ranjan-mohanty/vfs-appointment-bot)](https://github.com/ranjan-mohanty/vfs-appointment-bot/issues)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Franjan-mohanty%2Fvfs-appointment-bot)](https://twitter.com/intent/tweet?text=Check%20this%20out%20&url=https%3A%2F%2Fgithub.com%2Franjan-mohanty%2Fvfs-appointment-bot)

This Python script(**vfs-appointment-bot**) automates checking for appointments at VFS Global portal in a specified country.

## Installation

The `vfs-appointment-bot` script can be installed using two methods:

**1. Using pip:**

It is the preferred method for installing `vfs-appointment-bot`. Here's how to do it:

1.  **Install using pip:**

    ```bash
    pip install vfs-appointment-bot
    ```

    This will download and install the `vfs-appointment-bot` package and its dependencies into your Python environment.

**2. Manual Installation:**

If you prefer a more traditional approach, you can clone the source code from the project repository and install it manually:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ranjan-mohanty/vfs-appointment-bot
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd vfs-appointment-bot
    ```

3.  **Create a virtual environment (Recommended):**

    ```bash
    python3 -m venv venv
    ```

    This creates a virtual environment named `venv` to isolate project dependencies from your system-wide Python installation (**recommended**).

4.  **Activate the virtual environment:**

    **Linux/macOS:**

    ```bash
    source venv/bin/activate
    ```

    **Windows:**

    ```bash
    venv\Scripts\activate
    ```

5.  **Install dependencies:**

    ```bash
    pip install poetry
    poetry install
    ```

6.  **Install playwright dependencies:**

    ```bash
    playwright install
    ```

## Usage

1. **Command-Line Argument:**

   The script requires the country code ([as per ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)) to be provided as a command-line argument using the `-c` or `--country-code` option.

2. **Running the Script:**

   There are two ways to provide required appointment details:

   - **Responding to User Prompts (recommended):**

     ```bash
     vfs-appointment-bot -c DE
     ```

     The script will prompt you to enter the required apponitment parameters for the specified country.

   - **Using `-ap` or `--appointment-params`:**

     Specify appointment details in a comma-separated (**not space-separated**) key-value format:

     ```bash
     vfs-appointment-bot -c DE -ap visa_center=X,visa_category=Y,visa_sub_category=Z
     ```

   The script will then connect to the VFS Global website for the specified country, search for available appointments using the provided or entered parameters, and potentially send notifications (depending on your configuration).

## Supported Countries and Appointment Parameters

The following table lists currently supported countries and their corresponding appointment parameters:

| Country      | Appointment Parameters                        |
| ------------ | --------------------------------------------- |
| Germany (DE) | visa_category, visa_sub_category, visa_center |

**Notes:**

- Appointment parameters might vary depending on the specific country and visa type. Always consult VFS Global's website for the latest information.

## Extending Country Support

This script is currently designed to work with the VFS Global website for Germany. It might be possible to extend support for other countries by modifying the script to handle potential variations in website structure and parameter requirements across different VFS Global country pages.

## Contributing

We welcome contributions from the community to improve this project! Here's how you can get involved:

- **Report issues:** If you encounter any bugs or problems with the script, please create an issue on the project's repository.
- **Suggest improvements:** Do you have ideas for making the script more user-friendly or feature-rich? Feel free to create an issue or pull request on the repository.
- **Submit pull requests:** If you've made code changes that you think would benefit the project, create a pull request on the repository. Please follow any contribution guidelines outlined in a CONTRIBUTING.md file.

## Disclaimer

This script is provided as-is and is not affiliated with VFS Global. It's your responsibility to ensure you're complying with VFS Global's terms and conditions when using this script. Be aware that website structures and appointment availability mechanisms might change over time.
