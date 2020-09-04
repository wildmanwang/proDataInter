VERSION 5.00
Begin VB.Form frmMain 
   Caption         =   "接口程序"
   ClientHeight    =   3240
   ClientLeft      =   165
   ClientTop       =   450
   ClientWidth     =   5850
   LinkTopic       =   "Form1"
   ScaleHeight     =   3240
   ScaleWidth      =   5850
   StartUpPosition =   2  '屏幕中心
   Begin VB.CommandButton cmdEnd 
      Caption         =   "退出(&E)"
      Height          =   495
      Left            =   3240
      TabIndex        =   1
      Top             =   2640
      Width           =   1965
   End
   Begin VB.TextBox txtHook 
      BeginProperty Font 
         Name            =   "宋体"
         Size            =   12
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   1965
      Left            =   240
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   0
      Top             =   480
      Width           =   5355
   End
   Begin VB.Label Label1 
      Caption         =   "接收到的消息:"
      Height          =   255
      Left            =   240
      TabIndex        =   2
      Top             =   240
      Width           =   1695
   End
   Begin VB.Menu mnuPopup 
      Caption         =   "ddd"
      Visible         =   0   'False
      Begin VB.Menu mnuPopupContext 
         Caption         =   "ddddd"
      End
   End
End
Attribute VB_Name = "frmMain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Dim lResult As Long

Private Sub cmdEnd_Click()
    Unload Me
End Sub


Private Sub Form_Load()

    Me.Tag = Hook(Me.hWnd)

End Sub
Private Sub Form_Unload(Cancel As Integer)
'*******保证让软件能够和程序同时关闭（软件关闭时也一样）************//
    lResult = PostMessage(ToHandle, WM_CLOSE, 0, 0)
    UnHook Me.hWnd, Me.Tag
End Sub


