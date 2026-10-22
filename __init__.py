from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.theme import theme_manager
import os

# Import config dialog
try:
    from .config_dialog import show_config_dialog
except ImportError:
    try:
        from config_dialog import show_config_dialog
    except ImportError:
        show_config_dialog = None

class AnimatedChangeLabel(QLabel):
    """Label that shows animated +1/-1 changes"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Animation setup
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1500)  # 1.5 seconds
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.finished.connect(self.hide)
        
        self.hide()
    
    def show_change(self, text, color, font_family, font_size):
        """Show an animated change indicator"""
        self.setText(
            f'<span style="color: {color}; font-family: {font_family}; font-size: {font_size}px; font-weight: bold;">{text}</span>'
        )
        self.adjustSize()
        self.opacity_effect.setOpacity(1.0)
        self.show()
        self.fade_animation.start()

class CardCountsPopup(QWidget):
    def __init__(self):
        super().__init__(mw)
        self.config = mw.addonManager.getConfig(__name__) or {}
        
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(4)
        self.setLayout(self.layout)
        
        # Create container for labels with animations
        self.new_container = QWidget()
        self.new_container_layout = QHBoxLayout()
        self.new_container_layout.setContentsMargins(0, 0, 0, 0)
        self.new_container.setLayout(self.new_container_layout)
        
        self.learning_container = QWidget()
        self.learning_container_layout = QHBoxLayout()
        self.learning_container_layout.setContentsMargins(0, 0, 0, 0)
        self.learning_container.setLayout(self.learning_container_layout)
        
        self.review_container = QWidget()
        self.review_container_layout = QHBoxLayout()
        self.review_container_layout.setContentsMargins(0, 0, 0, 0)
        self.review_container.setLayout(self.review_container_layout)
        
        # Create labels for each count type
        self.new_label = QLabel()
        self.learning_label = QLabel()
        self.review_label = QLabel()
        
        for label in [self.new_label, self.learning_label, self.review_label]:
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create animated change labels
        self.new_change = AnimatedChangeLabel()
        self.learning_change = AnimatedChangeLabel()
        self.review_change = AnimatedChangeLabel()
        
        # Add labels and changes to containers
        self.new_container_layout.addWidget(self.new_label)
        self.new_container_layout.addWidget(self.new_change)
        self.new_container_layout.addStretch()
        
        self.learning_container_layout.addWidget(self.learning_label)
        self.learning_container_layout.addWidget(self.learning_change)
        self.learning_container_layout.addStretch()
        
        self.review_container_layout.addWidget(self.review_label)
        self.review_container_layout.addWidget(self.review_change)
        self.review_container_layout.addStretch()
        
        # Add containers to main layout
        self.layout.addWidget(self.new_container)
        self.layout.addWidget(self.learning_container)
        self.layout.addWidget(self.review_container)
        
        # Store previous counts for comparison
        self.prev_counts = None
        
        self.update_styling()
        
    def update_styling(self):
        # Get main window geometry for scaling
        mw_geo = mw.geometry()
        screen_geo = QApplication.primaryScreen().geometry()
        is_small = mw_geo.width() <= screen_geo.width() * 0.5
        
        # Get base font size from config (default 48)
        base_size = self.config.get("base_font_size", 48)
        
        # Scale font size based on window width
        width_ratio = mw_geo.width() / screen_geo.width()
        font_size = int(base_size * min(width_ratio * 1.5, 1.0))
        
        # Adjust opacity based on window size
        if is_small:
            opacity = 0.3  # Very translucent when small
        else:
            opacity = 0.85
        
        # Get font from config
        font_name = self.config.get("font", "Minecraft.ttf")
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(addon_dir, "fonts", font_name)
        
        # Load custom font if it exists
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    font_family = font_families[0]
                else:
                    font_family = "Arial"
            else:
                font_family = "Arial"
        else:
            font_family = "Arial"
        
        # Transparent widget background
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Make containers transparent too
        for container in [self.new_container, self.learning_container, self.review_container]:
            container.setStyleSheet("background-color: transparent; border: none;")
        
        # Store colors and styling info
        self.font_size = font_size
        self.opacity = opacity
        self.font_family = font_family
    
    def current_card_index(self):
        """Which count the current card belongs to: 0 = new, 1 = learning, 2 = review, None = unknown"""
        card = mw.reviewer.card if mw.reviewer else None
        if not card:
            return None
        if card.queue == 0:
            return 0
        if card.queue in (1, 3, 4):  # learning, interday learning, preview
            return 1
        if card.queue == 2:
            return 2
        return None
    
    def styled_count(self, count, color, underline):
        """Build the rich-text span for one count, optionally underlined"""
        decoration = "underline" if underline else "none"
        return (
            f'<span style="color: {color}; font-family: {self.font_family}; '
            f'font-size: {self.font_size}px; font-weight: bold; '
            f'text-decoration: {decoration};">{count}</span>'
        )
        
    def update_counts(self, show_animations=True):
        # Re-read config so changes from the config dialog apply to the next card
        self.config = mw.addonManager.getConfig(__name__) or self.config
        
        if not mw.reviewer or not mw.reviewer.card:
            self.hide()
            return
        
        # Check if counts should be displayed (Anki setting)
        if not self.config.get("show_counts", True):
            self.hide()
            return
        
        # Get remaining counts from the reviewer
        counts = mw.reviewer.mw.col.sched.counts()
        new_count = counts[0]
        learning_count = counts[1]
        review_count = counts[2]
        
        # Update styling in case window size or config changed
        self.update_styling()
        
        # Show animations if enabled and we have previous counts
        if show_animations and self.prev_counts is not None and self.config.get("show_animations", True):
            prev_new, prev_learning, prev_review = self.prev_counts
            
            # Check for changes and show animations
            # Use white for decreases (progress) and red for increases (setbacks)
            if new_count < prev_new:
                # New card answered - show white -1 (progress)
                self.new_change.show_change(
                    "-1", "rgba(255, 255, 255, 1.0)",
                    self.font_family, self.font_size
                )
            
            if learning_count > prev_learning:
                # Card moved to learning (setback) - show angry red +1
                self.learning_change.show_change(
                    "+1", "rgba(255, 50, 50, 1.0)",
                    self.font_family, self.font_size
                )
            elif learning_count < prev_learning:
                # Learning card graduated (progress) - show white -1
                self.learning_change.show_change(
                    "-1", "rgba(255, 255, 255, 1.0)",
                    self.font_family, self.font_size
                )
            
            if review_count < prev_review:
                # Review card answered (progress) - show white -1
                self.review_change.show_change(
                    "-1", "rgba(255, 255, 255, 1.0)",
                    self.font_family, self.font_size
                )
        
        # Store current counts for next comparison
        self.prev_counts = (new_count, learning_count, review_count)
        
        # Colors: blue for new, red for learning, green for review
        new_color = "#2196f3"
        learning_color = "#ff8589"
        review_color = "#7cb342"
        
        # Apply opacity to colors
        new_rgba = self.hex_to_rgba(new_color, self.opacity)
        learning_rgba = self.hex_to_rgba(learning_color, self.opacity)
        review_rgba = self.hex_to_rgba(review_color, self.opacity)
        
        # Underline the count matching the current card (if enabled)
        if self.config.get("underline_current_card", True):
            current = self.current_card_index()
        else:
            current = None
        
        # Create styled text
        self.new_label.setText(self.styled_count(new_count, new_rgba, current == 0))
        self.learning_label.setText(self.styled_count(learning_count, learning_rgba, current == 1))
        self.review_label.setText(self.styled_count(review_count, review_rgba, current == 2))
        
        self.adjustSize()
        self.position_popup()
        self.show()
    
    def hex_to_rgba(self, hex_color, opacity):
        """Convert hex color to rgba with opacity"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {opacity})"
    
    def position_popup(self):
        if not mw.reviewer or not mw.reviewer.web:
            return
        
        corner = self.config.get("corner", "top-left")
        
        # Get main window geometry
        mw_geo = mw.geometry()
        
        popup_width = self.width()
        popup_height = self.height()
        
        reviewer_y_offset = 70
        
        # Try to detect if card history popup exists and get its position
        history_offset = 0
        try:
            # Look for the card history killfeed popup
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QWidget) and widget != self and widget.isVisible():
                    if hasattr(widget, 'text_label'):  # Card history popup has text_label
                        history_geo = widget.geometry()
                        # Check if on same side
                        history_on_left = history_geo.x() < mw_geo.x() + mw_geo.width() / 2
                        popup_on_left = corner in ["top-left", "bottom-left"]
                        
                        if history_on_left == popup_on_left and corner.startswith("top"):
                            history_offset = history_geo.height() + 10
                        break
        except:
            pass
        
        # Always position in corner - never center
        if corner == "top-left":
            x = mw_geo.x() + 10
            y = mw_geo.y() + reviewer_y_offset + history_offset
        elif corner == "top-right":
            x = mw_geo.x() + mw_geo.width() - popup_width - 10
            y = mw_geo.y() + reviewer_y_offset + history_offset
        elif corner == "bottom-left":
            x = mw_geo.x() + 10
            y = mw_geo.y() + mw_geo.height() - popup_height - 50
        else:  # bottom-right
            x = mw_geo.x() + mw_geo.width() - popup_width - 10
            y = mw_geo.y() + mw_geo.height() - popup_height - 50
        
        self.move(x, y)

# Global popup instance
popup = None

def on_reviewer_did_show_question(card):
    global popup
    if popup is None:
        popup = CardCountsPopup()
        # First card - don't show animations
        popup.update_counts(show_animations=False)
    else:
        popup.update_styling()
        # Subsequent cards - show animations
        popup.update_counts(show_animations=True)
    popup.position_popup()

def on_reviewer_will_end():
    global popup
    if popup:
        popup.hide()
        # Reset previous counts when ending review session
        popup.prev_counts = None

# Setup hooks
gui_hooks.reviewer_did_show_question.append(on_reviewer_did_show_question)
gui_hooks.reviewer_did_show_answer.append(on_reviewer_did_show_question)
gui_hooks.reviewer_will_end.append(on_reviewer_will_end)

# Cleanup on profile unload
def cleanup():
    global popup
    if popup:
        popup.close()
        popup = None

gui_hooks.profile_will_close.append(cleanup)

# Add menu item for configuration
def setup_menu():
    if show_config_dialog:
        action = QAction("Card Counts Display Config...", mw)
        action.triggered.connect(show_config_dialog)
        mw.form.menuTools.addAction(action)

gui_hooks.main_window_did_init.append(setup_menu)