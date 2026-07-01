---
name: vendor-scoping
description: Use PHP-Scoper to prevent namespace conflicts in WordPress plugins by prefixing Composer dependencies. Apply when codesoup/options, psr/*, symfony/*, or other packages conflict with theme/plugin versions, or preparing for production distribution.
---

# Vendor Scoping with PHP-Scoper

PHP-Scoper rewrites dependency namespaces to prevent conflicts:
`CodeSoup\Options` → `YourPlugin\Dependencies\CodeSoup\Options`

**Problem:** Plugin shares dependencies with theme/other plugins → wrong version loads first → fatal errors.

**Solution:** Isolate by prefixing all dependency namespaces.

## Quick Start

```bash
# 1. Setup (once)
composer require --dev bamarni/composer-bin-plugin
# Add scripts to composer.json (see Setup section)

# 2. Create build/ files (see Appendix)

# 3. Scope dependencies
composer scope

# 4. Update index.php autoloader
require_once __DIR__ . '/vendor-prefixed/autoload.php';
require_once __DIR__ . '/vendor/autoload.php';
```

## How It Works

Python script → isolate scoper in `vendor-bin/` → run scoper → create custom autoloader → remove originals from `vendor/` → rebuild classmap

## Setup

### 1. Add Composer Dependencies

See [references/composer-config.md](references/composer-config.md)

### 2. Copy Build Scripts

```bash
cp ~/.augment/skills/vendor-scoping/scripts/scope.py build/
cp ~/.augment/skills/vendor-scoping/scripts/scoper.inc.php build/
cp ~/.augment/skills/vendor-scoping/scripts/check-scoping.php build/
chmod +x build/scope.py build/check-scoping.php
```

### 3. Adapt Configuration

Edit `build/scope.py` - change `SCOPED_PACKAGES` and PSR-4 mappings
Edit `build/scoper.inc.php` - change `prefix`, `finders`, `patchers`

### 4. Update Plugin Autoloader

```php
require_once __DIR__ . '/vendor-prefixed/autoload.php';
require_once __DIR__ . '/vendor/autoload.php';
// Then custom autoloader
\YourPlugin\Autoloader::register( __DIR__ );
```

## What to Scope

**Scope:** psr/*, symfony/*, guzzle/*, custom packages, anything used by multiple plugins
**Don't scope:** WordPress core, Action Scheduler (designed global), database/cache singletons

## Distribution

```bash
composer install --no-dev
composer scope
# Deploy: vendor-prefixed/ + reduced vendor/ (excludes scoped packages)
# Exclude: vendor-bin/, build/
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md)

## Additional Files

- `scripts/scope.py` - Full Python orchestration script
- `scripts/scoper.inc.php` - Complete PHP-Scoper configuration
- `scripts/check-scoping.php` - Verification script
- `references/composer-config.md` - Composer setup
- `references/troubleshooting.md` - Common issues

## References

- [PHP-Scoper](https://github.com/humbug/php-scoper)
- [Composer Bin Plugin](https://github.com/bamarni/composer-bin-plugin)
