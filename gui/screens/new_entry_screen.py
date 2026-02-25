import datetime
from tkinter import Entry, Frame, Label, StringVar, Text, Toplevel
from tkinter import ttk

from domain.fields import FIELDS
from gui.screens.screen import Screen

ENTRY_FIELDS = [field for field in FIELDS if field != "date"]
MULTILINE_FIELDS = {"work_contribution", "learning"}


class NewEntryScreen(Screen):
    TEXT_HEIGHT = 4

    def __init__(self, *args, on_home, on_valid_save, on_date, on_full_replace, on_partial_update, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_home = on_home
        self._on_valid_save = on_valid_save
        self._on_date = on_date
        self._on_full_replace = on_full_replace
        self._on_partial_update = on_partial_update
        self._text_widgets = {}

        # Track whether we're currently editing an existing entry (True) or creating a new one (False) to determine post-save behaviour
        self._editing = False
        self._original_data = None

        self._configure_grid()
        self._create_header_row()
        self._create_date_dropdown()
        self._create_fields_frame()
        self._create_save_button()

        today = datetime.date.today().strftime("%Y-%m-%d")
        entry = self._on_date(today)
        if entry:
            self._on_edit(entry.entry_dict)

    def _configure_grid(self):
        """Single column; header, date, fields, and save button stack vertically."""
        self._configure_responsive_grid(
            col_dict={0: 1, 1: 1},
            row_dict={0: 0, 1: 0, 2: 1, 3: 0}
        )

    def _create_header_row(self):
        """Title label on the left, back button on the right."""
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

        back_btn = self._add_back_button(func=self._on_home)
        self._position_button(
            back_btn, row=0, column=1, colspan=1,
            pad_x=(10, self.OUTER_PADDING), pad_y=(20, 10), sticky="e"
        )

    def _create_date_dropdown(self):
        """Centred date dropdown spanning both columns."""
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

        # Store options for today up to the past year in YYYY-MM-DD format
        today = datetime.date.today()
        dates = [
            (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(365)
        ]

        # Combobox requires StringVar to track selected value; default to today's date and use readonly to prevent invalid input
        self._selected_date = StringVar(value=dates[0])
        date_dropdown = ttk.Combobox(
            date_frame, textvariable=self._selected_date,
            values=dates, state="readonly", width=20
        )
        date_dropdown.grid(row=1, column=0)
        date_dropdown.bind("<<ComboboxSelected>>", self._on_date_selected)

    def _create_fields_frame(self):
        """Light-blue bordered outer frame containing a white inner frame with labelled entry fields."""
        self.fields_frame = self._create_frame(row=2, column=0, colspan=2)

        inner = self._create_inner_frame(self.fields_frame)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=3)

        for i, field in enumerate(ENTRY_FIELDS):
            inner.grid_rowconfigure(i, weight=1)
            is_multiline = field in MULTILINE_FIELDS

            # Labels next to a tall Text widget are pinned to the top-left with
            # matching top padding so they align with the first line of text.
            # Labels next to a single-line Entry are truly vertically centred with sticky="w".
            label_sticky = "nw" if is_multiline else "w"
            label_pady = (14, 10) if is_multiline else 10

            Label(
                inner,
                text=field.upper().replace("_", " ") + ":",
                font=self.subheading_font,
                bg="white",
                anchor="w",
            ).grid(row=i, column=0, padx=(20, 10), pady=label_pady, sticky=label_sticky)

            if is_multiline:
                widget = Text(
                    inner,
                    height=self.TEXT_HEIGHT,
                    font=self.italic_font,
                    relief="solid",
                    borderwidth=1,
                    wrap="word",
                )
                widget.grid(row=i, column=1, padx=(0, 20), pady=10, sticky="ew")
            else:
                widget = Entry(
                    inner,
                    font=self.italic_font,
                    relief="solid",
                    borderwidth=1,
                )
                widget.grid(row=i, column=1, padx=(0, 20), pady=10, sticky="ew")

            self._text_widgets[field] = widget

    def _create_save_button(self):
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

    def _on_date_selected(self, event):
        selected_date = self._selected_date.get()
        entry = self._on_date(selected_date)
        if entry:
            self._editing = True
            self._original_data = entry.entry_dict
            self._prepopulate_fields(entry.entry_dict)
        else:
            self.clear_fields(reset_date=False)

    def _input_is_valid(self, raw_data):
        valid = True
        if not raw_data or not any(raw_data[field] for field in ENTRY_FIELDS):
            self._show_error("No input detected", "Please fill in at least one field before saving.")
            valid = False

        for field, value in raw_data.items():
            if len(value) > 2000:
                self._show_error(f"Input for {field} too long", "Please limit each field to 2000 characters.")
                valid = False

        return valid

    @staticmethod
    def _get_filtered_data(raw_data):
        filtered_data = {
            field: value.strip() for field, value in raw_data.items()
            if value is not None and value.strip() != ""
        }
        return filtered_data

    def refresh(self):
        """Reset today's date; check the selected date and prepopulate or clear fields accordingly."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        self._selected_date.set(today)
        entry = self._on_date(self._selected_date.get())
        if entry:
            self._on_edit(entry.entry_dict)
        else:
            self.clear_fields(reset_date=False)

    def _on_save(self):
        """Collect field values and submit via the save callback."""
        new_data = self.get_entry_data()
        if self._input_is_valid(new_data):
            data = self._get_filtered_data(new_data)

            if self._editing and self._original_data:
                self._determine_update_route(data)
            else:
                self._on_valid_save(data)

            self._editing = False
            self._original_data = None
            self._on_home()

    def _determine_update_route(self, new_data):
        if self._is_update_required(new_data):
            # If all values are changed, put route, else patch route
            if all(self._original_data.get(field) != value for field, value in new_data.items()):
                self._on_full_replace(new_data)
            else:
                self._on_partial_update(new_data)
        else:
            return

    def _is_update_required(self, new_data):
        for field, value in new_data.items():
            if self._original_data.get(field) != value and value != "":
                return True
        return False

    def _show_error(self, title, message):
        """Display an error message in a pop-up window."""
        error_window = Toplevel(self)
        error_window.title(title)
        error_window.geometry("300x150")
        error_window.resizable(False, False)

        Label(error_window, text=message, font=self.subheading_font, wraplength=280).pack(pady=20)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

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

    def _on_edit(self, original_data):
        self._prepopulate_fields(original_data)
        self._editing = True
        self._original_data = original_data

    def get_entry_data(self):
        """Return a dict of the current date and field values."""
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

    def clear_fields(self, reset_date=True):
        """Clear all fields and reset date to today."""
        if reset_date:
            today = datetime.date.today().strftime("%Y-%m-%d")
            self._selected_date.set(today)
        self._editing = False
        self._original_data = None
        for widget in self._text_widgets.values():
            if isinstance(widget, Text):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")
