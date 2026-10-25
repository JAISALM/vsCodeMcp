"""Empty D: recycle bin (SHEmptyRecycleBinW) + report freed space."""
import ctypes
import subprocess

# SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
flags = 0x01 | 0x02 | 0x04
hr = ctypes.windll.shell32.SHEmptyRecycleBinW(None, "D:\\", flags)
print("SHEmptyRecycleBinW HRESULT:", hr)  # 0 = S_OK

# report
out = subprocess.check_output(["cmd", "/c", "wmic", "logicaldisk", "where", "DeviceID='D:'", "get", "FreeSpace,Size"], text=True)
print(out)
