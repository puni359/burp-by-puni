# coding: utf-8

from burp import IBurpExtender, IHttpListener, ITab
from java.awt import BorderLayout, Toolkit
from javax.swing import JButton, JPanel, JTextArea, JScrollPane
from java.awt.datatransfer import StringSelection
import re

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}"

class BurpExtender(IBurpExtender, IHttpListener, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        # Множество для хранения уникальных email-адресов
        self._unique_emails = set()

        # GUI setup
        self._textArea = JTextArea()
        self._scrollPane = JScrollPane(self._textArea)
        self._panel = JPanel()
        self._panel.setLayout(BorderLayout())
        self._panel.add(self._scrollPane, BorderLayout.CENTER)

        # Кнопка для копирования
        self._copyButton = JButton("Copy to Clipboard", actionPerformed=self.copyToClipboard)
        self._panel.add(self._copyButton, BorderLayout.SOUTH)

        # Регистрация
        callbacks.setExtensionName("Email Collector")
        callbacks.registerHttpListener(self)
        callbacks.addSuiteTab(self)
        
        return

    def getTabCaption(self):
        return "Email Collector"

    def getUiComponent(self):
        return self._panel

    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        if not messageIsRequest:  # Если это ответ
            responseBytes = currentRequest.getResponse()
            responseBody = self._helpers.bytesToString(responseBytes)
            
            # Ищем email'ы
            emails = re.findall(EMAIL_PATTERN, responseBody)
            
            for email in emails:
                # Добавляем email в множество. Если он уже там есть, ничего не произойдет
                if email not in self._unique_emails:
                    self._unique_emails.add(email)
                    self._textArea.append(email + "\n")

    def copyToClipboard(self, e):
        clip = Toolkit.getDefaultToolkit().getSystemClipboard()
        clip.setContents(StringSelection(self._textArea.getText()), None)
