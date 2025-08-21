; -------------------------------
; Telecom Manager Installer
; -------------------------------

[Setup]
AppName=El-Hussiny Telecom
AppVersion=2.0
AppPublisher=Masr
AppPublisherURL=http://www.dark.great-site.net/?i=1
DefaultDirName={pf}\El-Hussiny Telecom
DefaultGroupName=El-Hussiny Telecom
DisableProgramGroupPage=yes
OutputBaseFilename=El-Hussiny-TelecomSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=app.ico
UninstallDisplayIcon={app}\El-Hussiny-Telecom.exe

[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; كل ملفات البرنامج من PyInstaller
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\El-Hussiny Telecom"; Filename: "{app}\El-Hussiny-Telecom.exe"
Name: "{commondesktop}\El-Hussiny Telecom"; Filename: "{app}\El-Hussiny-Telecom.exe"; Tasks: desktopicon

[Run]
; تشغيل البرنامج بعد التثبيت
Filename: "{app}\El-Hussiny-Telecom.exe"; Description: "تشغيل Telecom Manager"; Flags: nowait postinstall skipifsilent
