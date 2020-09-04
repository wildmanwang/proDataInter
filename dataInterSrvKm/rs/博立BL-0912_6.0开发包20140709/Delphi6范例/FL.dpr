program FL;

uses
  Forms,SysUtils,Windows,ShellApI,
  Unit2 in 'Unit2.pas' {Form1};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TForm1, Form1);
  //******设置数据源的访问路径*************//
  Form1.ADO.ConnectionString :='Provider=Microsoft.Jet.OLEDB.4.0;' +
         'Persist Security Info=False;Data Source=' +
         ExtractFilePath(Application.ExeName) + 'TXT\范例数据.mdb';
  If ParamCount >0 Then Begin
    Form1.ToHandle :=StrtoInt(ParamStr(1));
    IF Form1.ToHandle <> 0 Then
      PostMessage(Form1.ToHandle,WMA_InterPro,Form1.Handle,Form1.Handle);
  End Else Begin
  //****运行接口软件，并把主窗体的句柄传给接口软件***************//
  ShellExecute(Application.Handle, Nil,Pchar(ExtractFilePath(Application.ExeName) + 'Wx.exe'),
         Pchar(IntToStr(Form1.Handle)), Nil, SW_SHOWNORMAL);
  End;
  //********接口软件运行后自动缩小到托盘里***********//
//  Application.ShowMainForm :=False;
  Application.Run;
end.
