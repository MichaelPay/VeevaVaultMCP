# VeevaVault Testing Credentials Configuration
# This file should NOT be committed to version control
# Copy this file to test_credentials.py and fill in your actual credentials

TEST_VAULTS = {
    "michael_mastermind": {
        "URL": "https://your-vault.veevavault.com/",
        "username": "your-username@domain.com",
        "password": "your-password"
    },
    # Add more test vaults as needed
    "sandbox": {
        "URL": "https://sandbox-vault.veevavault.com/",
        "username": "sandbox-user@domain.com", 
        "password": "sandbox-password"
    }
}

# Default vault to use for testing
DEFAULT_VAULT = "michael_mastermind"
