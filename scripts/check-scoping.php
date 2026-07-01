#!/usr/bin/env php
<?php
/**
 * Check if scoping is needed by comparing timestamps
 */

$root_dir = dirname(__DIR__, 3);

$scoped_packages = ['codesoup', 'psr', 'symfony', 'vlucas'];
$composer_lock = $root_dir . '/composer.lock';
$prefixed_dir = $root_dir . '/vendor-prefixed';

// ANSI colors
$red = "\033[31m";
$yellow = "\033[33m";
$green = "\033[32m";
$reset = "\033[0m";

// Check if scoped packages still exist in vendor/
$found_unscoped = [];
foreach ($scoped_packages as $package) {
	if (file_exists($root_dir . '/vendor/' . $package)) {
		$found_unscoped[] = $package;
	}
}

if (!empty($found_unscoped)) {
	echo "{$yellow}⚠️  Warning:{$reset} Scoped packages still in vendor/\n";
	foreach ($found_unscoped as $package) {
		echo "   - vendor/{$package}/\n";
	}
	echo "\n   Run: {$green}composer scope{$reset}\n\n";
	exit(1);
}

// Check if vendor-prefixed/ exists
if (!file_exists($prefixed_dir)) {
	echo "{$red}❌ Error:{$reset} vendor-prefixed/ does not exist\n";
	echo "   Run: {$green}composer scope{$reset}\n\n";
	exit(1);
}

// Check if all scoped packages exist in vendor-prefixed/
$missing_scoped = [];
foreach ($scoped_packages as $package) {
	if (!file_exists($prefixed_dir . '/' . $package)) {
		$missing_scoped[] = $package;
	}
}

if (!empty($missing_scoped)) {
	echo "{$red}❌ Error:{$reset} Missing scoped packages\n";
	foreach ($missing_scoped as $package) {
		echo "   - {$package}\n";
	}
	echo "\n   Run: {$green}composer scope{$reset}\n\n";
	exit(1);
}

// Check timestamps
$lock_time = filemtime($composer_lock);
$prefixed_time = filemtime($prefixed_dir);

if ($lock_time > $prefixed_time) {
	echo "{$yellow}⚠️  Warning:{$reset} composer.lock newer than scoped files\n";
	echo "   Run: {$green}composer scope{$reset}\n\n";
	exit(1);
}

echo "{$green}✓{$reset} Scoping is up to date\n";
echo "   Scoped packages: " . count($scoped_packages) . "\n\n";
exit(0);
