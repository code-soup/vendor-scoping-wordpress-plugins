# Vendor Scoping WordPress Plugins Agent Skill

An [Agent Skill](https://docs.augmentcode.com/skills) for preventing namespace conflicts in WordPress plugins using PHP-Scoper.

## What This Skill Does

Teaches AI agents how to implement vendor scoping (dependency prefixing) in WordPress plugins to prevent namespace conflicts. When your plugin shares dependencies with themes or other plugins (like `codesoup/options`, `psr/*`, `symfony/*`), the first loaded version wins, causing fatal errors or unexpected behavior.

This skill provides:

- Complete workflow for scoping Composer dependencies
- Python orchestration script for automated scoping
- PHP-Scoper configuration with WordPress-specific exclusions
- Custom autoloader supporting both PSR-4 and WordPress naming conventions
- Verification and troubleshooting guides

## Installation

### For Augment CLI Users

```bash
# Install via skillshare (recommended)
skillshare install code-soup/vendor-scoping-wordpress-plugins

# Or clone directly to skills directory
git clone https://github.com/code-soup/vendor-scoping-wordpress-plugins.git ~/.augment/skills/vendor-scoping
```

### For Other AI Tools

Copy the skill directory to your AI tool's skills location:

```bash
# Claude Desktop
git clone https://github.com/code-soup/vendor-scoping-wordpress-plugins.git ~/Library/Application\ Support/Claude/skills/vendor-scoping

# Cursor
git clone https://github.com/code-soup/vendor-scoping-wordpress-plugins.git ~/.cursor/skills/vendor-scoping

# Windsurf
git clone https://github.com/code-soup/vendor-scoping-wordpress-plugins.git ~/.windsurf/skills/vendor-scoping
```

See [agentskills.io](https://agentskills.io) for other tools.

## Usage

Once installed, the skill is automatically available to your AI agent. When you mention:

- "I'm getting namespace conflicts with codesoup/options"
- "Need to scope dependencies for distribution"
- "Plugin conflicts with theme's psr/\* packages"

The agent will use this skill to guide the implementation.

### Manual Invocation

You can explicitly reference the skill:

```
Using the vendor-scoping skill, help me isolate my plugin's dependencies
```

## What Gets Created

When the agent applies this skill to your WordPress plugin, it will:

1. **Add Composer configuration** for php-scoper and bin-plugin
2. **Create build scripts:**
    - `build/scope.py` - Python orchestration script
    - `build/scoper.inc.php` - PHP-Scoper configuration
    - `build/check-scoping.php` - Verification script
3. **Add composer commands:**
    - `composer scope` - Scope all dependencies
    - `composer re-scope` - Re-scope without reinstalling
    - `composer check-scoping` - Verify scoping status
4. **Generate `vendor-prefixed/`** directory with scoped dependencies
5. **Update plugin autoloader** to load prefixed dependencies first

## Example Workflow

```bash
# 1. Setup (one time)
composer require --dev bamarni/composer-bin-plugin

# 2. Agent creates build scripts and configuration

# 3. Scope dependencies
composer scope

# 4. Deploy with vendor-prefixed/ included
```

## Files Included

```
vendor-scoping/
├── SKILL.md                      # Main skill documentation
├── scripts/                      # Reference implementations
│   ├── scope.py                  # Python orchestration
│   ├── scoper.inc.php           # PHP-Scoper config
│   └── check-scoping.php        # Verification
└── references/                   # Detailed guides
    ├── composer-config.md       # Setup instructions
    └── troubleshooting.md       # Common issues
```

## Requirements

- PHP 8.1+
- Python 3.6+
- Composer 2.0+
- WordPress plugin using Composer

## How It Works

1. **Isolation:** PHP-Scoper installed in `vendor-bin/` (isolated from production)
2. **Prefixing:** All dependency namespaces rewritten to `YourPlugin\Dependencies\*`
3. **Autoloading:** Custom autoloader handles both PSR-4 and WordPress conventions
4. **Cleanup:** Original packages removed from `vendor/` after scoping
5. **Verification:** Automated checks ensure scoping is current

## Use Cases

- **Conflict Prevention:** Multiple plugins use same dependency
- **Version Isolation:** Plugin needs different version than theme
- **Production Distribution:** Prevent conflicts in unknown environments
- **Premium Plugins:** Ensure dependencies don't conflict with customer's setup

## Compatibility

Works with:

- WordPress plugins (PHP 8.1+)
- Composer-managed dependencies
- PSR-4 and WordPress-style class naming
- Custom package autoloaders (via patchers)

## Contributing

Issues and PRs welcome at [github.com/code-soup/vendor-scoping-wordpress-plugins](https://github.com/code-soup/vendor-scoping-wordpress-plugins)

## License

MIT

## Credits

Created for WordPress plugin development with [Augment](https://augmentcode.com).

Based on:

- [PHP-Scoper](https://github.com/humbug/php-scoper) by Humbug
- [Composer Bin Plugin](https://github.com/bamarni/composer-bin-plugin) by Bamarni
- [Agent Skills Specification](https://agentskills.io)

## Learn More

- [Agent Skills Documentation](https://docs.augmentcode.com/skills)
- [PHP-Scoper Documentation](https://github.com/humbug/php-scoper/blob/main/docs/further-reading.md)
- [WordPress Plugin Best Practices](https://developer.wordpress.org/plugins/plugin-basics/best-practices/)
