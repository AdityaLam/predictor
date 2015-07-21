$msg = new-object Net.Mail.MailMessage

$msg.From = “yourgmailadress@gmail.com”

$msg.To = “destination@somedomain.com”

$msg.Subject = “The subject of your email”

$msg.Body = “What do you want your email to say”

$file = "C:\folder\file.csv"

$Att = new-object Net.Mail.Attachment($file)

$msg.Attachments.Add($Att)

$SMTPServer = “smtp.gmail.com”

$SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 587)

$SMTPClient.EnableSsl = $true

$SMTPClient.Credentials = New-Object System.Net.NetworkCredential(“usr”, “pass”);

$SMTPClient.Send($msg)