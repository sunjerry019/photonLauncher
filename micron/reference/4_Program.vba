' General area for declare the varible for all sub function used.
' note : the unit setting will be set to microns and speed are in microns/s

Dim x1, x2, x0, x3, x4, x5, x6, x7, x8, x9, y1, y2 As Integer 'valuable for cooridinate

Dim enter, space, move, neg
Dim sent As String
Dim oldSpd As Integer
Dim inited As Boolean
Dim Speed As Integer

Dim mInstCnt As Integer
Dim mCumTime As Single

Dim xDisp, yDisp As Integer

Private Sub cmdMv_Click()
    spd = CInt(edSpeed.Text)
    initComm (spd)
    dX = CInt(edMvX.Text)
    dy = CInt(edMvY.Text)
    
    mvXY dX, dy
    
End Sub

Private Sub CommandButton1_Click()
If MSComm1.PortOpen = False Then MSComm1.PortOpen = True
MSComm1.Output = "0 0 move" + enter
MSComm1.PortOpen = False
End Sub


Private Sub CommandButton2_KeyPress(ByVal KeyAscii As MSForms.ReturnInteger)
    Dim dX, dy As Integer
    spd = CInt(edSpeed.Text)
    initComm (spd)
    
        
    Step = CInt(edStepSize.Text)
    lblStatus.Caption = Chr(KeyAscii) + Trim(Str(Step))
    Select Case Chr(KeyAscii)
        Case "W", "w"
            dX = 0
            dy = -1
        Case "A", "a"
            dX = -1
            dy = 0
        Case "D", "d"
            dX = 1
            dy = 0
        Case "X", "x"
            dX = 0
            dy = 1
    End Select
    
    dX = dX * Step
    dy = dy * Step
    
    mvXY dX, dy
    
End Sub

