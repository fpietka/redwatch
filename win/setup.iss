
[Setup]
AppName=
AppVerName=
AppPublisher=
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
DefaultDirName={pf}\RedmineTickets
DefaultGroupName=Redmine Tickets
OutputBaseFilename=RedmineTickets
OutputDir=..\dist\setup
AllowNoIcons=yes
;SetupIconFile=pyastqueues.ico
Compression=lzma
SolidCompression=yes
; required to install common Start Menu/Startup/ links
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: ..\dist\*; DestDir: "{app}"
;Source: ..\dist\images\*; DestDir: "{app}\images\"
;Source: ..\dist\locales\*; DestDir: "{app}\locales\"

[Icons]
Name: "{group}\Redmine Tickets"; Filename: "{app}\RedmineTickets.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,Redmine Tickets}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Redmine Tickets"; Filename: "{app}\RedmineTickets.exe"; Tasks: desktopicon; WorkingDir: "{app}"
;Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\pyastqueues"; Filename: "{app}\pyastqueues.exe"; Tasks: quicklaunchicon; WorkingDir: "{app}"
Name: "{commonstartup}\Redmine Tickets"; Filename: "{app}\Redmine Tickets.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\RedmineTickets.exe"; Description: "{cm:LaunchProgram,RedmineTickets}"; Flags: nowait postinstall skipifsilent

[InstallDelete]
;Type: filesandordirs; Name: "{userappdata}\pyastqueues.ini"
Type: filesandordirs; Name: "{app}\RedmineTickets.exe.log"

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\pyastqueues.ini"
Type: filesandordirs; Name: "{app}\RedmineTickets.exe.log"

[Languages]
Name: "fr"; MessagesFile: "compiler:Languages/French.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

