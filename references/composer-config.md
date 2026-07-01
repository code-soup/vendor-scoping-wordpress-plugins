# Composer Configuration

Add to `composer.json`:

```json
{
  "require-dev": {
    "bamarni/composer-bin-plugin": "^1.9"
  },
  "config": {
    "allow-plugins": {
      "bamarni/composer-bin-plugin": true
    }
  },
  "extra": {
    "bamarni-bin": {
      "bin-links": false,
      "target-directory": "vendor-bin",
      "forward-command": false
    }
  },
  "scripts": {
    "scope": ["python3 build/scope.py"],
    "re-scope": ["python3 build/scope.py --skip-install"],
    "check-scoping": ["php build/check-scoping.php"],
    "post-install-cmd": ["printf '⚠️  Dependencies updated. Run: composer scope'"],
    "post-update-cmd": ["printf '⚠️  Dependencies updated. Run: composer scope'"]
  }
}
```

## Usage

```bash
# Initial setup
composer install

# Scope dependencies
composer scope

# Re-scope without reinstalling
composer re-scope

# Check if scoping is current
composer check-scoping
```
