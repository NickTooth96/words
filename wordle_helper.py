import ast
import sys
import subprocess
import os
from PySide6 import QtCore, QtWidgets, QtGui # type: ignore
# from PyQt5.QtWidgets import QLineEdit, QLabel


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Defualt values
        self.pattern = "....."
        self.has = ""
        self.hasnot = ""
        self.non_pattern = ""
        self.cmd = "python3 main.py --pattern " + self.pattern + " --has " + self.has + " --hasnot " + self.hasnot + " --non_pattern " + self.non_pattern
        
        self.button = QtWidgets.QPushButton("Run")
        self.button.setToolTip("Click to run the script with selected parameters")
        self.button.setFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold))


        self.text = QtWidgets.QLabel("Wordle Helper",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text.setFont(QtGui.QFont("Times", 48, QtGui.QFont.Bold))

        self.button.clicked.connect(self.run_script) 

        self.text_pattern = QtWidgets.QLabel("Pattern") 
        self.text_pattern.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)) 

        self.text_has = QtWidgets.QLabel("Yellow Letters")
        self.text_has.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.text_hasnot = QtWidgets.QLabel("Black Letters")
        self.text_hasnot.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.text_non_pattern = QtWidgets.QLabel("Non Pattern")
        self.text_non_pattern.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))   

        # add text input box
        self.pattern = QtWidgets.QLineEdit()
        self.pattern.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.pattern.setPlaceholderText("Enter Data Source File Path or URL")
        self.pattern.textChanged.connect(self.on_text_changed)
        self.pattern.setText(".....")
        # self.pattern.setStyleSheet("QLineEdit { background-color: yellow }")

        self.has = QtWidgets.QLineEdit()
        self.has.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.has.setPlaceholderText("Enter Yellow Letters (if any)")
        self.has.textChanged.connect(self.on_text_changed)
        # self.has.setStyleSheet("QLineEdit { font-weight: bold; color: yellow; background-color: white;}")

        self.hasnot = QtWidgets.QLineEdit()
        self.hasnot.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.hasnot.setPlaceholderText("Enter Black Letters (if any)")
        self.hasnot.textChanged.connect(self.on_text_changed)

        self.non_pattern = QtWidgets.QLineEdit()
        self.non_pattern.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.non_pattern.setPlaceholderText("Enter Patterns not matching separated by commas with NO spaces. EX: ...a.,..e..")
        self.non_pattern.textChanged.connect(self.on_text_changed)

        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.words_found = QtWidgets.QLabel("Words Found")
        self.words_found.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.error = QtWidgets.QMessageBox()
        self.error.setIcon(QtWidgets.QMessageBox.Critical)
        self.error.setText("An error has occured")
        self.error.setWindowTitle("Input Error")
        self.error.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.plurals = QtWidgets.QCheckBox("Exclude Plurals?")
        self.plurals.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.plurals.setChecked(False)
        self.plurals.stateChanged.connect(self.exclude_plurals)
        

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(self.text)
        self.layout.addRow(self.text_pattern, self.pattern)
        self.layout.addRow(self.text_hasnot, self.hasnot)
        self.layout.addRow(self.text_has, self.has)        
        self.layout.addRow(self.text_non_pattern, self.non_pattern)
        self.layout.addRow(self.plurals)
        self.layout.addRow(self.button)  
        self.layout.addRow(self.words_found)    
        self.layout.addWidget(self.list_widget)




    @QtCore.Slot()
    def exclude_plurals(self):
        pass

    def on_text_changed(self):
        self.button.setEnabled(bool(self.pattern.text()))

    def run_script(self):
        # get the values from the text boxes
        pattern = self.pattern.text()
        has = self.has.text()
        hasnot = self.hasnot.text()
        non_pattern = self.non_pattern.text()

        if self.plurals.isChecked():
            if len(non_pattern) > 0:
                non_pattern += ",....s"
            else:
                non_pattern = "....s"

        script_path = os.path.join(os.path.dirname(__file__), 'main.py')

        cmd = ["python3", script_path,"--pattern", pattern]

        if has:
            cmd.extend(["--has", has])
        
        if hasnot:
            cmd.extend(["--has-not", hasnot])

        if non_pattern:
            cmd.extend(["--non", non_pattern])

        # run the script      
        
        try:
            # print(f"Running command: {' '.join(cmd)}")
            script = subprocess.run(cmd, check=True, text=True, capture_output=True)
            result = ast.literal_eval(script.stdout)
            words = result[0]
            words_found = result[1]
            words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)}

            # remove all items from the list widget
            self.list_widget.clear()

            i = 1
            self.list_widget.addItem("-- Top Choice --")
            for word in words:
                if words[word] == 100:                    
                    item = QtWidgets.QListWidgetItem(f"{i}: {word} {words[word]}")
                    self.list_widget.addItem(item)
                    i += 1
            if i < len(words.values()):
                self.list_widget.addItem("-- Less Likely Choices --")
            for word in words:
                if words[word] < 100:
                    item = QtWidgets.QListWidgetItem(f"{i}: {word} {words[word]}")
                    self.list_widget.addItem(item)
                    i += 1
                
            
            self.words_found.setText(f"Words Found: {words_found}")

        except subprocess.CalledProcessError as e:
            self.error.setInformativeText(f"{check_error(e, cmd)}")
            self.error.exec()

def check_error(error, command):

    
    idx_pattern = command.index("--pattern") + 1
    idx_has = command.index("--has") + 1 if "--has" in command else None
    idx_hasnot = command.index("--has-not") + 1 if "--has-not" in command else None
    
    if have_common_elements(command[idx_has], command[idx_hasnot])[0]:
        common = have_common_elements(command[idx_has], command[idx_hasnot])[1].pop()
        msg = f"Yellow and Black letters \nhave common element '{common}'.\n"
        msg += "Please remove the common element from either Yellow or Black letters.\n"
        msg += f"Consider input similar to '..{common}..' in Non Pattern."
    elif have_common_elements(command[idx_pattern], command[idx_hasnot])[0]:
        common = have_common_elements(command[idx_hasnot], command[idx_pattern])[1].pop()
        msg = f"Pattern and Black letters have common element '{common}'.\n"
        msg += f"Remove the '{common}' from Black letters."
        msg += f"Use input similar to '..{common}..' in Non Pattern instead."
    else: 
        msg = error
    return msg

def have_common_elements(a, b):
    common_elements = set()
    for char in a:
        if char in b:
            common_elements.add(char)
    return bool(set(a) & set(b)), common_elements

   


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())