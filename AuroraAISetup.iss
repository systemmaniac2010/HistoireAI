; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E2A9940E-E218-42A2-B4DC-C33231B55337}
AppName=Aurora AI
AppVersion=1.0.0
;AppVerName=Aurora AI 1.0.0
AppPublisher=systemmaniac2010
AppPublisherURL=https://github.com/systemmaniac2010/AuroraAI
AppSupportURL=https://github.com/systemmaniac2010/AuroraAI
AppUpdatesURL=https://github.com/systemmaniac2010/AuroraAI
DefaultDirName={autopf}\Aurora AI
; "ArchitecturesAllowed=x64compatible" specifies that Setup cannot run
; on anything but x64 and Windows 11 on Arm.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" requests that the
; install be done in "64-bit mode" on x64 or Windows 11 on Arm,
; meaning it should use the native 64-bit Program Files directory and
; the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
LicenseFile=C:\Users\Aurora\Downloads\LICENSE.txt
InfoAfterFile=C:\Users\Aurora\Documents\Aurora AI User Manual Setup.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SetupIconFile=C:\Users\Aurora\Documents\AuroraAI\images\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Aurora\Documents\AuroraAI\Aurora.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Aurora\Documents\AuroraAI\themes\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Aurora\Documents\AuroraAI\images\*"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\Aurora AI"; Filename: "{app}\Aurora.exe"
Name: "{autodesktop}\Aurora AI"; Filename: "{app}\Aurora.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Aurora.exe"; Description: "{cm:LaunchProgram,Aurora AI}"; Flags: nowait postinstall skipifsilent
