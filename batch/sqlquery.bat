echo off
sqlcmd -S PDTCA123242\sapdatadb -U shareuser -P asdf -i "\\PDTCA123242\C:\Users\bhumbad\Desktop\PartNumber.sql" -s "," -o "C:\Users\bhumbad\Desktop\yesterday.csv"
curl -XPOST -F data=@C:\Users\bhumbad\Desktop\yesterday.csv http://domain.com/yesterday
powershell -File \\PDTCA123242\C:\Users\bhumbad\Desktop\email.ps1 C:\Users\bhumbad\Desktop\yesterday.csv
