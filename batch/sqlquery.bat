echo off
sqlcmd -S sapdatadb -U shareuser -P asdf -i "C:\Users\bhumbad\Desktop\PartNumber.sql" -s "," -o "C:\Users\bhumbad\Desktop\"yesterday.csv"