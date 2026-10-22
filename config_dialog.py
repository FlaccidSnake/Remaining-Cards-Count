# -*- coding: utf-8 -*-
"""
Card Counts Display Config Dialog
"""
from aqt.qt import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QFrame, QGroupBox, QCheckBox, Qt
from aqt import mw
from aqt.utils import tooltip, openFolder
import os


class CardCountsConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        config = mw.addonManager.getConfig(__name__)
        
        # Handle missing config gracefully
        if config is None:
            config = {
                "corner": "top-left",
                "show_counts": True,
                "show_animations": True,
                "underline_current_card": True,
                "font": "Minecraft.ttf",
                "base_font_size": 48
            }
        
        self.corner = config.get("corner", "top-left")
        self.show_counts = config.get("show_counts", True)
        self.show_animations = config.get("show_animations", True)
        self.underline_current_card = config.get("underline_current_card", True)
        self.font = config.get("font", "Minecraft.ttf")
        self.base_font_size = config.get("base_font_size", 48)
        
        self.setWindowTitle("Card Counts Display Configuration")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout()
        
        # Display Settings
        display_group = QGroupBox("Display Settings")
        display_layout = QVBoxLayout()
        
        # Show counts checkbox
        self.show_counts_checkbox = QCheckBox("Show card counts during reviews")
        self.show_counts_checkbox.setChecked(self.show_counts)
        display_layout.addWidget(self.show_counts_checkbox)
        
        display_info = QLabel(
            "<i>When unchecked, the card counts popup will be hidden</i>"
        )
        display_info.setWordWrap(True)
        display_layout.addWidget(display_info)
        
        # Show animations checkbox
        self.show_animations_checkbox = QCheckBox("Show animated +1/-1 change indicators")
        self.show_animations_checkbox.setChecked(self.show_animations)
        display_layout.addWidget(self.show_animations_checkbox)
        
        animations_info = QLabel(
            "<i>Displays fading +1/-1 indicators when counts change:<br>"
            "• White -1 for progress (cards completed)<br>"
            "• Red +1 for setbacks (cards added to learning queue)</i>"
        )
        animations_info.setWordWrap(True)
        display_layout.addWidget(animations_info)
        
        # Underline current card checkbox
        self.underline_checkbox = QCheckBox("Underline the count of the current card's type")
        self.underline_checkbox.setChecked(self.underline_current_card)
        display_layout.addWidget(self.underline_checkbox)
        
        underline_info = QLabel(
            "<i>Underlines the blue, red, or green number depending on whether "
            "the card you're looking at is new, learning, or review</i>"
        )
        underline_info.setWordWrap(True)
        display_layout.addWidget(underline_info)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Position Settings
        position_group = QGroupBox("Position")
        position_layout = QVBoxLayout()
        
        # Corner selection
        corner_layout = QHBoxLayout()
        corner_label = QLabel("Popup corner position:")
        self.corner_combo = QComboBox()
        self.corner_combo.addItems([
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right"
        ])
        self.corner_combo.setCurrentText(self.corner)
        corner_layout.addWidget(corner_label)
        corner_layout.addWidget(self.corner_combo)
        corner_layout.addStretch()
        position_layout.addLayout(corner_layout)
        
        corner_info = QLabel(
            "<i>Defaults to left side to avoid Card History Killfeed. "
            "Will stack below it if on the same side.</i>"
        )
        corner_info.setWordWrap(True)
        position_layout.addWidget(corner_info)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator2)
        
        # Font Settings
        font_group = QGroupBox("Font")
        font_layout = QVBoxLayout()
        
        # Font selection
        font_selection_layout = QHBoxLayout()
        font_label = QLabel("Font:")
        self.font_combo = QComboBox()
        
        # Find all fonts in the fonts folder
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        fonts_dir = os.path.join(addon_dir, "fonts")
        
        available_fonts = []
        if os.path.exists(fonts_dir):
            for file in os.listdir(fonts_dir):
                if file.endswith(('.ttf', '.otf')):
                    available_fonts.append(file)
        
        if not available_fonts:
            available_fonts = ["Minecraft.ttf"]  # Default
        
        self.font_combo.addItems(sorted(available_fonts))
        
        # Set current font if it exists in the list
        if self.font in available_fonts:
            self.font_combo.setCurrentText(self.font)
        elif available_fonts:
            self.font_combo.setCurrentIndex(0)
        
        font_selection_layout.addWidget(font_label)
        font_selection_layout.addWidget(self.font_combo)
        font_selection_layout.addStretch()
        font_layout.addLayout(font_selection_layout)
        
        # Add clickable link to open fonts folder
        font_folder_layout = QHBoxLayout()
        font_folder_link = QLabel(
            f'<a href="#" style="color: #2196f3;">Open fonts folder</a>'
        )
        font_folder_link.setTextFormat(Qt.TextFormat.RichText)
        font_folder_link.linkActivated.connect(lambda: openFolder(fonts_dir))
        font_folder_layout.addWidget(font_folder_link)
        font_folder_layout.addStretch()
        font_layout.addLayout(font_folder_layout)
        
        # Base font size selection
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("Base font size (fullscreen):")
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setMinimum(12)
        self.font_size_spinbox.setMaximum(200)
        self.font_size_spinbox.setValue(self.base_font_size)
        self.font_size_spinbox.setSuffix(" px")
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_spinbox)
        font_size_layout.addStretch()
        font_layout.addLayout(font_size_layout)
        
        font_info = QLabel(
            "<i>Place .ttf or .otf font files in the 'fonts' folder. "
            "Text size scales with window width based on the base size.</i>"
        )
        font_info.setWordWrap(True)
        font_layout.addWidget(font_info)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_config(self):
        """Save configuration"""
        config = mw.addonManager.getConfig(__name__)
        
        # Create new config if it doesn't exist
        if config is None:
            config = {}
        
        config["corner"] = self.corner_combo.currentText()
        config["show_counts"] = self.show_counts_checkbox.isChecked()
        config["show_animations"] = self.show_animations_checkbox.isChecked()
        config["underline_current_card"] = self.underline_checkbox.isChecked()
        config["font"] = self.font_combo.currentText()
        config["base_font_size"] = self.font_size_spinbox.value()
        
        mw.addonManager.writeConfig(__name__, config)
        
        tooltip("Configuration saved! Changes will apply to the next card.")
        self.accept()


def show_config_dialog():
    """Show the configuration dialog"""
    dialog = CardCountsConfigDialog(mw)
    dialog.exec()