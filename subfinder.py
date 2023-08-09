# coding: utf-8# coding: utf-8


from burp import IBurpExtender, ITab
from javax.swing import JPanel, JButton, JTextArea, JTextField, JLabel, JScrollPane
import subprocess
import os

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("Subfinder Runner")

        # Create the GUI
        self.panel = JPanel()
        self.label = JLabel("Enter the domain:")
        self.domain_field = JTextField(25)
        self.run_button = JButton("Run subfinder", actionPerformed=self.run_subfinder)
        self.output_area = JTextArea(25, 80)
        self.output_area.setEditable(False)
        scroll = JScrollPane(self.output_area)

        self.panel.add(self.label)
        self.panel.add(self.domain_field)
        self.panel.add(self.run_button)
        self.panel.add(scroll)

        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "Subfinder Runner"

    def getUiComponent(self):
        return self.panel

    def run_subfinder(self, event):
        domain = self.domain_field.getText().strip()
        if domain:
            self.output_area.setText("Running subfinder for domain: {}\n".format(domain))
            try:
                env = dict(os.environ, PATH="/usr/bin")
                process = subprocess.Popen(['subfinder', '-d', domain], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.output_area.append(output)
                rc = process.poll()
            except Exception as e:
                self.output_area.append("Error: {}\n".format(str(e)))
                return
        else:
            self.output_area.setText("Please enter a domain.\n")
