# Card Counts Display
A customizable overlay that displays remaining new, learning, and review card counts during Anki review sessions with animated feedback.

## Use Case
I've heard that it's best to turn off the remaining card display, so you don't stare at it and stay unmotivated during your painfully long review sessions. This addon is the opposite of that principle, making the remaining cards huge and obvious; hopefully this will prove the common META wrong and actually motivate you as you study.

## What It Shows
Large, color-coded numbers showing:
- **New cards** (blue)
- **Learning cards** (red)
- **Review cards** (green)

### Animated Feedback
When enabled, shows fading +1/-1 indicators:
- **White -1**: Progress (cards completed)
- **Red +1**: Setbacks (cards added to learning queue)

## Configuration
Access via **Tools → Card Counts Display Config...**

### Display Settings
- **Show card counts during reviews**: Toggle the entire display on/off
- **Show animated +1/-1 change indicators**: Enable/disable the animated feedback

- **Underline the count of the current card's type**: Underlines the blue/red/green number matching the card on screen (new/learning/review)

### Position
- **Corner position**: Choose where the counts appear (top-left, top-right, bottom-left, bottom-right)
  - Defaults to top-left to avoid Card History Killfeed
  - Automatically stacks below Card History Killfeed if both are on the same side

### Font Settings
- **Font**: Select from .ttf or .otf fonts in the addon's 'fonts' folder
  - Click "Open fonts folder" link to add custom fonts
- **Base font size (fullscreen)**: Set the font size when window is fullscreen (12-200px, default 48px)
  - Text automatically scales down as window width decreases
  - Opacity increases dramatically when window is ≤50% of screen width, to avoid covering your cards.

## Changelog

  ### Version 1.0.0
- Initial release

### Version 1.1.0
- Added underline for state of current card in reviewer