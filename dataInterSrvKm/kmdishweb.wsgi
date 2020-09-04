# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import sys
from os import path

sPath = path.abspath(path.dirname(__file__))
sys.path.insert(0, sPath)

from interService import server

application = server