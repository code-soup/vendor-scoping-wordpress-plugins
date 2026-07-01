# Troubleshooting

## Scoper Produces No Output

**Symptom:** `composer scope` runs but creates no files

**Cause:** Finder config references non-existent directories

**Solution:** Check `scoper.inc.php` finders match actual vendor packages

## Namespace Not Found Errors

**Symptom:** `Class 'CodeSoup\Options\Manager' not found`

**Cause:** Using original namespace instead of prefixed

**Solution:** Check autoloader order in index.php - prefixed must load first:

```php
require_once __DIR__ . '/vendor-prefixed/autoload.php';
require_once __DIR__ . '/vendor/autoload.php';
```

## WordPress-Style Classes Not Loading

**Symptom:** `Class 'CodeSoup\Dependencies\...' not found` for class-*.php files

**Cause:** Classmap not updated

**Solution:** Run `composer scope` to rebuild classmap with injected classes

## Package-Specific Autoloaders Broken

**Symptom:** Package loads but internal autoloader fails

**Cause:** Package has its own autoloader with hardcoded namespace

**Solution:** Add patcher in `scoper.inc.php`:

```php
'patchers' => [
    static function (string $filePath, string $prefix, string $content): string {
        if (strpos($filePath, 'vendor/package/autoloader.php') !== false) {
            $content = str_replace(
                "namespace Original\\Package;",
                "namespace YourPlugin\\Dependencies\\Original\\Package;",
                $content
            );
            $content = str_replace(
                "'Original\\Package\\\\'",
                "'YourPlugin\\\\Dependencies\\\\Original\\\\Package\\\\'",
                $content
            );
        }
        return $content;
    },
],
```

## Scoped Packages Still in vendor/

**Symptom:** `composer check-scoping` warns packages still in vendor/

**Cause:** Python script didn't complete cleanup step

**Solution:** Run `composer scope` again, or manually:

```bash
rm -rf vendor/codesoup vendor/psr vendor/symfony
composer dump-autoload
```
