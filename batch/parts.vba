Public Sub saveAttachtoDisk (itm As Outlook.MailItem)
Dim objAtt As Outlook.Attachment
Dim saveFolder As String
saveFolder = "c:\Users\bhumbad\Desktop"
     For Each objAtt In itm.Attachments        
          objAtt.SaveAsFile saveFolder & "\" & objAtt.DisplayName        
          Set objAtt = Nothing    
     Next
     Call Shell(saveFolder & '\PartData.bat')
End Sub