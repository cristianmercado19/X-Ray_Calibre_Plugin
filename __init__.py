#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
'''Creates plugin for Calibre to allow users to create x-ray, author profile, start actions, and end actions for devices'''

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2016, Samreen Zarroug, Anthony Toole, & Alex Mayer'
__docformat__ = 'restructuredtext en'

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase

class XRayCreatorPlugin(InterfaceActionBase):
    '''Initializes X-Ray Creator Plugin'''
    name = 'X-Ray Creator'
    description = 'A plugin to create X-Ray files for Kindle books'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Samreen Zarroug, Anthony Toole, & Alex Mayer'
    version = (3, 0, 1)
    minimum_calibre_version = (2, 0, 0)
    actual_plugin = 'calibre_plugins.xray_creator.ui:XRayCreatorInterfacePlugin'

    @staticmethod
    def is_customizable():
        '''Tells Calibre that this widget is customizable'''
        return True

    @staticmethod
    def config_widget():
        '''Creates preferences dialog'''
        from calibre_plugins.xray_creator.config import ConfigWidget
        return ConfigWidget()

    @staticmethod
    def save_settings(config_widget):
        '''Saves preferences into book setting's json file'''
        config_widget.save_settings()

    def do_user_config(self, parent=None):
        '''
        This method shows a configuration dialog for this plugin. It returns
        True if the user clicks OK, False otherwise. The changes are
        automatically applied.
        '''
        from PyQt5.Qt import QDialog, QDialogButtonBox, QVBoxLayout
        from calibre.gui2 import gprefs

        prefname = 'plugin config dialog:' + self.type + ':' + self.name
        geom = gprefs.get(prefname, None)

        config_dialog = QDialog(parent)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout = QVBoxLayout(config_dialog)

        def size_dialog():
            '''Sets size of dialog'''
            if geom is None:
                config_dialog.resize(config_dialog.sizeHint())
            else:
                config_dialog.restoreGeometry(geom)

        button_box.accepted.connect(lambda: self.validate(config_dialog, config_widget))
        button_box.rejected.connect(config_dialog.reject)
        config_dialog.setWindowTitle('Customize ' + self.name)

        config_widget = self.config_widget()
        layout.addWidget(config_widget)
        layout.addWidget(button_box)
        size_dialog()
        config_dialog.exec_()

        geom = bytearray(config_dialog.saveGeometry())
        gprefs[prefname] = geom

        return config_dialog.result()

    def validate(self, config_dialog, config_widget):
        '''Validates config widget info'''
        if config_widget.validate():
            config_dialog.accept()
            self.save_settings(config_widget)
