# Stop qM2.sh after its mP3 run: its bash processes and any python they started (its own drawn mP2).
$all = Get-CimInstance Win32_Process
$b = $all | Where-Object { $_.Name -eq 'bash.exe' -and $_.CommandLine -match 'qM2' }
$bid = @($b | ForEach-Object { $_.ProcessId })
$py = $all | Where-Object { $_.Name -eq 'python.exe' -and ($bid -contains $_.ParentProcessId) }
foreach ($p in @($py) + @($b)) { if ($p) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue; "$($p.ProcessId) $($p.Name)" } }
