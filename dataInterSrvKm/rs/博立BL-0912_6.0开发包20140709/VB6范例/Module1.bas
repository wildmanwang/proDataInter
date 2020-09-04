Attribute VB_Name = "Module1"

Option Explicit

Public Const GWL_WNDPROC = -4
Public Const GWL_USERDATA = (-21)
Public Const WM_SIZE = &H5
Public Const WM_USER = &H400
Public Const WM_CLOSE = &H10
Public Const WM_DESTORY = &H2
Public Const WM_QUIT = &H12
Public Const WMA_InterPro = &H500 '与软件通信的消息号
Public Const SW_SHOWNORMAL = 1
'***********参数类型值********
Public Const CX_OK = 0
Public Const CX_DC1 = 1
Public Const CX_DC2 = 2
Public Const CX_DC3 = 3
Public Const CX_DC4 = 4
Public Const CX_DC5 = 5
Public Const CX_DC6 = 6
Public Const CX_DC7 = 7
Public Const CX_DC8 = 8
Public Const CX_Login = 10
Public Const CX_Down = 11

Public ToHandle As Long '对方窗体的句柄(软件)
Public lHwndA As Long '本方窗体的句柄(程序)

Public Declare Function PostMessage& Lib "user32" Alias "PostMessageA" (ByVal hWnd As Long, ByVal wMsg As Long, ByVal wParam As Long, lParam As Any)

Public Declare Function SendMessage Lib "user32" Alias "SendMessageA" (ByVal hWnd As Long, ByVal wMsg As Long, ByVal wParam As Long, lParam As Any) As Long

Public Declare Function CallWindowProc Lib "user32" Alias "CallWindowProcA" (ByVal lpPrevWndFunc As Long, ByVal hWnd As Long, ByVal Msg As Long, ByVal wParam As Long, ByVal lParam As Long) As Long

Public Declare Function GetWindowLong Lib "user32" Alias "GetWindowLongA" (ByVal hWnd As Long, ByVal nIndex As Long) As Long

Public Declare Function SetWindowLong Lib "user32" Alias "SetWindowLongA" (ByVal hWnd As Long, ByVal nIndex As Long, ByVal dwNewLong As Long) As Long

Public Declare Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" (ByVal hWnd As Long, ByVal lpOperation As String, ByVal lpFile As String, ByVal lpParameters As String, ByVal lpDirectory As String, ByVal nShowCmd As Long) As Long

Public Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)


Sub Main()
    Dim lResult As Long
   
    Load frmMain

    lHwndA = frmMain.hWnd

    lResult = ShellExecute(lHwndA, "open", "WX.exe", CStr(lHwndA), "", SW_SHOWNORMAL)
    
    frmMain.Show
End Sub
Public Function Hook(ByVal hWnd As Long) As Long

    Dim pOld As Long
    '指定自定义的窗口过程
    pOld = SetWindowLong(hWnd, GWL_WNDPROC, AddressOf WindowProc)
    '保存原来默认的窗口过程指针
    SetWindowLong hWnd, GWL_USERDATA, pOld
    Hook = pOld
End Function

Public Sub UnHook(ByVal hWnd As Long, ByVal lpWndProc As Long)
    Dim temp As Long
    temp = SetWindowLong(hWnd, GWL_WNDPROC, lpWndProc)
End Sub

'处理消息的判断过程
Public Function WindowProc(ByVal hw As Long, ByVal uMsg As Long, _
    ByVal wParam As Long, ByVal lParam As Long) As Long

    Dim lpPrevWndProc As Long
    Dim lResult As Long
    Dim sReturnData As String
    Dim sFileName As String
    
     '判断是不是对方发过来的消息
    If uMsg = WMA_InterPro Then
       frmMain.txtHook = frmMain.txtHook & _
                    "hw=" & hw & ";uMsg=" & uMsg & ";wParam=" & wParam & ";lParam=" & lParam & vbCrLf
                    
        If ToHandle = 0 Then
            ToHandle = lParam
        '**********下载或操作员登陆***********'
        ElseIf lParam = 10 Or lParam = 11 Then
        
            sReturnData = "1"

            sFileName = App.Path & "\TXT\DL" & ".TXT"

            SaveData sReturnData, sFileName
            '处理完相应的操作后发送返回消息
            '请注意在VB中传递消息时的参数调用方式
            lResult = PostMessage(ToHandle, WMA_InterPro, 0, ByVal lParam&)
                       
  '          frmMain.txtHook = frmMain.txtHook & vbCrLf & _
  '                  "ToHandle=" & ToHandle & " ;WMA_InterPro=" & WMA_InterPro & " ;wParam=" & wParam & " ;lParam=" & lParam & " ;lResult=" & lResult

        Else
          sFileName = App.Path & "\TXT\T" & lParam & ".TXT"
          '在这里添加根据消息类型需要程序处理的过程
          sReturnData = ReadData(sFileName) + "已经处理完成!"
          sFileName = App.Path & "\TXT\R" & lParam & ".TXT"
          lResult = SaveData(sReturnData, sFileName)
          lResult = PostMessage(ToHandle, WMA_InterPro, 0, ByVal lParam&)
        End If

    End If

    '查询原来默认的窗口过程指针
    lpPrevWndProc = GetWindowLong(hw, GWL_USERDATA)

    '调用原来的窗口过程
    WindowProc = CallWindowProc(lpPrevWndProc, hw, uMsg, wParam, lParam)
End Function
'把字符串保存到文件中
Private Function SaveData(strData As String, strFileName As String) As Long
 
    On Error GoTo SysErr:
    Dim i As Integer

    SaveData = 1
                     
    Open strFileName For Output As #1              '写文件
        Print #1, strData
    Close #1
    
    Exit Function
SysErr:
    Close #1
    MsgBox Err.Description

    Err.Clear

End Function

'从文件中读取数据
Private Function ReadData(strFileName As String) As String
  Dim StrLine, Dd  As String
  Open strFileName For Input As #1
     Do While Not EOF(1)
     Line Input #1, StrLine                             '读文件
     Dd = Dd + StrLine + Chr(13) + Chr(10)
     Loop
     ReadData = Dd
     Close #1

End Function
