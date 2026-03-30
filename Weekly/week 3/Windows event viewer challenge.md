# Intro
A `Challenge.zip` file is provided with two images and a logs file (`evtx`). It also contains two images containing questions to answer.

1. What event ID is to detect a **PowerShell downgrade** attack?
	

2. What is the Date and Time this attack took place? (`MM/DD/YYY H:MM:SS [AM/PM]`)
	

3. A **Log clear** event was recorded. What is the 'Event Record ID'?
	104

4. What is the name of the computer?
	PC01.example.corp

5. What is the name of the first variable within the PowerShell command?
	
	base64data

6. What is the Date and Time this attack took place?
	

7. What is the Execution process ID?
	

8. What is the Group Security ID of the group she enumerated?
	

9. What is the event ID?
	




---
```
Creating Scriptblock text (1 of 1):
$base64data = "H4sIAIGp1V8CA51WbW/bNhD+7l9xcLVaQixCdltsDZCirpJuAbLWqLzlg2EgtHSOtcikR1J+QeL/XlKiLDlO0Kb6You8e+65545HvYIhX6OY5Qx8uBapUshguoVP+meUC4YCXsM5XSH8RUWybbW0ZaxSzuBPVP41TuMsRaagdd8C/TjrGM7gC679r9P/MFbgj7ZL/EIXqBcV0fZhYV8Zk38knuOM5pkKBSZ6J6WZ1BCOEjnurYaCb7bkkYVeb6xUtq1dTXFZpda6h2J/SAVduOX/caREym4nTsgXC8qS7uFqJLOYs0eL53zNMk6TYtWzmILHKCVYARY8yTM0BD+6HpQm6QzcKgz4+D+0pylL2l6xWfoVvlkqtfxa8jMdcqv/L4hRLeLxHSpJRvHyylpMer0/fn977EmkokKZwDZ0sWtrdNawG8QxLpVGLOvhllx2z/EVuEIh8ZjyHrpR86eoh0MbqN0LSO/Ne9IL3pD+23ftbpGJDd8qNZRKIF0YviU80b0WFWuaZ82wLFFJ0LRL21akQU/KLKrAnmGIca7bfkuiytS18bvOTPcVdt17Z6TRd+BTCeMDn2+44ApDFCqdpTFV+C/N0oSa5gtplk1pfDfxvCfokEGu5qZzjdNAPqON16hhrUmdU1O08XSrcDyZOObXtF9ASD/Qz8Nv98HO6oosqbbdscKNIshinpjePj0dROHlpWe0/mRs3Pa1blK+luWEiOaYZSByxrQ1aCVyqRu1DSfgIFudmjdmjvmJXtNF2W/EfLHMVb15w0K+3Ir0dq7ADT3oB7138HcaCy75TEHIxZKLQkECAxPRWEoQqAOsMCE37IbZNrSaEDO20K2z6wbd+oVcIbtV82bfVKe42TlHjfMyqcYnE7jSkEYbOwHInufLuVZen7m4oPFccy5BIWX7CVNb1bTN4x4MZo9U2ZYzrELyHi7Zit+hf7FZam2l1nuPsjs8jC9SojOMoKPrXLC44nFRSY8MqZrr1c6Hzi+Xbj1PM3RdJy3OQOn+DWnilh3fhaALzoGfBz5DCI5qe2HoYzLSqTx3WdkBYUxIkeKFTblG0cecGioNNDunCpmrdMBJvUdtpaeC0fKoAOBXM7cE73943YMH+Jorv0QFK8UBVB8KQSpgLfIPSgCdGmRjiDgoBBfjYHIQrMG62CdxhlS43lMMzpov+uBvWscn6afap4b54dFptsrRwal8Pme5nO/vYTsG7aUSZlyizae+GCPFl9VtqL8lWvtviH1x7F0Ivr1/zAD5DjRBmd5HCQAA"
$data = [System.Convert]::FromBase64String($base64data)
$ms = New-Object System.IO.MemoryStream
$ms.Write($data, 0, $data.Length)
$ms.Seek(0,0) | Out-Null

$sr = New-Object System.IO.StreamReader(New-Object System.IO.Compression.DeflateStream($ms, [System.IO.Compression.CompressionMode]::Decompress))

while ($line = $sr.ReadLine()) {  
    $line
}

ScriptBlock ID: 9031d7ef-964a-4acf-9030-b7b136a45edf
Path: C:\Users\Administrator\Desktop\test.ps1
```