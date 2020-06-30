from distutils.core import setup
import py2exe
from pygame.locals import *

setup(console=[os.path.join(os.path.dirname(__file__,'main.py')])
