<?php

declare(strict_types=1);

use Isolated\Symfony\Component\Finder\Finder;

return [
	'prefix' => 'YourPlugin\\Dependencies',
	'output-dir' => 'vendor-prefixed',

	'finders' => [
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/codesoup/metabox-schema'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/codesoup/options'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/psr'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/graham-campbell'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/phpoption'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/symfony'),
		Finder::create()
			->files()
			->ignoreVCS(true)
			->notName('/.*\\.md|.*\\.dist|Makefile|composer\\.json|composer\\.lock/')
			->exclude(['doc', 'test', 'tests', 'Tests', 'vendor-bin'])
			->in('vendor/vlucas'),
	],

	'expose-global-constants' => false,
	'expose-global-classes' => false,
	'expose-global-functions' => false,

	'exclude-constants' => [
		'/^ABSPATH$/',
		'/^WPINC$/',
		'/^WP_.*/',
	],

	'exclude-classes' => [
		'/^WP_.*/',
		'/^wpdb$/',
		'/^Walker.*/',
	],

	'exclude-functions' => [
		'/^wp_.*/',
		'/^add_.*/',
		'/^remove_.*/',
		'/^get_.*/',
		'/^is_.*/',
		'/^has_.*/',
		'/^do_.*/',
		'/^apply_.*/',
		'/^register_.*/',
		'/^current_.*/',
		'/^__$/',
		'/^_e$/',
		'/^_n$/',
		'/^_x$/',
		'/^esc_.*/',
		'/^sanitize_.*/',
	],

	'patchers' => [
		static function (string $filePath, string $prefix, string $content): string {
			// Fix CodeSoup Options autoloader
			if (strpos($filePath, 'codesoup/options/includes/class-autoloader.php') !== false) {
				$content = str_replace(
					"namespace CodeSoup\\Options;",
					"namespace YourPlugin\\Dependencies\\CodeSoup\\Options;",
					$content
				);
				$content = str_replace(
					"private const NAMESPACE_PREFIX = 'CodeSoup\\Options\\\\';",
					"private const NAMESPACE_PREFIX = 'YourPlugin\\\\Dependencies\\\\CodeSoup\\\\Options\\\\';",
					$content
				);
			}

			// Fix CodeSoup MetaboxSchema autoloader
			if (strpos($filePath, 'codesoup/metabox-schema') !== false
				&& strpos($filePath, 'autoloader') !== false) {
				$content = str_replace(
					"private const NAMESPACE_PREFIX = 'CodeSoup\\MetaboxSchema\\\\';",
					"private const NAMESPACE_PREFIX = 'YourPlugin\\\\Dependencies\\\\CodeSoup\\\\MetaboxSchema\\\\';",
					$content
				);
			}

			return $content;
		},
	],
];