Private Sub drawNo(no As String, size As Integer, gap As Boolean)
    
    s = UCase(no)
    For i = 1 To Len(s)
        Select Case (Mid(s, i, 1))
            Case "0"
                moveXY size, 0
                moveXY 0, size
                moveXY -size, 0
                moveXY 0, -size
                Pause 1
                moveXY size, size
                moveXY 0, -size
            Case "1"
                moveXY 0, size
                moveXY 0, -size
            Case "2"
                moveXY size, 0
                moveXY 0, size / 2
                moveXY -size, 0
                moveXY 0, size - size / 2
                Pause 1
                moveXY size, 0
                moveXY -size, 0
                moveXY 0, -(size - size / 2)
                moveXY size, 0
                Pause 1
                moveXY 0, -size / 2
            Case "3"
                moveXY size, 0
                moveXY 0, size / 2
                moveXY -size, 0
                moveXY size, 0
                Pause 1
                moveXY 0, size - size / 2
                moveXY -size, 0
                moveXY size, 0
                moveXY 0, -size
            Case "4"
                moveXY 0, size / 2
                moveXY size, 0
                moveXY 0, size / 2
                moveXY 0, -size
            Case "5", "S"
                moveXY size, 0
                moveXY -size, 0
                moveXY 0, size / 2
                moveXY size, 0
                Pause 1
                moveXY 0, size - size / 2
                moveXY -size, 0
                moveXY size, 0
                moveXY 0, -(size - size / 2)
                Pause 1
                moveXY -size, 0
                moveXY 0, -size / 2
                moveXY size, 0
                
            Case "6"
                moveXY 0, size
                moveXY size, 0
                moveXY 0, -(size - size / 2)
                moveXY -size, 0
                Pause 1
                moveXY 0, -size / 2
                moveXY size, 0
            Case "7"
                moveXY size, 0
                moveXY 0, size
                moveXY 0, -size
            Case "8", "B"
                moveXY size, 0
                moveXY 0, size
                moveXY -size, 0
                moveXY 0, -size
                Pause 1
                moveXY 0, size / 2
                moveXY size, 0
                moveXY 0, -size / 2
            Case "9"
                moveXY size, 0
                moveXY 0, size / 2
                moveXY -size, 0
                moveXY 0, -size / 2
                Pause 1
                moveXY size, 0
                moveXY 0, size
                moveXY 0, -size
                
            Case "A"
                moveXY 0, size
                moveXY 0, -size
                moveXY size, 0
                moveXY 0, size
                Pause 1
                moveXY 0, -size / 2
                moveXY -size, 0
                moveXY size, 0
                moveXY 0, -size / 2
                'Pause 1
            
            Case "C"
                moveXY size, 0
                moveXY -size, 0
                moveXY 0, size
                moveXY size, 0
                Pause 1
                moveXY -size, 0
                moveXY 0, -size
                moveXY size, 0
                
            Case "D", "O"
                moveXY size, 0
                moveXY 0, size
                moveXY -size, 0
                moveXY 0, -size
                Pause 1
                moveXY size, 0
                
            Case "E"
                moveXY size, 0
                moveXY -size, 0
                moveXY 0, size / 2
                moveXY size, 0
                Pause 1
                moveXY -size, 0
                moveXY 0, size - size / 2
                moveXY size, 0
                moveXY -size, 0
                Pause 1
                moveXY 0, -size
                moveXY size, 0
                
            Case "F"
                moveXY size, 0
                moveXY -size, 0
                moveXY 0, size / 2
                moveXY size, 0
                Pause 1
                moveXY -size, 0
                moveXY 0, size - size / 2
                moveXY 0, -size
                Pause 1
                moveXY size, 0
                
            Case "G"
                moveXY 0, size
                moveXY size, 0
                moveXY 0, -size / 2
                moveXY -size / 2, 0
                Pause 1
                moveXY size / 2, 0
                moveXY 0, size / 2
                moveXY -size, 0
                moveXY 0, -size
                Pause 1
                moveXY size, 0
            
            Case "H"
                moveXY 0, size
                moveXY 0, -size / 2
                moveXY size, 0
                moveXY 0, size / 2
                Pause 1
                moveXY 0, -size
            
            Case "I"
                moveXY size / 2, 0
                moveXY 0, size
                moveXY -size / 2, 0
                moveXY size, 0
                Pause 1
                moveXY -(size - size / 2), 0
                moveXY 0, -size
                moveXY size - size / 2, 0
                'Pause 1
            
            Case "J"
                moveXY size / 2, 0
                moveXY 0, size
                moveXY -size / 2, 0
                moveXY size / 2, 0
                Pause 1
                moveXY 0, -size
                moveXY size - size / 2, 0
            
            Case "K"
                moveXY 0, size
                moveXY 0, -size / 2
                moveXY size, size / 2
                moveXY -size, -size / 2
                Pause 1
                moveXY size, -(size - size / 2)
            
            Case "L"
                If Not gap Then
                    moveXY 0, size
                    moveXY 0, -size
                Else
                    moveXY 0, size
                    moveXY size, 0
                    moveXY -size, 0
                    MsgBox ("off laser")
                    moveXY 0, -size
                    moveXY size, 0
                    
                End If
            
            Case "M"
                moveXY 0, size
                moveXY 0, -size
                moveXY size / 2, 0
                moveXY 0, size
                Pause 1
                moveXY 0, -size
                moveXY size - size / 2, 0
                moveXY 0, size
                moveXY 0, -size
                'Pause 1
            
            Case "N"
                moveXY 0, size
                moveXY 0, -size
                moveXY size, size
                moveXY 0, -size
                Pause 1
            
            Case "P"
                moveXY 0, size
                moveXY 0, -size / 2
                moveXY size, 0
                moveXY 0, -(size - size / 2)
                Pause 1
                moveXY -size, 0
                moveXY size, 0
            
            Case "Q"
                moveXY 0, size
                moveXY size, 0
                moveXY -size / 2, -size / 2
                moveXY size / 2, size / 2
                Pause 1
                moveXY 0, -size
                moveXY -size, 0
                moveXY size, 0
                'Pause 1
            
            Case "R"
                moveXY 0, size
                moveXY 0, -size / 2
                moveXY size / 2, size / 2
                moveXY -size / 2, -size / 2
                Pause 1
                moveXY size, 0
                moveXY 0, -(size - size / 2)
                moveXY -size, 0
                moveXY size, 0
                'pause 1
            
            Case "T"
                moveXY size, 0
                moveXY -size / 2, 0
                moveXY 0, size
                moveXY 0, -size
                Pause 1
                moveXY size - size / 2, 0
            
            Case "U"
                moveXY 0, size
                moveXY size, 0
                moveXY 0, -size
                'Pause 1
            
            Case "V"
                moveXY size / 2, size
                moveXY size / 2, -size
            
            Case "W"
                moveXY 0, size
                moveXY size / 2, 0
                moveXY 0, -size
                moveXY 0, size
                Pause 1
                moveXY size - size / 2, 0
                moveXY 0, -size
            
            Case "X"
                moveXY size, size
                moveXY -size / 2, -size / 2
                moveXY -size / 2, size / 2
                moveXY size, -size
                'Pause 1
            
            Case "Y"
                moveXY size / 2, size / 2
                moveXY 0, size - size / 2
                moveXY 0, -(size - size / 2)
                moveXY size - size / 2, -(size - size / 2)
            
            Case "Z"
                moveXY size, 0
                moveXY -size, size
                moveXY size, 0
                moveXY -size, 0
                Pause 1
                moveXY size, -size
            
            Case " "
                moveXY size, 0
            
                
                
                
                
                
                
                
                
                
                
                

        End Select
        If gap And Mid(s, i, 1) <> "L" And Mid(s, i, 1) <> " " Then MsgBox "shut laser"
        If i <> Len(s) Then
            moveXY size / 2, 0
            Pause 1
        End If
        If gap And Mid(s, i + 1, 1) <> " " Then MsgBox "on laser"

    Next
    
