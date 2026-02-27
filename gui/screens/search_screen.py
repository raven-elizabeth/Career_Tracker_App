# This screen allows users to select a date from a calendar and view the corresponding entry if one exists.
# It also provides options to edit or delete the entry, with a confirmation dialog for deletions.
# The layout adapts responsively to different window sizes, switching between adjacent and wrap layouts as needed.

import datetime
from tkinter import Frame, messagebox

from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    WRAP_LAYOUT_WIDTH = 1000
    INNER_PADDING = 20

    def __init__(self, *args, on_date, on_home, on_edit, on_delete, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_date = on_date
        self._on_home = on_home
        self._on_edit = on_edit
        self._on_delete = on_delete

        self._wrap_layout = False
        self._current_entry = None

        self._configure_adjacent_grid()

        self._setup_back_button()
        self._setup_calendar()
        self._setup_display_frame()

        self.bind("<Configure>", self._on_resize)

    def refresh_display(self):
        """
        Refresh the display frame based on the currently selected calendar date.
        Fetch and display entry for the selected date, or show default message if no entry exists.
        Unused event parameter is required by the binding but not needed for the logic, so it's ignored
        """
        selected_date = self.calendar.get_date()
        date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
        entry = self._on_date(date)
        if entry:
            self._on_valid_date(entry)
        else:
            self._reset_display_frame(default=True)

    def _on_resize(self, event):
        """Switch between adjacent and wrap layouts based on window width."""
        if event.widget != self:
            return

        should_wrap = event.width < self.WRAP_LAYOUT_WIDTH

        if should_wrap and not self._wrap_layout:
            self._apply_wrap_layout()
            self._wrap_layout = True
        elif not should_wrap and self._wrap_layout:
            self._apply_adjacent_layout()
            self._wrap_layout = False

    def _configure_adjacent_grid(self):
        """Two equal columns; calendar and display frame share the main row."""
        self._configure_responsive_grid(
            column_weights={0: 1, 1: 1},
            row_weights={0: 0, 1: 1, 2: 10, 3: 1}
        )

    def _configure_wrap_grid(self):
        """Single column; calendar and display frame stack vertically."""
        self._configure_responsive_grid(
            column_weights={0: 1, 1: 1},
            row_weights={0: 0, 1: 1, 2: 0, 3: 10, 4: 1}
        )

    def _apply_adjacent_layout(self):
        """Grid and position calendar and display frame side by side in the main row."""
        self._configure_adjacent_grid()
        self._position_calendar(row=2, colspan=1)
        self._position_frame(
            self.display_frame, row=2, column=1, colspan=1,
            pad_x=(self.INNER_PADDING, self.OUTER_PADDING)
        )

    def _apply_wrap_layout(self):
        """Grid and position calendar above the display frame, both spanning full width."""
        self._configure_wrap_grid()
        self._position_calendar(row=2, colspan=2)
        self._position_frame(
            self.display_frame, row=3, column=0,
            pad_x=self.INNER_PADDING,
            pad_y=(self.INNER_PADDING, self.OUTER_PADDING)
        )

    def _setup_back_button(self):
        back_button = self._create_stylised_button(
            parent=self,
            title="⬅️ Back",
            subtitle="Return to home screen",
            func=self._on_home,
        )
        self._position_button(
            back_button,
            row=0, colspan=2, pad_y=(20, 10), sticky="w"
        )

    def _setup_calendar(self):
        """Create calendar widget with max date of today and bind date selection event."""
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self._position_calendar(row=2, colspan=1)
        self.calendar.bind("<<CalendarSelected>>", self.refresh_display())

    def _position_calendar(self, row, colspan):
        """Grid the calendar with consistent padding."""
        pad_x = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 1 else self.INNER_PADDING
        pad_y = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 2 else self.OUTER_PADDING
        self.calendar.grid(
            row=row, column=0, columnspan=colspan,
            padx=pad_x, pady=pad_y, sticky="nsew"
        )

    def _setup_display_frame(self):
        """Create the display frame with an inner frame for content"""
        self.display_frame = self._create_frame(row=2, column=1, colspan=1)
        self._position_frame(
            self.display_frame, row=2, column=1, colspan=1,
            pad_x=(self.INNER_PADDING, self.OUTER_PADDING)
        )
        # Prevent outer frame from resizing to fit content from entry data
        self.display_frame.grid_propagate(False)

        self.inner_frame = self._setup_inner_frame(self.display_frame)

        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )
        self.default_msg.grid_configure(columnspan=2)

        self._action_buttons = self._create_action_buttons()
        # Hidden until an entry is displayed
        self._action_buttons.grid_remove()

    def _setup_inner_frame(self, parent):
        """Create an inner frame within the display frame to hold entry details and action buttons,
        with spacers for centering."""
        inner_frame = self._create_inner_frame(parent)

        # Prevent inner frame from resizing to fit content from entry data
        self.inner_frame.grid_propagate(False)

        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_rowconfigure(0, weight=1)  # Top spacer
        self.inner_frame.grid_rowconfigure(2, weight=1)  # Bottom spacer

        return inner_frame

    def _on_valid_date(self, entry):
        """Display the entry details and show action buttons for editing or deleting the entry."""
        self._reset_display_frame(default=False)
        self._current_entry = entry
        self._display_entry(entry)
        self._display_entry_action_buttons(entry)

    def _reset_widgets(self):
        """Clear the display frame and reset to default state, optionally showing the default message."""
        widgets = self.inner_frame.winfo_children()
        widgets.remove(self.default_msg)
        widgets.remove(self._action_buttons)
        for widget in widgets:
            widget.destroy()

    def _reset_inner_frame(self):
        """Clear the inner frame of all entry details and action buttons, and reset any layout bindings."""
        # Remove per-entry wraplength bindings added in _display_entry
        self.inner_frame.unbind("<Configure>")

        # Reset the spacer rows used by default message centering
        self.inner_frame.grid_rowconfigure(0, weight=0)
        self.inner_frame.grid_rowconfigure(2, weight=0)
        # Reset the trailing spacer row added after entry labels
        self.inner_frame.grid_rowconfigure(len(self.inner_frame.grid_slaves()), weight=0)

    def _reset_display_frame(self, default=False):
        """Clear the display frame and reset to default state, optionally showing the default message."""
        self._reset_widgets()
        self._reset_inner_frame()

        # Always hide action buttons until an entry is displayed
        self._action_buttons.grid_remove()

        # Show default message if default=True, otherwise hide it
        if not default:
            self.default_msg.grid_remove()
        else:
            self._current_entry = None
            # Restore spacer rows for centered default message
            self.inner_frame.grid_rowconfigure(0, weight=1)
            self.inner_frame.grid_rowconfigure(2, weight=1)
            self.default_msg.grid(row=1, padx=10, pady=10)

    def _display_entry(self, entry):
        """Create labels for each field in the entry and display them in the inner frame, with action buttons below."""
        for row, (field, value) in enumerate(entry.entry_dict.items()):
            label = self._create_label(
                self.inner_frame, row=row + 1,
                text=f"{field.replace('_', ' ').title()}: {value.capitalize() if value else 'N/A'}",
                font=self.subheading_font, bg="white",
                anchor="w", pad_y=5
            )
            label.grid_configure(columnspan=2)
            self.inner_frame.bind(
                "<Configure>",
                lambda event, lbl=label: lbl.config(wraplength=event.width - 20),
                add="+"
            )

    def _display_entry_action_buttons(self, entry):
        """Grid the Edit and Delete buttons below the entry details, centred and with consistent padding."""
        self._action_buttons.grid(
            row=len(entry.entry_dict) + 1, column=0, columnspan=2,
            padx=40, pady=(20, 10), sticky="ew"
        )

    def _create_action_buttons(self):
        """Create Edit and Delete stylised buttons of equal size, centred in the inner frame."""
        btn_frame = Frame(self.inner_frame, bg="white")
        btn_frame.grid_columnconfigure(0, weight=1, uniform="btn")
        btn_frame.grid_columnconfigure(1, weight=1, uniform="btn")

        edit_btn = self._create_stylised_button(
            parent=btn_frame,
            title="✏️ Edit",
            subtitle="Edit this entry",
            func=lambda: self._on_edit(self._current_entry.entry_dict)
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        delete_btn = self._create_stylised_button(
            parent=btn_frame,
            title="❌ Delete",
            subtitle="Delete this entry",
            func=self._show_delete_confirmation
        )
        delete_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        return btn_frame

    def _show_delete_confirmation(self):
        """Show a confirmation dialog before deleting an entry."""
        if self._current_entry:
            date = self._current_entry.entry_dict.get("date")
            confirm = messagebox.askyesno(
                title="Confirm delete",
                message=f"Are you sure you want to delete the entry for {date}?"
            )
            if confirm:
                self._delete_entry(self._current_entry.entry_dict.get("date"))

    def _delete_entry(self, date):
        """Delete the entry for the given date and reset the display."""
        self._on_delete(date)
        self._reset_display_frame(default=True)
