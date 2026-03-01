"""
This screen allows users to create a new entry or edit an existing one by selecting a date.
It features a dropdown for date selection, dynamically generated fields based on the FIELDS list.
Validation ensures meaningful input before saving.
The screen tracks if the user is editing or not to determine the save action.
If the user is editing, it checks what changes were made to determine whether to use the PATCH or PUT API route.
"""

import datetime
from tkinter import Entry, Frame, Label, StringVar, Text
from tkinter import ttk

from domain.fields import FIELDS
from gui.screens.screen import Screen
from gui.screens.strategies.partial_update_strategy import PartialUpdateStrategy
from gui.screens.strategies.replace_strategy import ReplaceStrategy

# Module constant depends on an import
ENTRY_FIELDS = [field for field in FIELDS if field != "date"]


class NewEntryScreen(Screen):
    # Class constants to avoid hardcoding and allow easy updates
    TEXT_HEIGHT = 4
    MULTILINE_FIELDS = {"work_contribution", "learning"}
    CHARACTER_LIMIT = 2000

    def __init__(self, *args, client, on_home, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = client
        self._on_home = on_home
        self._text_widgets = {}

        # Track whether we're editing an existing entry (True) or creating a new one (False).
        # This determines which API route is used on save.
        self._editing = False
        self._original_data = None

        self._configure_grid()

        self._setup_title()
        self._setup_back_button()
        self._setup_date_frame()

        entry_data_frame = self._setup_entry_date_frame()
        self._setup_entry_data(entry_data_frame)

        self._setup_save_button()

    def _configure_grid(self):
        """Single column; header, date, fields, and save button stack vertically."""
        self._configure_responsive_grid(
            column_weights={0: 1, 1: 1},
            row_weights={0: 0, 1: 0, 2: 1, 3: 0}
        )

    def refresh_screen(self, event=None, date=None):
        """Reset the screen for the given date, defaulting to today if none is provided.

        Three possible use cases for this function:
        - No args (show_new_entry): default to today.
        - date= provided (edit from search screen): use that date.
        - event= provided (ComboboxSelected binding): tkinter has already updated
          _selected_date, so just read it without overwriting.
        """
        # Always reset editing state — the entry for the new date is checked fresh below
        self._editing = False
        self._original_data = None

        if date:
            self._selected_date.set(date)
        elif not event:
            # Called programmatically with no date — default to today
            self._selected_date.set(datetime.date.today().strftime("%Y-%m-%d"))
        # If event is not None, the dropdown already updated _selected_date

        selected_date = self._selected_date.get()
        try:
            entry = self._client.get_entry_by_date(selected_date)
            if entry:
                self._on_edit(entry.entry_dict)
            else:
                self.clear_fields()
        # If the error is a connection error, show it to the user.
        except ValueError as e:
            self._show_error("Server error", str(e))
            self.clear_fields()

    def _on_edit(self, original_data):
        """Set up the screen for editing an existing entry by prepopulating fields and tracking original data."""
        self._prepopulate_fields(original_data)
        self._editing = True
        self._original_data = original_data

    def clear_fields(self):
        """Clear all entry field widgets, resetting them to empty."""
        for widget in self._text_widgets.values():
            if isinstance(widget, Text):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")

    def _setup_title(self):
        """Create the title label"""
        self.title_label = Label(
            self, text="NEW ENTRY",
            font=self.heading_font,
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR,
            anchor="w",
        )
        self.title_label.grid(
            row=0, column=0, padx=(self.OUTER_PADDING, 10),
            pady=(20, 10), sticky="w"
        )

    def _setup_back_button(self):
        """Create the back button and position it in the top-right corner."""
        back_btn = self._create_stylised_button(
            parent=self, func=self._on_home,
            title="❌ Cancel", subtitle="Return to home screen"
        )
        self._position_button(
            back_btn, row=0, column=1, column_span=1,
            pad_x=(10, self.OUTER_PADDING), pad_y=(20, 10), sticky="e"
        )

    def _setup_date_frame(self):
        """Create a centred date label and dropdown for selecting the entry date."""
        date_frame = Frame(self, bg=self.PRIMARY_COLOR)
        date_frame.grid(
            row=1, column=0, columnspan=2,
            padx=self.OUTER_PADDING, pady=(0, 10), sticky="ew"
        )
        date_frame.grid_columnconfigure(0, weight=1)

        Label(
            date_frame, text="Date",
            font=self.subheading_font,
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR,
        ).grid(row=0, column=0, pady=(0, 4))

        self._setup_date_dropdown(date_frame)

    def _setup_date_dropdown(self, parent):
        """Create a dropdown with options for today and the past year, defaulting to today."""
        # Store options for today up to the past year in YYYY-MM-DD format
        today = datetime.date.today()
        dates = [
            (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(365)
        ]

        # Combobox requires StringVar to track selected value; default to today's date and use readonly to prevent invalid input
        self._selected_date = StringVar(value=dates[0])
        date_dropdown = ttk.Combobox(
            parent, textvariable=self._selected_date,
            values=dates, state="readonly", width=20
        )
        date_dropdown.grid(row=1, column=0)
        date_dropdown.bind("<<ComboboxSelected>>", self.refresh_screen)

    def _setup_entry_date_frame(self):
        """Bordered outer frame containing an inner frame with labelled entry fields."""
        self.outer_frame = self._create_frame(row=2, column_span=2)

        inner_frame = self._create_inner_frame(self.outer_frame)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=3)

        return inner_frame

    def _setup_entry_data(self, parent):
        for i, field in enumerate(ENTRY_FIELDS):
            parent.grid_rowconfigure(i, weight=1)
            is_multiline = field in self.MULTILINE_FIELDS

            # Labels next to a tall Text widget are pinned to the top-left with
            # matching top padding so they align with the first line of text.
            # Labels next to a single-line Entry are truly vertically centred with sticky="w".
            label_sticky = "nw" if is_multiline else "w"
            label_pad_y = (14, 10) if is_multiline else 10

            Label(
                parent,
                text=field.upper().replace("_", " ") + ":",
                font=self.subheading_font,
                bg="white",
                anchor="w",
            ).grid(row=i, column=0, padx=(20, 10), pady=label_pad_y, sticky=label_sticky)

            widget = self._create_text_widget(parent=parent, multiline=is_multiline)
            widget.grid(row=i, column=1, padx=(0, 20), pady=10, sticky="ew")

            self._text_widgets[field] = widget

    def _create_text_widget(self, parent, multiline=False):
        """Helper function to create either a Text or Entry widget based on the multiline parameter."""
        if multiline:
            return Text(
                parent,
                height=self.TEXT_HEIGHT,
                font=self.italic_font,
                relief="solid",
                borderwidth=1,
                wrap="word",
            )
        else:
            return Entry(
                parent,
                font=self.italic_font,
                relief="solid",
                borderwidth=1,
            )

    def _setup_save_button(self):
        """Save button centred at the bottom with a fixed width."""
        container = Frame(self, bg=self.PRIMARY_COLOR)
        container.grid(row=3, column=0, columnspan=2, pady=(10, 60))

        save_btn = self._create_stylised_button(
            parent=container,
            title="✔️ Save",
            subtitle="Save entry & return to Home",
            func=self._on_save
        )
        save_btn.grid(padx=self.OUTER_PADDING)

    def _input_is_valid(self, raw_data):
        """Validate that at least one field is filled and no fields exceed character limits before allowing save."""
        valid = True
        if not raw_data or not any(raw_data[field] for field in ENTRY_FIELDS):
            self._show_error("No input detected", "Please fill in at least one field before saving.")
            valid = False

        for field, value in raw_data.items():
            if len(value) > self.CHARACTER_LIMIT:
                self._show_error(f"Input for {field.replace('_', ' ')} too long",
                                 "Please limit each field to 2000 characters.")
                valid = False

        return valid

    @staticmethod
    def _get_stripped_data(raw_data):
        """Strip leading/trailing whitespace from all field values before saving."""
        filtered_data = {
            field: value.strip() for field, value in raw_data.items()
        }
        return filtered_data

    def _on_save(self):
        """Collect field values and submit via the save callback."""
        new_data = self.get_entry_data()
        if self._input_is_valid(new_data):

            if self._editing and self._original_data:
                if self._is_update_required(new_data):
                    self._determine_update_route(new_data)
            else:
                filtered_data = self._get_stripped_data(new_data)
                self._client.save_entry(filtered_data)

            self._editing = False
            self._original_data = None
            self._on_home()

    def _determine_update_route(self, new_data):
        """Determine whether to use full replace (PUT) or partial update (PATCH) API route based on changed fields."""
        filtered_data = self._get_stripped_data(new_data)

        # If all values are changed, use PUT (full replace), otherwise use PATCH (partial update)
        all_values_changed = all(
            self._original_data.get(field) != value
            for field, value in new_data.items()
            if field != "date"
        )

        if all_values_changed:
            strategy = ReplaceStrategy()
        else:
            strategy = PartialUpdateStrategy()
            # Only send changed fields to the API for a PATCH request
            filtered_data = {
                field: value
                for field, value in filtered_data.items()
                if self._original_data.get(field) != value or field == "date"
            }
        strategy.update(self._client, filtered_data)


    def _is_update_required(self, new_data):
        """Check if any fields have changed compared to the original data"""
        for field, value in new_data.items():
            if self._original_data.get(field) != value:
                return True
        return False

    def _prepopulate_fields(self, saved_data):
        """Pre-fill fields with saved data for editing."""
        self._selected_date.set(saved_data.get("date"))
        for field, widget in self._text_widgets.items():
            value = saved_data.get(field, "")
            if isinstance(widget, Text):
                widget.delete("1.0", "end")
                widget.insert("1.0", value)
            else:
                widget.delete(0, "end")
                widget.insert(0, value)

    def get_entry_data(self):
        """Return a dict of the current date and its field values."""
        # Use get() to extract string value from StringVar
        data = {"date": self._selected_date.get()}
        for field, widget in self._text_widgets.items():
            if isinstance(widget, Text):
                # Use get() to extract text content from Text widget
                # Start from line 1, character 0
                # End at the end minus 1 character to exclude trailing newline added by Text widget
                data[field] = widget.get("1.0", "end-1c").strip()
            else:
                # Use get() to extract string value from Entry widget
                data[field] = widget.get().strip()
        return data
