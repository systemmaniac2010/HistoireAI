def find(command,array):
    for word in array:
        if word in command:
            x = word
            return word
negative = ['no','do not','never',"don't",'dont']
song = ['want to hear','play','want to listen','wanna hear','wanna listen']
ucr = ['please say the command again','repeat the command again','repeat','pardon','come again','i dont understand']
search = ['search for','search','who','what','where','why','when','how','does','do','show me','image','picture','show']
rsearch = ['search for','search','show me','show us','show']
invoke = ['go to','go','open']
websites = ['youtube','facebook','instagram','snapchat','twitter','x','telegram','google','spotify','netflix','amazon prime','hotstar','disney+','crunchyroll','whatsapp','chatgpt','gemini','reddit','threads','support','project','yt','fb','insta','snap','prime video','disney plus','disneyplus','disney']
weblinks = ['https://www.youtube.com/','https://www.facebook.com/','https://www.instagram.com/','https://www.snapchat.com/','https://x.com/','https://x.com/','https://web.telegram.org/','https://www.google.com/','https://open.spotify.com/','https://www.netflix.com','https://www.primevideo.com/','https://www.hotstar.com/','https://www.disneyplus.com/','https://www.crunchyroll.com/','https://web.whatsapp.com/','https://chatgpt.com/','https://gemini.google.com/','https://www.reddit.com/','https://www.threads.net/','https://github.com/systemmaniac2010/HistoireAI/issues','https://github.com/systemmaniac2010/HistoireAI','https://www.youtube.com/','https://www.facebook.com/','https://www.instagram.com/','https://www.snapchat.com/','https://www.primevideo.com/','https://www.disneyplus.com/','https://www.disneyplus.com/','https://www.disneyplus.com/']
troubleshooters = ['update','printer','audio','network adaptor','network','wifi','bluetooth','power','app','video','search','index','mic','recording','program','compatibility','keyboard','camera','speaker']
tcommands = ['msdt.exe /id WindowsUpdateDiagnostic','msdt.exe /id PrinterDiagnostic','msdt.exe /id AudioPlaybackDiagnostic','msdt.exe /id NetworkDiagnosticsNetworkAdapter','msdt.exe /id NetworkDiagnosticsNetworkAdapter','msdt.exe /id NetworkDiagnosticsNetworkAdapter','msdt.exe /id DeviceDiagnostic','msdt.exe /id PowerDiagnostic','msdt.exe /id WindowsStoreAppsDiagnostic','msdt.exe /id VideoPlaybackDiagnostic','msdt.exe /id SearchDiagnostic','msdt.exe /id SearchDiagnostic','msdt.exe /id AudioRecordingDiagnostic','msdt.exe /id AudioRecordingDiagnostic','msdt.exe /id ProgramCompatibilityDiagnostic','msdt.exe /id ProgramCompatibilityDiagnostic','msdt.exe /id KeyboardDiagnostic','msdt.exe /id DeviceDiagnostic','msdt.exe /id AudioPlaybackDiagnostic']
apps = ['settings','app store','windows store','microsoft store','cmd','terminal','command line','command prompt','powershell','browser','microsoft edge','edge','explorer','notepad']
appcommand = ['start ms-settings:','start ms-windows-store:','start ms-windows-store:','start ms-windows-store:','powershell -Command "Start-Process cmd -Verb RunAs"','powershell -Command "Start-Process cmd -Verb RunAs"','powershell -Command "Start-Process cmd -Verb RunAs"','powershell -Command "Start-Process cmd -Verb RunAs"','powershell -Command "Start-Process powershell -Verb RunAs"','start https://www.google.com','start msedge','start msedge','explorer','notepad']
devices = ['pc','computer','device','desktop','laptop','tablet']
edparams = ['firewall','defender','antivirus','wifi','network','bluetooth']
enablecommands = ['netsh advfirewall set allprofiles state on','sc start WinDefend','sc start WinDefend','netsh interface set interface "Wi-Fi" enabled','netsh interface set interface "Wi-Fi" enabled','powershell -Command "Start-Service bthserv"']
disablecommands = ['netsh advfirewall set allprofiles state off','sc stop WinDefend','sc stop WinDefend','netsh interface set interface "Wi-Fi" disabled','netsh interface set interface "Wi-Fi" disabled','powershell -Command "Stop-Service bthserv"']






