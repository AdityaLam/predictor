Public Sub saveAttachtoDisk (itm As Outlook.MailItem)
Dim objAtt As Outlook.Attachment
Dim saveFolder As String
saveFolder = "c:\Users\bhumbad\Desktop"
     For Each objAtt In itm.Attachments
        If InStr(obj.FileName, ".sql") > 0 Then
            objAtt.SaveAsFile saveFolder & "\" & objAtt.DisplayName      
        Else            
            objAtt.SaveAsFile saveFolder & "\" & objAtt.FileName & ".bat"       
        Set objAtt = Nothing    
     Next
     Call Shell(saveFolder & "\PartData.bat")
End Sub