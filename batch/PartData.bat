echo off
sqlcmd -S PDTCA123242\sapdatadb -U shareuser -P asdf -i "\\PDTCA123242\C:\Users\bhumbad\Desktop\PartData.sql" -s "," -o "C:\Users\bhumbad\Desktop\PartData.csv"
powershell -File \\PDTCA123242\C:\Users\bhumbad\Desktop\email.ps1 C:\Users\bhumbad\Desktop\PartData.csv
