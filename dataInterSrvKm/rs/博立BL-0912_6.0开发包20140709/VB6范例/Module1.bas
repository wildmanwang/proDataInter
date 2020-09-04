Attribute VB_Name = "Module1"

Option Explicit

Public Const GWL_WNDPROC = -4
Public Const GWL_USERDATA = (-21)
Public Const WM_SIZE = &H5
Public Const WM_USER = &H400
Public Const WM_CLOSE = &H10
Public Const WM_DESTORY = &H2
Public Const WM_QUIT = &H12
Public Const WMA_InterPro = &H500 '�����ͨ�ŵ���Ϣ��
Public Const SW_SHOWNORMAL = 1
'***********��������ֵ********
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

Public ToHandle As Long '�Է�����ľ��(���)
Public lHwndA As Long '��������ľ��(����)

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
    'ָ���Զ���Ĵ��ڹ���
    pOld = SetWindowLong(hWnd, GWL_WNDPROC, AddressOf WindowProc)
    '����ԭ��Ĭ�ϵĴ��ڹ���ָ��
    SetWindowLong hWnd, GWL_USERDATA, pOld
    Hook = pOld
End Function

Public Sub UnHook(ByVal hWnd As Long, ByVal lpWndProc As Long)
    Dim temp As Long
    temp = SetWindowLong(hWnd, GWL_WNDPROC, lpWndProc)
End Sub

'������Ϣ���жϹ���
Public Function WindowProc(ByVal hw As Long, ByVal uMsg As Long, _
    ByVal wParam As Long, ByVal lParam As Long) As Long

    Dim lpPrevWndProc As Long
    Dim lResult As Long
    Dim sReturnData As String
    Dim sFileName As String
    
     '�ж��ǲ��ǶԷ�����������Ϣ
    If uMsg = WMA_InterPro Then
       frmMain.txtHook = frmMain.txtHook & _
                    "hw=" & hw & ";uMsg=" & uMsg & ";wParam=" & wParam & ";lParam=" & lParam & vbCrLf
                    
        If ToHandle = 0 Then
            ToHandle = lParam
        '**********���ػ����Ա��½***********'
        ElseIf lParam = 10 Or lParam = 11 Then
        
            sReturnData = "1"

            sFileName = App.Path & "\TXT\DL" & ".TXT"

            SaveData sReturnData, sFileName
            '��������Ӧ�Ĳ������ͷ�����Ϣ
            '��ע����VB�д�����Ϣʱ�Ĳ������÷�ʽ
            lResult = PostMessage(ToHandle, WMA_InterPro, 0, ByVal lParam&)
                       
  '          frmMain.txtHook = frmMain.txtHook & vbCrLf & _
  '                  "ToHandle=" & ToHandle & " ;WMA_InterPro=" & WMA_InterPro & " ;wParam=" & wParam & " ;lParam=" & lParam & " ;lResult=" & lResult

        Else
          sFileName = App.Path & "\TXT\T" & lParam & ".TXT"
          '��������Ӹ�����Ϣ������Ҫ������Ĺ���
          sReturnData = ReadData(sFileName) + "�Ѿ��������!"
          sFileName = App.Path & "\TXT\R" & lParam & ".TXT"
          lResult = SaveData(sReturnData, sFileName)
          lResult = PostMessage(ToHandle, WMA_InterPro, 0, ByVal lParam&)
        End If

    End If

    '��ѯԭ��Ĭ�ϵĴ��ڹ���ָ��
    lpPrevWndProc = GetWindowLong(hw, GWL_USERDATA)

    '����ԭ���Ĵ��ڹ���
    WindowProc = CallWindowProc(lpPrevWndProc, hw, uMsg, wParam, lParam)
End Function
'���ַ������浽�ļ���
Private Function SaveData(strData As String, strFileName As String) As Long
 
    On Error GoTo SysErr:
    Dim i As Integer

    SaveData = 1
                     
    Open strFileName For Output As #1              'д�ļ�
        Print #1, strData
    Close #1
    
    Exit Function
SysErr:
    Close #1
    MsgBox Err.Description

    Err.Clear

End Function

'���ļ��ж�ȡ����
Private Function ReadData(strFileName As String) As String
  Dim StrLine, Dd  As String
  Open strFileName For Input As #1
     Do While Not EOF(1)
     Line Input #1, StrLine                             '���ļ�
     Dd = Dd + StrLine + Chr(13) + Chr(10)
     Loop
     ReadData = Dd
     Close #1

End Function
