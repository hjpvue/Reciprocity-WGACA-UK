from ._anvil_designer import NewsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import blue, bright_blue

class News(NewsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.title.background = bright_blue
    # Any code you write here will run when the form opens.