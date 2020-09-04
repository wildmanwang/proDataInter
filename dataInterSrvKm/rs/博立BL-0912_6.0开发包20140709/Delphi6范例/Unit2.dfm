object Form1: TForm1
  Left = 236
  Top = 178
  Width = 317
  Height = 222
  Caption = 'delphi'#30340#31616#21333#25509#21475#33539#20363
  Color = clBtnFace
  Font.Charset = GB2312_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = #23435#20307
  Font.Style = []
  OldCreateOrder = False
  OnCloseQuery = FormCloseQuery
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 12
  object Label1: TLabel
    Left = 39
    Top = 60
    Width = 24
    Height = 12
    Caption = #20869#23481
  end
  object Label2: TLabel
    Left = 16
    Top = 20
    Width = 60
    Height = 12
    Caption = #21457#36865#26041#32534#21495
  end
  object Label3: TLabel
    Left = 160
    Top = 20
    Width = 60
    Height = 12
    Caption = #25509#25910#26041#32534#21495
  end
  object Edt_Send: TEdit
    Left = 80
    Top = 20
    Width = 68
    Height = 20
    MaxLength = 3
    TabOrder = 0
    Text = '001'
  end
  object Memo_Cont: TMemo
    Left = 79
    Top = 60
    Width = 214
    Height = 49
    Lines.Strings = (
      #20170#22825#23458#20154#22810#65292#35831#21152#24555#36895#24230'.')
    TabOrder = 1
  end
  object Button1: TButton
    Left = 119
    Top = 154
    Width = 75
    Height = 25
    Caption = #21457#36865#30701#20449
    TabOrder = 2
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 215
    Top = 154
    Width = 75
    Height = 25
    Caption = #20851#38381
    TabOrder = 3
    OnClick = Button2Click
  end
  object Edt_Receive: TEdit
    Left = 224
    Top = 20
    Width = 68
    Height = 20
    MaxLength = 3
    TabOrder = 4
    Text = '012'
  end
  object Button3: TButton
    Left = 15
    Top = 154
    Width = 75
    Height = 25
    Caption = #19979#36733
    TabOrder = 5
    OnClick = Button3Click
  end
  object CheckBox1: TCheckBox
    Left = 24
    Top = 122
    Width = 257
    Height = 17
    Caption = #25910#21040#28857#33756#25968#25454#21518#22238#36865'"'#28857#33756#25104#21151'"'#20197#21024#38500#25968#25454
    TabOrder = 6
  end
  object Timer1: TTimer
    Enabled = False
    Interval = 2000
    Left = 128
    Top = 264
  end
  object ADO: TADOConnection
    ConnectionString = 
      'Provider=Microsoft.Jet.OLEDB.3.51;Persist Security Info=False;Da' +
      'ta Source=D:\exe\TXT\'#33539#20363#25968#25454'.mdb'
    LoginPrompt = False
    Mode = cmShareDenyNone
    Provider = 'Microsoft.Jet.OLEDB.4.0'
    Left = 40
    Top = 80
  end
  object TmpQry: TADOQuery
    Connection = ADO
    Parameters = <>
    Left = 8
    Top = 80
  end
end
