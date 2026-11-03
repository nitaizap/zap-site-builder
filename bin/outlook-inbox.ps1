# Save new sites-team mail from the desktop Outlook on this PC into work/inbox/<id>/ (no cloud, no Graph).
# Used by the zap-intake skill when the Microsoft 365 connector is blocked by company sign-in policy.
#   powershell -ExecutionPolicy Bypass -File bin/outlook-inbox.ps1 [-Days 14]
# Per message: attachments, body.txt (UTF-8), meta.json {entry_id, from, subject, received, conversation_id, conversation_topic}.
# Skips messages already listed in work/intake-state.json. Reads only; never sends or moves mail.
param([int]$Days = 14,
      [string[]]$Senders = @("NetaS@d.co.il", "SharonY@d.co.il", "NoamR@d.co.il"))

$ErrorActionPreference = "Stop"
$root  = Split-Path -Parent $PSScriptRoot
$inbox = Join-Path $root "work\inbox"
$state = Join-Path $root "work\intake-state.json"
New-Item -ItemType Directory -Force -Path $inbox | Out-Null
$done = @{}
if (Test-Path $state) { (Get-Content $state -Raw -Encoding UTF8 | ConvertFrom-Json).handled | ForEach-Object { $done[$_] = 1 } }

$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace("MAPI")
$folder = $ns.GetDefaultFolder(6)   # Inbox
$since = (Get-Date).AddDays(-$Days).ToString("g")
$items = $folder.Items.Restrict("[ReceivedTime] >= '$since'")
$want = $Senders | ForEach-Object { $_.ToLower() }
$out = @()

foreach ($m in $items) {
    if ($m.Class -ne 43) { continue }            # mail items only
    $addr = $m.SenderEmailAddress
    if ($m.SenderEmailType -eq "EX") { try { $addr = $m.Sender.GetExchangeUser().PrimarySmtpAddress } catch {} }
    if (-not $addr -or ($want -notcontains $addr.ToLower())) { continue }
    $id = $m.EntryID.Substring($m.EntryID.Length - 16)
    if ($done.ContainsKey($id)) { continue }
    $dir = Join-Path $inbox $id
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    foreach ($a in $m.Attachments) { if ($a.Type -eq 1) { $a.SaveAsFile((Join-Path $dir $a.FileName)) } }
    [IO.File]::WriteAllText((Join-Path $dir "body.txt"), $m.Body, [Text.UTF8Encoding]::new($false))
    $meta = [ordered]@{ entry_id = $id; from = $addr; subject = $m.Subject; received = $m.ReceivedTime.ToString("s");
                        conversation_id = $m.ConversationID; conversation_topic = $m.ConversationTopic }
    [IO.File]::WriteAllText((Join-Path $dir "meta.json"), ($meta | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
    $out += $meta
}
$out | ConvertTo-Json -Depth 3