End Sub

Private Sub CommandButton5_Click()
    
    spd = CInt(edSpeed.Text)
    initComm (spd)
                
    Dim i As Integer
    drawNo edNo.Text, 24, cbxStringGap.Value


End Sub
Private Sub CommandButton7_Click()
'Your program goes here; thus :
initComm (150)


upPen
mvXY 4, 78
downPen
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 148, 0
mvXY 0, 2
mvXY -148, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 0, 2
mvXY 146, 0
mvXY 0, 2
mvXY -146, 0
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
mvXY 0, 2
mvXY 396, 0
mvXY 0, 2
mvXY -396, 0
upPen
mvXY 158, -244
downPen
mvXY 12, 0
mvXY 0, 2
mvXY -2, 0
mvXY -10, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -2, 0
mvXY -6, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 0
mvXY 0, 2
mvXY 0, 2
mvXY -2, 0
mvXY 0, 0
upPen
mvXY 24, -18
downPen
mvXY 8, 0
mvXY 0, 2
mvXY -4, 0
mvXY -4, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
upPen
mvXY 24, -30
downPen
mvXY 8, 0
mvXY 0, 2
mvXY -2, 0
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 0
mvXY 0, 2
mvXY 0, 2
mvXY 18, 0
mvXY 0, 2
mvXY -2, 0
mvXY -16, 0
mvXY 0, 2
mvXY 2, 0
mvXY 8, 0
mvXY 0, 2
mvXY -4, 0
mvXY -4, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 2, 0
mvXY 0, 0
mvXY 0, 2
mvXY 0, 2
mvXY 4, 0
upPen
mvXY 16, -30
downPen
mvXY 164, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 2, 0
mvXY 158, 0
mvXY 0, 2
mvXY -158, 0
mvXY 0, 2
mvXY 158, 0
mvXY 0, 2
mvXY -158, 0
mvXY 0, 2
mvXY 158, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 160, 0
mvXY -162, 0
mvXY 0, 2
mvXY 162, 0
mvXY -166, 0
mvXY 0, 2
mvXY 166, 0
mvXY -170, 0
mvXY 0, 2
mvXY 170, 0
mvXY -174, 0
mvXY 0, 2
mvXY 10, 0
mvXY -12, 0
upPen
mvXY -28, -18
downPen
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
upPen
mvXY 16, -24
downPen
mvXY 10, 0
upPen
mvXY -56, 8
downPen
mvXY 0, 2
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY -4, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -6, 0
mvXY 0, 2
mvXY 6, 0
mvXY -8, 0
mvXY 0, 2
mvXY 8, 0
mvXY 0, 2
mvXY -10, 0
upPen
mvXY 76, -6
downPen
mvXY 160, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 160, 0
mvXY 0, 2
mvXY -160, 0
upPen
mvXY -84, 14
downPen
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
upPen
mvXY 12, -14
downPen
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 0
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
upPen
mvXY 14, -14
downPen
mvXY 8, 0
mvXY 0, 2
mvXY -2, 0
mvXY -6, 0
mvXY 0, 2
mvXY 2, 0
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
upPen
mvXY 20, -6
downPen
mvXY 6, 0
mvXY 0, 2
mvXY -2, 0
mvXY -4, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
upPen
mvXY 14, -16
downPen
mvXY 0, 0
upPen
mvXY 8, 0
downPen
mvXY 8, 0
mvXY 0, 2
mvXY -6, 0
mvXY 0, 2
mvXY 6, 0
mvXY 0, 2
mvXY -6, 0
upPen
mvXY 14, -6
downPen
mvXY 156, 0
mvXY 0, 2
mvXY -156, 0
mvXY 0, 2
mvXY 156, 0
mvXY 0, 2
mvXY -156, 0
mvXY 0, 2
mvXY 156, 0
mvXY -158, 0
mvXY 0, 2
mvXY 158, 0
mvXY 0, 2
mvXY -158, 0
mvXY 0, 2
mvXY 158, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 160, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 160, 0
mvXY 0, 2
mvXY -160, 0
mvXY 0, 2
mvXY 160, 0
mvXY -162, 0
mvXY 0, 2
mvXY 162, 0
upPen
mvXY -202, -24
downPen
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 6, 0
mvXY -8, 0
upPen
mvXY 30, -24
downPen
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 6, 0
upPen
mvXY -50, -22
downPen
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -4, 0
mvXY 0, 2
mvXY 6, 0
mvXY -8, 0
upPen
mvXY 12, -14
downPen
mvXY 0, 2
mvXY 0, 2
upPen
mvXY 26, -4
downPen
mvXY 0, 0
mvXY 0, 2
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY -4, 0
mvXY 0, 2
mvXY 4, 0
mvXY 0, 2
mvXY -6, 0
upPen
mvXY 24, -14
downPen
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 0
upPen
mvXY -70, 0
downPen
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -2, 0
mvXY 0, 2
mvXY 2, 0
mvXY 0, 2
mvXY -4, 0
mvXY 6, 0
mvXY 0, 2
mvXY -6, 0


