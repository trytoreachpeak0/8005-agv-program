$ErrorActionPreference = "Stop"
$desktopKey = "HKCU:\Control Panel\Desktop"
$pendingKey = "HKCU:\Control Panel\Desktop\LanguageConfigurationPending"
Remove-ItemProperty `
    -LiteralPath $desktopKey `
    -Name "PreferredUILanguagesPending" `
    -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath $pendingKey) {
    Remove-Item -LiteralPath $pendingKey -Recurse -Force
}
& pwsh -NoProfile -Command {
    [pscustomobject]@{
        Override = (Get-WinUILanguageOverride)
        Culture = (Get-Culture).Name
        UiCulture = [Globalization.CultureInfo]::CurrentUICulture.Name
        Pending = (Get-ItemProperty "HKCU:\Control Panel\Desktop").PreferredUILanguagesPending
    }
}
