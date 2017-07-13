from popUps import PopUp
from backend.consts import INFO

class WidgetDevelopment(PopUp):
    """
    Child popup that has long text. I decided to make popups with long text their
    own widget so that they don't make the main.py file messy.
    """
    def __init__(self, parent=None):
        self.text = 'Developed by: Sam Raisbeck (Mechatronics Engineering Student of 2020 at the University of Waterloo)\n'+\
        'Developed for: MTE219 Truss Project (instructor: Prof. Hamid Jahed)\n\n'+\
        'This project is still under development for experiential purposes more than anything. '+\
        'It originally was a very simple command line calculating program, but has turned into a more '+\
        'customizable GUI application.\n\nIf you would like to use any of this code, please include the '+\
        'following in a comment of the utilized code:\n\nCopyright (c) 2017 Sam Raisbeck.\nI am allowing '+\
        'anyone to use and/or alter this code, provided that they paste the copyright, this message, and the following into '+\
        'their project:\nObtained at https://github.com/samraisbeck/MTE219-Truss-Calculator'
        super(WidgetDevelopment, self).__init__(self.text, INFO, parent=parent)
