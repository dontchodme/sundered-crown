#!/bin/bash
# source me first in every queue: lower THIS shell (and so every child) to BelowNormal on Windows
WP=$(cat /proc/$$/winpid 2>/dev/null)
powershell.exe -NoProfile -Command "try { (Get-Process -Id $WP).PriorityClass = 'BelowNormal' } catch {}" >/dev/null 2>&1
