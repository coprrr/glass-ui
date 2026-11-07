"""Native, keyboard-accessible configuration dialog for Glass UI."""
from aqt.qt import (
    QButtonGroup, QCheckBox, QColor, QColorDialog, QDialog, QDialogButtonBox, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QRadioButton, QScrollArea,
    QSlider, Qt, QVBoxLayout, QWidget,
)


class GlassSettings(QDialog):
    def __init__(self, parent, module, config, defaults, apply_settings):
        super().__init__(parent)
        self.host, self.module = parent, module
        self.apply_settings = apply_settings
        self.original, self.defaults = dict(config), dict(defaults)
        self.groups, self.sliders = {}, {}
        self.colors = {}
        self.setWindowTitle('Glass UI Settings')
        self.resize(620, 720)
        root = QVBoxLayout(self)
        title = QLabel('Glass UI Settings · v1.0')
        title.setStyleSheet('font-size: 20px; font-weight: 600;')
        root.addWidget(title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.form = QVBoxLayout(content)
        self.form.setSpacing(16)
        scroll.setWidget(content)
        root.addWidget(scroll)
        self.enabled = QCheckBox('Enable Glass UI')
        self.form.addWidget(self.enabled)
        self.status = QLabel()
        self.status.setWordWrap(True)
        self.form.addWidget(self.status)
        self.enabled.toggled.connect(self.update_status)
        self.choices('appearance', 'Appearance', [
            ('Dark glass (default)', 'dark'), ('Light glass', 'light'),
            ('Match Anki appearance', 'system')], vertical=True)
        self.slider('panel_opacity', 'Panel opacity', 15, 100, '%', scale=100)
        self.slider('blur_px', 'Background blur', 0, 40, 'px')
        self.slider('corner_radius_px', 'Corner radius', 0, 40, 'px')
        self.color_control('accent_color', 'Accent colour')
        self.color_control('highlight_color', 'Deck highlight')
        self.color_control('highlight_text_color', 'Highlighted deck text')
        self.color_control('text_color', 'Normal text — dark glass')
        self.color_control('light_text_color', 'Normal text — light glass')
        self.slider('font_size_px', 'Interface text size', 12, 28, 'px')
        self.slider('panel_max_width_px', 'Maximum panel width', 400, 1800, 'px')
        self.slider('row_padding_px', 'Row spacing', 0, 14, 'px')
        self.slider('overview_width_px', 'Overview panel width', 400, 1400, 'px')
        self.slider('overview_padding_px', 'Overview panel padding', 8, 48, 'px')
        self.slider('study_button_padding_px', 'Study Now button padding', 4, 20, 'px')
        note = QLabel('Apply updates Anki immediately. Save applies and closes. '
                      'Background images are managed by your background add-on.')
        note.setWordWrap(True)
        self.form.addWidget(note)
        self.form.addStretch()
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save |
                                   QDialogButtonBox.StandardButton.Cancel)
        apply_button = buttons.addButton(QDialogButtonBox.StandardButton.Apply)
        apply_button.clicked.connect(lambda: self.save(close=False))
        reset = QPushButton('Restore defaults')
        buttons.addButton(reset, QDialogButtonBox.ButtonRole.ResetRole)
        reset.clicked.connect(lambda: self.load(self.defaults))
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)
        self.load(config)
        self.update_status()

    def update_status(self):
        self.status.setText('Styling enabled. Click Apply to see your changes.'
                            if self.enabled.isChecked() else
                            'Styling disabled. Enable Glass UI to use these settings; '
                            'Apply will remove Glass UI styling while disabled.')

    def color_control(self, key, title):
        row = QHBoxLayout()
        row.addWidget(QLabel(title))
        row.addStretch()
        button = QPushButton()
        button.setAccessibleName(title)
        button.clicked.connect(lambda: self.pick_color(key, title))
        row.addWidget(button)
        self.form.addLayout(row)
        self.colors[key] = button

    def set_color(self, key, value):
        color = QColor(str(value))
        if not color.isValid():
            color = QColor(self.defaults[key])
        button = self.colors[key]
        button.setText(color.name())
        # Choose a readable label for the colour swatch itself.
        foreground = '#111111' if color.lightnessF() > 0.55 else '#ffffff'
        button.setStyleSheet(f'background-color: {color.name()}; color: {foreground}; padding: 6px 16px;')

    def pick_color(self, key, title):
        color = QColorDialog.getColor(QColor(self.colors[key].text()), self, title)
        if color.isValid():
            self.set_color(key, color.name())

    def choices(self, key, title, choices, vertical=False):
        box = QGroupBox(title)
        layout = QVBoxLayout(box) if vertical else QHBoxLayout(box)
        group = QButtonGroup(self)
        values = []
        for label, value in choices:
            button = QRadioButton(label)
            group.addButton(button)
            layout.addWidget(button)
            values.append((button, value))
        self.groups[key] = (group, values)
        self.form.addWidget(box)

    def slider(self, key, title, low, high, suffix, scale=1):
        layout = QVBoxLayout()
        heading = QHBoxLayout()
        label, value = QLabel(title), QLabel()
        heading.addWidget(label)
        heading.addStretch()
        heading.addWidget(value)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(low, high)
        slider.setAccessibleName(title)
        label.setBuddy(slider)
        slider.valueChanged.connect(lambda n: value.setText(f'{n}{suffix}'))
        layout.addLayout(heading)
        layout.addWidget(slider)
        self.form.addLayout(layout)
        self.sliders[key] = (slider, scale)
        # Set text even when the initial slider value is zero.
        value.setText(f'{slider.value()}{suffix}')

    def load(self, config):
        for key in self.colors:
            self.set_color(key, config.get(key, self.defaults[key]))
        self.enabled.setChecked(bool(config.get('enabled', True)))
        for key, (_, choices) in self.groups.items():
            selected = config.get(key, self.defaults.get(key))
            button = next((b for b, v in choices if v == selected), choices[0][0])
            button.setChecked(True)
        for key, (slider, scale) in self.sliders.items():
            try:
                number = round(float(config.get(key, self.defaults[key])) * scale)
            except (TypeError, ValueError, OverflowError):
                number = round(self.defaults[key] * scale)
            slider.setValue(max(slider.minimum(), min(slider.maximum(), number)))

    def save(self, close=True):
        # Preserve advanced settings and unknown keys during normal edits.
        config = dict(self.original)
        config.pop('font_family', None)
        config['enabled'] = self.enabled.isChecked()
        for key, button in self.colors.items():
            config[key] = button.text()
        for key, (_, choices) in self.groups.items():
            config[key] = next(v for b, v in choices if b.isChecked())
        for key, (slider, scale) in self.sliders.items():
            config[key] = slider.value() / scale if scale != 1 else slider.value()
        self.host.addonManager.writeConfig(self.module, config)
        self.apply_settings()
        self.status.setText('Applied to Anki.' if config['enabled'] else 'Applied: Glass UI is disabled.')
        if close:
            self.accept()
