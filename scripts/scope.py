#!/usr/bin/env python3
"""Scope dependencies to prevent namespace conflicts."""

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict

ROOT_DIR = Path(__file__).parent.parent.parent
VENDOR_DIR = ROOT_DIR / "vendor"
PREFIXED_DIR = ROOT_DIR / "vendor-prefixed"
SCOPER_CONFIG = ROOT_DIR / "build" / "scoper.inc.php"
SCOPER_BIN = ROOT_DIR / "vendor-bin" / "php-scoper" / "vendor" / "bin" / "php-scoper"

REQUIRED_PHP_VERSION = "8.1"

# Adapt these for your plugin
SCOPED_PACKAGES = [
    "codesoup",
    "psr",
    "graham-campbell",
    "phpoption",
    "symfony",
    "vlucas",
]

CLASSMAP_SOURCE = PREFIXED_DIR / "codesoup" / "metabox-schema" / "includes"
CLASSMAP_FILE = VENDOR_DIR / "composer" / "autoload_classmap.php"
CLASSMAP_STATIC = VENDOR_DIR / "composer" / "autoload_static.php"


def run(cmd: str, cwd: Path = None) -> subprocess.CompletedProcess:
    """Run shell command and exit on failure."""
    print(f"→ {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd or ROOT_DIR,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def check_php_version() -> None:
    """Verify PHP version."""
    print("\nChecking PHP version...")
    result = subprocess.run("php -v", shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        print("Error: Could not detect PHP version", file=sys.stderr)
        sys.exit(1)

    version_match = re.search(r'PHP (\d+\.\d+)', result.stdout)
    if not version_match:
        print("Error: Could not parse PHP version", file=sys.stderr)
        sys.exit(1)

    php_version = version_match.group(1)
    print(f"✓ Detected PHP {php_version}")

    if php_version < REQUIRED_PHP_VERSION:
        print(f"\n❌ Error: PHP {REQUIRED_PHP_VERSION}+ is required", file=sys.stderr)
        sys.exit(1)


def setup_scoper() -> None:
    """Setup php-scoper in vendor-bin if missing."""
    if SCOPER_BIN.exists():
        return

    print("\nSetting up php-scoper...")
    scoper_config = ROOT_DIR / "vendor-bin" / "php-scoper" / "composer.json"
    scoper_config.parent.mkdir(parents=True, exist_ok=True)
    scoper_config.write_text('{\n    "require": {\n        "humbug/php-scoper": "^0.18"\n    }\n}\n')
    print("✓ Created vendor-bin/php-scoper/composer.json")

    run("composer bin php-scoper install")
    print("✓ Installed php-scoper")


def install_dependencies() -> None:
    """Install dependencies."""
    print("\nInstalling dependencies...")
    run("composer install --no-scripts")


def clean_prefixed() -> None:
    """Remove vendor-prefixed directory."""
    print("\nCleaning vendor-prefixed/...")
    if PREFIXED_DIR.exists():
        shutil.rmtree(PREFIXED_DIR)
        print(f"✓ Removed {PREFIXED_DIR}")


def run_scoper() -> None:
    """Run PHP Scoper."""
    print("\nRunning PHP Scoper...")
    run(f"{SCOPER_BIN} add-prefix --force --config={SCOPER_CONFIG}")


def cleanup_vendor() -> None:
    """Remove scoped packages from vendor."""
    print("\nRemoving scoped packages from vendor/...")
    for package in SCOPED_PACKAGES:
        pkg_dir = VENDOR_DIR / package
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)
            print(f"✓ Removed vendor/{package}")


def create_prefixed_autoloader() -> None:
    """Create autoloader for vendor-prefixed."""
    print("\nCreating vendor-prefixed autoloader...")

    # Adapt PSR-4 mappings for your packages
    psr4_map = {
        "YourPlugin\\\\Dependencies\\\\Psr\\\\Container\\\\": "psr/container/src",
        "YourPlugin\\\\Dependencies\\\\CodeSoup\\\\Options\\\\": "codesoup/options/includes",
        # Add other mappings...
    }

    map_code = ""
    for ns, path in psr4_map.items():
        map_code += f"    '{ns}' => __DIR__ . '/{path}',\n"

    autoload_file = PREFIXED_DIR / "autoload.php"
    autoload_file.write_text(f"""<?php
// Autoloader for scoped dependencies
spl_autoload_register(function ($class) {{
    static $map = [
{map_code}    ];

    foreach ($map as $prefix => $base_dir) {{
        $len = strlen($prefix);
        if (strncmp($prefix, $class, $len) !== 0) {{
            continue;
        }}

        $relative_class = substr($class, $len);


        // PSR-4 path
        $file = $base_dir . '/' . str_replace('\\\\', '/', $relative_class) . '.php';
        if (file_exists($file)) {{
            require_once $file;
            return;
        }}

        // WordPress-style fallback
        $parts = explode('\\\\', $relative_class);
        $class_name = array_pop($parts);
        $wp_filename = strtolower(str_replace('_', '-', $class_name)) . '.php';

        $type_prefixes = ['class-', 'trait-', 'interface-'];
        $search_dirs = ['', 'core/', 'utilities/', 'fields/', 'admin/'];

        foreach ($search_dirs as $search_dir) {{
            foreach ($type_prefixes as $type_prefix) {{
                $wp_file = $base_dir . '/' . $search_dir . $type_prefix . $wp_filename;
                if (file_exists($wp_file)) {{
                    require_once $wp_file;
                    return;
                }}
            }}
        }}
    }}
}});
""")
    print(f"✓ Created autoloader with {len(psr4_map)} mappings")


def rebuild_autoloader() -> None:
    """Rebuild Composer autoloader."""
    print("\nRebuilding autoloader...")
    run("composer dump-autoload")


def extract_classes() -> Dict[str, str]:
    """Extract class definitions from WordPress-style class files."""
    classes = {}
    if not CLASSMAP_SOURCE.exists():
        return classes

    for php_file in CLASSMAP_SOURCE.rglob("class-*.php"):
        content = php_file.read_text()
        ns_match = re.search(r'namespace\s+([\w\\]+)', content)
        class_match = re.search(r'class\s+(\w+)', content)

        if ns_match and class_match:
            fqcn = f"{ns_match.group(1)}\\{class_match.group(1)}"
            abs_path = str(php_file)
            classes[fqcn] = abs_path
    return classes


def update_classmap(classes: Dict[str, str]) -> None:
    """Update autoload_classmap.php with new classes."""
    if not classes or not CLASSMAP_FILE.exists():
        return

    content = CLASSMAP_FILE.read_text()
    for fqcn, abs_path in classes.items():
        rel_path = Path(abs_path).relative_to(ROOT_DIR)
        entry = f"    '{fqcn}' => $baseDir . '/{rel_path}',"
        if entry not in content:
            content = content.replace("return array(", f"return array(\n{entry}")
    CLASSMAP_FILE.write_text(content)


def inject_classmap() -> None:
    """Inject WordPress-style classes to classmap."""
    print("\nBuilding classmap...")
    classes = extract_classes()
    if classes:
        update_classmap(classes)
        print(f"✓ Classmap updated with {len(classes)} classes")


def main() -> None:
    """Execute all scoping steps."""
    skip_install = len(sys.argv) > 1 and sys.argv[1] == "--skip-install"

    print("=== Scoping Dependencies ===")

    check_php_version()
    setup_scoper()

    if not skip_install:
        install_dependencies()
    else:
        print("\nEnsuring packages exist...")
        run("composer install --no-scripts")

    clean_prefixed()
    run_scoper()
    create_prefixed_autoloader()
    cleanup_vendor()
    rebuild_autoloader()
    inject_classmap()
    print("\n✓ Scoping complete")


if __name__ == "__main__":
    main()
