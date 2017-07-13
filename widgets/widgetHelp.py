from popUps import PopUp
from backend.consts import INFO

class WidgetHelp(PopUp):
    """
    Child popup that has long text. I decided to make popups with long text their
    own widget so that they don't make the main.py file messy.
    """
    def __init__(self, parent=None):
        self.text = 'How To Use\n\n1. Add in member information, and click "Add Member"'+\
        'to add the member to the design. The easiest way is to add all members first, '+\
        'then joints. But you can begin adding joints as soon as 2 members have been added.\n\n'+\
        '2. To add joints, click "Begin Joint Creation". Select each member that appears on the '+\
        'joint. VERY IMPORTANT: when creating joints, view the design from one side (right or left) '+\
        'and then add the members in the order they appear. Stay consistent for all joints! When '+\
        'done adding joints, click "Add New Joints".\n\n3. When done creating the design, or while '+\
        'creating it, you can verify the members and joints by clicking "View Components". \n\n'+\
        '4. When done and ready, click "Calculate!" The Components/Results should fill up with the '+\
        'results, and will be displayed to you.\n\nVERY IMPORTANT! All measurements are based on METERS.'
        super(WidgetHelp, self).__init__(self.text, INFO, parent=parent)
