program FL;

uses
  Forms,SysUtils,Windows,ShellApI,
  Unit2 in 'Unit2.pas' {Form1};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TForm1, Form1);
  //******��������Դ�ķ���·��*************//
  Form1.ADO.ConnectionString :='Provider=Microsoft.Jet.OLEDB.4.0;' +
         'Persist Security Info=False;Data Source=' +
         ExtractFilePath(Application.ExeName) + 'TXT\��������.mdb';
  If ParamCount >0 Then Begin
    Form1.ToHandle :=StrtoInt(ParamStr(1));
    IF Form1.ToHandle <> 0 Then
      PostMessage(Form1.ToHandle,WMA_InterPro,Form1.Handle,Form1.Handle);
  End Else Begin
  //****���нӿ����������������ľ�������ӿ����***************//
  ShellExecute(Application.Handle, Nil,Pchar(ExtractFilePath(Application.ExeName) + 'Wx.exe'),
         Pchar(IntToStr(Form1.Handle)), Nil, SW_SHOWNORMAL);
  End;
  //********�ӿ�������к��Զ���С��������***********//
//  Application.ShowMainForm :=False;
  Application.Run;
end.