upPen
upPen


End Sub
Private Sub ExitProgram_Click()
If MSComm1.PortOpen = True Then MSComm1.PortOpen = False
Unload UserForm1
UserForm1.Hide
Reset
End Sub
Private Sub Port1_Click()
If MSComm1.CommPort = 2 Then MSComm1.CommPort = 1
'End If
End Sub
Private Sub port2_Click()
If MSComm1.CommPort = 1 Then MSComm1.CommPort = 2
'End If
End Sub

Private Sub moveXY(ByVal x As Integer, ByVal y As Integer)
    xDisp = xDisp + x
    yDisp = yDisp + y
    outStr = Trim(Str(x)) + " " + Trim(Str(y)) + " " + move + enter
    MSComm1.Output = outStr
    'MSComm1.Output = XYStr(x, y)
End Sub

Private Sub initComm(vel As Integer)

    If MSComm1.PortOpen = False Then MSComm1.PortOpen = True
    
    If Not inited Then
        sent = "0 0 9900 9900 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        'sent = "0 0 move" + enter
        'Debug.Print sent
        'MSComm1.Output = sent
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        inited = True
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    End If
    
    
    
    ' default speed
    sent = Trim(Str(vel)) + " setvel" + enter
    Debug.Print sent
    MSComm1.Output = sent
    Speed = vel

End Sub
Private Sub Pause(t As Integer)
    If True Then ' Put as false to disable 'globally'
        Start = Timer
        Do While Timer < Start + t
            DoEvents
'            If Timer < Start Then Start = Start - 24 * 60 * 60
        Loop
    End If
End Sub

Private Sub UserForm_Initialize()

enter = Chr(13) ' enter command
space = Chr(32) ' space command
move = Chr(114) ' move command
neg = Chr(45)   ' - ascii


x0 = 48
x1 = 49
x2 = 50
x3 = 51
x4 = 52
x5 = 53
x6 = 54
x7 = 55
x8 = 56
x9 = 57

MSComm1.Settings = "9600,N,8,1" ' communication setting
If Not MSComm1.PortOpen Then MSComm1.PortOpen = True

oldSpd = 150
edSpeed.Text = Trim(Str(oldSpd))

inited = False

mInstCnt = 0
mCumTime = 0

xDisp = 0
yDisp = 0

initComm (200)

End Sub

Private Sub mvXY(ByVal x As Integer, ByVal y As Integer)
    Dim Dist As Single
    Dim t As Single
    
    moveXY x, y
    Dist = Sqr(CSng(x) * x + CSng(y) * y)
    
    t = Dist / Speed
    If (t > 1) Then
        mCumTime = 0
        mInstCnt = 0
        Pause Int(t) + 1
    Else
        mCumTime = mCumTime + t
        mInstCnt = mInstCnt + 1
        If (mInstCnt > 3) Then
            Pause Int(mCumTime) + 1
            mCumTime = 0
            mInstCnt = 0
        End If
    End If
End Sub

Sub upPen()
    MsgBox ("Off laser 1/3")
End Sub

Sub downPen()
    MsgBox ("on laser")
End Sub



