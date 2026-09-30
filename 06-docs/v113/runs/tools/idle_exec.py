"""Run any command at Idle priority (children inherit it): idle_exec.py <cmd> [args...]. Rick is on the PC.
Children print UTF-8 (PYTHONIOENCODING), as the earlier lanes' runs did."""
import ctypes, os, subprocess, sys
k = ctypes.windll.kernel32
k.SetPriorityClass(k.GetCurrentProcess(), 0x40)   # IDLE_PRIORITY_CLASS
env = dict(os.environ, PYTHONIOENCODING="utf-8")
sys.exit(subprocess.run(sys.argv[1:], env=env).returncode)
